import type { Notification, NotificationRecipient, Role, User } from '../types'

const t = (minutesAgo: number) =>
  new Date(Date.now() - minutesAgo * 60_000).toISOString()

export const MOCK_ROLES: Role[] = [
  { id: 1, name: 'Admin', created_at: t(14400) },
  { id: 2, name: 'Manager', created_at: t(14400) },
  { id: 3, name: 'Editor', created_at: t(14400) },
  { id: 4, name: 'Viewer', created_at: t(14400) },
  { id: 5, name: 'Support', created_at: t(14400) },
]

export const MOCK_USERS: User[] = [
  { id: 1, name: 'Alice Admin', email: 'alice@example.com', role_id: 1, role: MOCK_ROLES[0], created_at: t(14400) },
  { id: 2, name: 'Bob Manager', email: 'bob@example.com', role_id: 2, role: MOCK_ROLES[1], created_at: t(14400) },
  { id: 3, name: 'Carol Editor', email: 'carol@example.com', role_id: 3, role: MOCK_ROLES[2], created_at: t(14400) },
  { id: 4, name: 'Dave Viewer', email: 'dave@example.com', role_id: 4, role: MOCK_ROLES[3], created_at: t(14400) },
  { id: 5, name: 'Eve Support', email: 'eve@example.com', role_id: 5, role: MOCK_ROLES[4], created_at: t(14400) },
  { id: 6, name: 'Frank Manager', email: 'frank@example.com', role_id: 2, role: MOCK_ROLES[1], created_at: t(14400) },
]

const notif1 = { id: 1, title: 'Welcome to the Platform', message: 'Hello everyone — glad to have you on board.', audience_type: 'ALL' as const, created_by: 1, created_at: t(1440) }
const notif2 = { id: 2, title: 'Q2 Planning Session', message: 'All managers: planning meeting today at 3 pm in room B.', audience_type: 'BY_ROLE' as const, created_by: 1, created_at: t(120) }
const notif3 = { id: 3, title: 'Content Guidelines Updated', message: 'New editorial guidelines are live. Please review before your next publish.', audience_type: 'BY_ROLE' as const, created_by: 1, created_at: t(30) }
const notif4 = { id: 4, title: 'Scheduled Maintenance', message: 'System will be unavailable tonight from 11 pm to 1 am for maintenance.', audience_type: 'ALL' as const, created_by: 1, created_at: t(15) }

let recipientSeq = 0
const mkRecipient = (
  notification_id: number,
  user_id: number,
  is_read: boolean,
  deliveredMinutesAgo: number,
  notification: Notification
): NotificationRecipient => ({
  id: ++recipientSeq,
  notification_id,
  user_id,
  is_read,
  read_at: is_read ? t(deliveredMinutesAgo - 5) : null,
  delivered_at: t(deliveredMinutesAgo),
  notification,
})

export const MOCK_RECIPIENTS: NotificationRecipient[] = [
  // notif1: ALL users — Alice has read it
  ...MOCK_USERS.map(u => mkRecipient(1, u.id, u.id === 1, 1440, notif1)),
  // notif2: BY_ROLE Manager (Bob=2, Frank=6)
  ...MOCK_USERS.filter(u => u.role_id === 2).map(u => mkRecipient(2, u.id, false, 120, notif2)),
  // notif3: BY_ROLE Editor (Carol=3)
  ...MOCK_USERS.filter(u => u.role_id === 3).map(u => mkRecipient(3, u.id, false, 30, notif3)),
  // notif4: ALL users — none read yet
  ...MOCK_USERS.map(u => mkRecipient(4, u.id, false, 15, notif4)),
]
