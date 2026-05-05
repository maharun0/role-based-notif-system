import type { NotificationRecipient } from '../types'
import { useUser } from '../context/UserContext'
import { formatRelativeTime } from '../utils/date'

interface NotificationItemProps {
  recipient: NotificationRecipient
}

export default function NotificationItem({ recipient }: NotificationItemProps) {
  const { markAsRead } = useUser()
  const { notification, is_read, delivered_at } = recipient

  return (
    <div
      className={`flex gap-4 p-4 rounded-lg border transition-colors ${
        is_read
          ? 'bg-white border-gray-100 opacity-75'
          : 'bg-white border-blue-100 border-l-4 border-l-blue-500 shadow-sm'
      }`}
    >
      <div className="mt-1 flex-shrink-0">
        <span
          className={`w-2 h-2 rounded-full inline-block ${is_read ? 'bg-gray-300' : 'bg-blue-500'}`}
        />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <p className={`text-sm font-medium truncate ${is_read ? 'text-gray-500' : 'text-gray-800'}`}>
            {notification.title}
          </p>
          <span className="text-xs text-gray-400 flex-shrink-0">{formatRelativeTime(delivered_at)}</span>
        </div>
        <p className="text-sm text-gray-500 mt-0.5 line-clamp-2">{notification.message}</p>
        <div className="flex items-center gap-3 mt-2">
          <span
            className={`text-[10px] font-medium px-1.5 py-0.5 rounded uppercase tracking-wide ${
              notification.audience_type === 'ALL'
                ? 'bg-purple-50 text-purple-600'
                : 'bg-amber-50 text-amber-600'
            }`}
          >
            {notification.audience_type === 'ALL' ? 'All' : 'By Role'}
          </span>
          <button
            onClick={() => markAsRead(notification.id, !is_read)}
            className="text-xs text-blue-500 hover:text-blue-700 transition-colors"
          >
            {is_read ? 'Mark unread' : 'Mark read'}
          </button>
        </div>
      </div>
    </div>
  )
}
