import AdminPanel from '../components/AdminPanel'
import NotificationBell from '../components/NotificationBell'
import NotificationList from '../components/NotificationList'
import UserSwitcher from '../components/UserSwitcher'
import { useUser } from '../context/UserContext'

export default function Home() {
  const { activeUser } = useUser()
  if (!activeUser) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center text-sm text-gray-500">
        Loading users...
      </div>
    )
  }

  const isAdmin = activeUser.role.name === 'Admin'

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-100 sticky top-0 z-10 shadow-sm">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 bg-blue-600 rounded-lg flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 10-4 0v1.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </div>
            <span className="font-semibold text-gray-800 text-sm">NotifyApp</span>
          </div>
          <div className="flex items-center gap-3">
            <NotificationBell />
            <UserSwitcher />
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-6 space-y-4">
        {isAdmin && <AdminPanel />}
        <NotificationList />
      </main>
    </div>
  )
}
