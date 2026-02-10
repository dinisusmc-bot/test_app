import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Device endpoints
export const devicesApi = {
  getAll: () => api.get('/devices'),
  getById: (id: string) => api.get(`/devices/${id}`),
  create: (data: any) => api.post('/devices', data),
  update: (id: string, data: any) => api.put(`/devices/${id}`, data),
  delete: (id: string) => api.delete(`/devices/${id}`),
};

// Location endpoints
export const locationsApi = {
  getAll: () => api.get('/locations'),
  getById: (id: string) => api.get(`/locations/${id}`),
  create: (data: any) => api.post('/locations', data),
  nearby: (lat: number, lon: number, radius: number) => 
    api.get(`/locations/nearby?lat=${lat}&lon=${lon}&radius_km=${radius}`),
};

// Event endpoints
export const eventsApi = {
  getAll: () => api.get('/events'),
  getByDevice: (deviceId: string) => api.get(`/events/device/${deviceId}`),
  create: (data: any) => api.post('/events', data),
};

// Command endpoints
export const commandsApi = {
  getAll: () => api.get('/commands'),
  getById: (id: string) => api.get(`/commands/${id}`),
  create: (data: any) => api.post('/commands', data),
};

export default api;
