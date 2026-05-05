export interface Role {
  id: number
  name: string
  created_at: string
}

export interface User {
  id: number
  name: string
  email: string
  role_id: number
  role: Role
  created_at: string
}

export interface Notification {
  id: number
  title: string
  message: string
  audience_type: 'ALL' | 'BY_ROLE'
  created_by: number
  created_at: string
}

export interface NotificationRecipient {
  id: number
  notification_id: number
  user_id: number
  is_read: boolean
  read_at: string | null
  delivered_at: string
  notification: Notification
}

export type AudienceType = 'ALL' | 'BY_ROLE'
