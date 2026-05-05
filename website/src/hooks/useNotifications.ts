import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  createNotification,
  getUnreadCount,
  getUserNotifications,
  markNotificationRead,
  type CreateNotificationPayload,
} from '../api/notifications'
import type { NotificationRecipient } from '../types'

export type NotificationFilter = 'all' | 'unread' | 'read'

export function useNotifications(userId: number | null) {
  const [notifications, setNotifications] = useState<NotificationRecipient[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState<NotificationFilter>('all')
  const [loading, setLoading] = useState(false)
  const cacheRef = useRef<Map<string, NotificationRecipient[]>>(new Map())
  const unreadCacheRef = useRef<Map<number, number>>(new Map())

  const cacheKey = useMemo(
    () => `${userId ?? 0}|${filter}|${search.trim().toLowerCase()}`,
    [filter, search, userId]
  )

  const loadUnreadCount = useCallback(
    async (force = false) => {
      if (!userId) return
      const cached = unreadCacheRef.current.get(userId)
      if (!force && cached !== undefined) {
        setUnreadCount(cached)
        return
      }
      const count = await getUnreadCount(userId)
      unreadCacheRef.current.set(userId, count)
      setUnreadCount(count)
    },
    [userId]
  )

  const loadNotifications = useCallback(
    async (force = false) => {
      if (!userId) return
      if (!force && cacheRef.current.has(cacheKey)) {
        setNotifications(cacheRef.current.get(cacheKey) ?? [])
        return
      }

      const params = {
        isRead: filter === 'all' ? undefined : filter === 'read',
        search: search.trim() || undefined,
      }
      const data = await getUserNotifications(userId, params)
      cacheRef.current.set(cacheKey, data)
      setNotifications(data)
    },
    [cacheKey, filter, search, userId]
  )

  const refresh = useCallback(async () => {
    if (!userId) return
    setLoading(true)
    try {
      cacheRef.current.delete(cacheKey)
      unreadCacheRef.current.delete(userId)
      await Promise.all([loadNotifications(true), loadUnreadCount(true)])
    } finally {
      setLoading(false)
    }
  }, [cacheKey, loadNotifications, loadUnreadCount, userId])

  const markAsRead = useCallback(
    async (notificationId: number, isRead: boolean) => {
      if (!userId) return
      await markNotificationRead(notificationId, { user_id: userId, is_read: isRead })

      unreadCacheRef.current.delete(userId)
      for (const key of cacheRef.current.keys()) {
        if (key.startsWith(`${userId}|`)) cacheRef.current.delete(key)
      }
      await refresh()
    },
    [refresh, userId]
  )

  const sendNotification = useCallback(
    async (payload: CreateNotificationPayload) => {
      await createNotification(payload)
      // New notifications may impact multiple users (ALL/BY_ROLE), so drop caches.
      cacheRef.current.clear()
      unreadCacheRef.current.clear()
      await refresh()
    },
    [refresh]
  )

  useEffect(() => {
    if (!userId) return
    setLoading(true)
    Promise.all([loadNotifications(), loadUnreadCount()]).finally(() => setLoading(false))
  }, [loadNotifications, loadUnreadCount, userId])

  return {
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
  }
}
