interface Device {
  id: string;
  name: string;
  type: string;
  status: 'online' | 'offline' | 'maintenance';
  lat: number;
  lon: number;
  lastSeen: string;
}

interface WebSocketService {
  connect: () => void;
  disconnect: () => void;
  onMessage: (callback: (data: Device) => void) => void;
  getStatus: () => 'connected' | 'connecting' | 'disconnected';
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

export const websocketService: WebSocketService = {
  ws: null as WebSocket | null,

  connect() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) return;

    this.ws = new WebSocket(WS_URL);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected, reconnecting in 5s...');
      setTimeout(() => this.connect(), 5000);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  },

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  },

  onMessage(callback: (data: Device) => void) {
    if (this.ws) {
      this.ws.onmessage = (event) => {
        try {
          const data: Device = JSON.parse(event.data);
          callback(data);
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
        }
      };
    }
  },

  getStatus() {
    if (!this.ws) return 'disconnected';
    if (this.ws.readyState === WebSocket.CONNECTING) return 'connecting';
    if (this.ws.readyState === WebSocket.OPEN) return 'connected';
    return 'disconnected';
  },
};

export default websocketService;
