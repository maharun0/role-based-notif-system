import { useState } from 'react'
import { useUser } from '../context/UserContext'
import NotificationItem from './NotificationItem'

export default function NotificationList() {
  const { notifications, unreadCount, loading, search, filter, setSearch, setFilter } = useUser()
  const [searchDraft, setSearchDraft] = useState(search)

  function submitSearch() {
    setSearch(searchDraft)
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-2">
          <h2 className="font-semibold text-gray-800 text-sm">Notifications</h2>
          {unreadCount > 0 && (
            <span className="text-xs bg-blue-100 text-blue-700 font-medium px-2 py-0.5 rounded-full">
              {unreadCount} unread
            </span>
          )}
        </div>
        <div className="flex items-center gap-2 flex-1 min-w-0 justify-end">
          <div className="relative flex-1 max-w-xs">
            <svg
              className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-400"
              fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              placeholder="Search..."
              value={searchDraft}
              onChange={e => setSearchDraft(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter') submitSearch()
              }}
              className="w-full pl-8 pr-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="button"
            onClick={submitSearch}
            className="text-xs border border-gray-200 rounded-lg px-2.5 py-1.5 text-gray-600 hover:bg-gray-50"
          >
            Search
          </button>
          <select
            value={filter}
            onChange={e => setFilter(e.target.value as 'all' | 'unread' | 'read')}
            className="text-sm border border-gray-200 rounded-lg px-2 py-1.5 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
          >
            <option value="all">All</option>
            <option value="unread">Unread</option>
            <option value="read">Read</option>
          </select>
        </div>
      </div>

      <div className="divide-y divide-gray-50">
        {loading ? (
          <div className="py-12 text-center text-sm text-gray-400">Loading notifications...</div>
        ) : notifications.length === 0 ? (
          <div className="py-12 text-center text-sm text-gray-400">No notifications found</div>
        ) : (
          notifications.map(r => <NotificationItem key={r.id} recipient={r} />)
        )}
      </div>
    </div>
  )
}
