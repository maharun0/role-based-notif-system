import { useUser } from '../context/UserContext'

export default function UserSwitcher() {
  const { activeUser, setActiveUser, users } = useUser()

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-gray-400 hidden sm:inline">Viewing as</span>
      <select
        value={activeUser.id}
        onChange={e => {
          const user = users.find(u => u.id === Number(e.target.value))
          if (user) setActiveUser(user)
        }}
        className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
      >
        {users.map(user => (
          <option key={user.id} value={user.id}>
            {user.name} · {user.role.name}
          </option>
        ))}
      </select>
    </div>
  )
}
