import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { getUsers } from '../api/users'
import client from '../api/client'
import { useNotifications, type NotificationFilter } from '../hooks/useNotifications'
import { useWebSocket } from '../hooks/useWebSocket'
import type { AudienceType, NotificationRecipient, Role, User } from '../types'

interface UserContextValue {
  activeUser: User | null
  setActiveUser: (user: User) => void
  users: User[]
  roles: Role[]
  notifications: NotificationRecipient[]
  unreadCount: number
  loading: boolean
  search: string
  filter: NotificationFilter
  setSearch: (value: string) => void
  setFilter: (value: NotificationFilter) => void
  addNotification: (
    title: string,
    message: string,
    audienceType: AudienceType,
    roleIds: number[]
  ) => Promise<void>
  markAsRead: (notificationId: number, isRead: boolean) => Promise<void>
}

const UserContext = createContext<UserContextValue | null>(null)

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [users, setUsers] = useState<User[]>([])
  const [roles, setRoles] = useState<Role[]>([])
  const [activeUserId, setActiveUserId] = useState<number | null>(null)

  useEffect(() => {
    async function bootstrap() {
      // Load reference data in parallel so first paint has real users/roles.
      const [usersData, rolesData] = await Promise.all([
        getUsers(),
        client.get<Role[]>('/roles').then(res => res.data),
      ])
      setUsers(usersData)
      setRoles(rolesData)
      setActiveUserId(prev => prev ?? usersData[0]?.id ?? null)
    }
    void bootstrap()
  }, [])

  const activeUser = useMemo(
    // Keep a stable object reference based on the selected id.
    () => users.find(user => user.id === activeUserId) ?? null,
    [activeUserId, users]
  )

  const {
    notifications,
    unreadCount,
    loading,
    search,
    filter,
    setSearch,
    setFilter,
    refresh,
    markAsRead,
    sendNotification,
  } = useNotifications(activeUser?.id ?? null)

  // WebSocket events only trigger a refetch; source of truth stays in REST endpoints.
  useWebSocket(activeUser?.id ?? null, refresh)

  async function addNotification(
    title: string,
    message: string,
    audienceType: AudienceType,
    roleIds: number[]
  ) {
    // No auth in this assignment: current dropdown user acts as sender.
    if (!activeUser) return
    await sendNotification({
      title,
      message,
      audience_type: audienceType,
      role_ids: roleIds,
      created_by: activeUser.id,
    })
  }

  function setActiveUser(user: User) {
    setActiveUserId(user.id)
  }

  return (
    <UserContext.Provider
      value={{
        activeUser,
        setActiveUser,
        users,
        roles,
        notifications,
        unreadCount,
        loading,
        search,
        filter,
        setSearch,
        setFilter,
        addNotification,
        markAsRead,
      }}
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
