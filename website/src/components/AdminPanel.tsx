import { useState } from 'react'
import type { AudienceType } from '../types'
import { useUser } from '../context/UserContext'
import Button from './common/Button'

export default function AdminPanel() {
  const { roles, addNotification } = useUser()
  const [title, setTitle] = useState('')
  const [message, setMessage] = useState('')
  const [audienceType, setAudienceType] = useState<AudienceType>('ALL')
  const [selectedRoleIds, setSelectedRoleIds] = useState<number[]>([])
  const [sent, setSent] = useState(false)

  const isValid =
    title.trim() !== '' &&
    message.trim() !== '' &&
    (audienceType === 'ALL' || selectedRoleIds.length > 0)

  function toggleRole(roleId: number) {
    setSelectedRoleIds(prev =>
      prev.includes(roleId) ? prev.filter(id => id !== roleId) : [...prev, roleId]
    )
  }

  function handleSend() {
    if (!isValid) return
    addNotification(title.trim(), message.trim(), audienceType, selectedRoleIds)
    setTitle('')
    setMessage('')
    setAudienceType('ALL')
    setSelectedRoleIds([])
    setSent(true)
    setTimeout(() => setSent(false), 2500)
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-blue-100 overflow-hidden">
      <div className="px-4 py-3 bg-blue-50 border-b border-blue-100 flex items-center gap-2">
        <svg className="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
        </svg>
        <h2 className="font-semibold text-blue-800 text-sm">Send Notification</h2>
      </div>

      <div className="p-4 space-y-3">
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Title</label>
          <input
            type="text"
            value={title}
            onChange={e => setTitle(e.target.value)}
            placeholder="Notification title"
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Message</label>
          <textarea
            value={message}
            onChange={e => setMessage(e.target.value)}
            placeholder="Notification message"
            rows={3}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-600 mb-2">Audience</label>
          <div className="flex gap-4">
            {(['ALL', 'BY_ROLE'] as AudienceType[]).map(type => (
              <label key={type} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  value={type}
                  checked={audienceType === type}
                  onChange={() => { setAudienceType(type); setSelectedRoleIds([]) }}
                  className="accent-blue-600"
                />
                <span className="text-sm text-gray-700">{type === 'ALL' ? 'All users' : 'By role'}</span>
              </label>
            ))}
          </div>
        </div>

        {audienceType === 'BY_ROLE' && (
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-2">Select roles</label>
            <div className="flex flex-wrap gap-2">
              {roles.map(role => (
                <label key={role.id} className="flex items-center gap-1.5 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedRoleIds.includes(role.id)}
                    onChange={() => toggleRole(role.id)}
                    className="accent-blue-600"
                  />
                  <span className="text-sm text-gray-700">{role.name}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        <div className="flex items-center gap-3 pt-1">
          <Button onClick={handleSend} disabled={!isValid}>
            Send Notification
          </Button>
          {sent && (
            <span className="text-xs text-green-600 font-medium">Sent successfully</span>
          )}
        </div>
      </div>
    </div>
  )
}
