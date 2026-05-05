import { createContext, useContext, useState } from 'react'
import type { AudienceType, NotificationRecipient, Role, User } from '../types'
import { MOCK_RECIPIENTS, MOCK_ROLES, MOCK_USERS } from '../utils/mockData'

interface UserContextValue {
  activeUser: User
  setActiveUser: (user: User) => void
  users: User[]
  roles: Role[]
  notifications: NotificationRecipient[]
  unreadCount: number
  addNotification: (title: string, message: string, audienceType: AudienceType, roleIds: number[]) => void
  markAsRead: (recipientId: number, isRead: boolean) => void
}

const UserContext = createContext<UserContextValue | null>(null)

let nextId = 1000

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [activeUser, setActiveUser] = useState<User>(MOCK_USERS[0])
  const [allRecipients, setAllRecipients] = useState<NotificationRecipient[]>(MOCK_RECIPIENTS)

  const notifications = allRecipients
    .filter(r => r.user_id === activeUser.id)
    .sort((a, b) => new Date(b.delivered_at).getTime() - new Date(a.delivered_at).getTime())

  const unreadCount = notifications.filter(n => !n.is_read).length

  function addNotification(title: string, message: string, audienceType: AudienceType, roleIds: number[]) {
    const now = new Date().toISOString()
    const notifId = ++nextId
    const newNotif = {
      id: notifId,
      title,
      message,
      audience_type: audienceType,
      created_by: activeUser.id,
      created_at: now,
    }

    const targets =
      audienceType === 'ALL'
        ? MOCK_USERS
        : MOCK_USERS.filter(u => roleIds.includes(u.role_id))

    const newRecipients: NotificationRecipient[] = targets.map(u => ({
      id: ++nextId,
      notification_id: notifId,
      user_id: u.id,
      is_read: false,
      read_at: null,
      delivered_at: now,
      notification: newNotif,
    }))

    setAllRecipients(prev => [...newRecipients, ...prev])
  }

  function markAsRead(recipientId: number, isRead: boolean) {
    setAllRecipients(prev =>
      prev.map(r =>
        r.id === recipientId
          ? { ...r, is_read: isRead, read_at: isRead ? new Date().toISOString() : null }
          : r
      )
    )
  }

  return (
    <UserContext.Provider
      value={{ activeUser, setActiveUser, users: MOCK_USERS, roles: MOCK_ROLES, notifications, unreadCount, addNotification, markAsRead }}
    >
      {children}
    </UserContext.Provider>
  )
}

export function useUser(): UserContextValue {
  const ctx = useContext(UserContext)
  if (!ctx) throw new Error('useUser must be used within UserProvider')
  return ctx
}
