import { useEffect } from 'react'

function getWebSocketBaseUrl() {
  const configured = import.meta.env.VITE_WS_URL
  if (configured) return configured

  // Fallback supports local dev without explicit env configuration.
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${window.location.host}/ws`
}

export function useWebSocket(userId: number | null, onNotification: () => void) {
  useEffect(() => {
    if (!userId) return

    // Trim trailing slash to avoid accidental double-slash URLs.
    const wsBaseUrl = getWebSocketBaseUrl().replace(/\/$/, '')
    const socket = new WebSocket(`${wsBaseUrl}/${userId}`)

    socket.onmessage = () => {
      // Payload details are ignored here; we always refetch from API for consistency.
      onNotification()
    }

    return () => {
      socket.close()
    }
  }, [onNotification, userId])
}
