import client from './client'
import type { AudienceType, Notification, NotificationRecipient } from '../types'

export interface CreateNotificationPayload {
  title: string
  message: string
  audience_type: AudienceType
  role_ids: number[]
  created_by: number
}

export interface MarkReadPayload {
  user_id: number
  is_read: boolean
}

export async function getUserNotifications(
  userId: number,
  params?: { isRead?: boolean; search?: string }
): Promise<NotificationRecipient[]> {
  const { data } = await client.get<NotificationRecipient[]>(`/users/${userId}/notifications`, {
    params: {
      is_read: params?.isRead,
      search: params?.search || undefined,
    },
  })
  return data
}

export async function getUnreadCount(userId: number): Promise<number> {
  const { data } = await client.get<{ unread_count: number }>(
    `/users/${userId}/notifications/unread-count`
  )
  return data.unread_count
}

export async function createNotification(
  payload: CreateNotificationPayload
): Promise<Notification> {
  const { data } = await client.post<Notification>('/notifications', payload)
  return data
}

export async function markNotificationRead(
  notificationId: number,
  payload: MarkReadPayload
): Promise<NotificationRecipient> {
  const { data } = await client.patch<NotificationRecipient>(
    `/notifications/${notificationId}/read`,
    payload
  )
  return data
}
