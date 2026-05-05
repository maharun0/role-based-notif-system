import { useEffect } from 'react'

function getWebSocketBaseUrl() {
  const configured = import.meta.env.VITE_WS_URL
  if (configured) return configured

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${window.location.host}/ws`
}

export function useWebSocket(userId: number | null, onNotification: () => void) {
  useEffect(() => {
    if (!userId) return

    const wsBaseUrl = getWebSocketBaseUrl().replace(/\/$/, '')
    const socket = new WebSocket(`${wsBaseUrl}/${userId}`)

    socket.onmessage = () => {
      onNotification()
    }

    return () => {
      socket.close()
    }
  }, [onNotification, userId])
}
