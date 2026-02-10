import { useState, useEffect } from 'react';
import MapContainer from '../Map/MapContainer';
import DeviceList from './DeviceList';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

interface Device {
  id: string;
  name: string;
  type: string;
  status: 'online' | 'offline' | 'maintenance';
  lat: number;
  lon: number;
  lastSeen: string;
}

export default function Dashboard() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/devices`);
        if (!response.ok) throw new Error('Failed to fetch devices');
        const data = await response.json();
        // Handle both array and object response formats
        const devices = Array.isArray(data) ? data : (data as any).devices || [];
        setDevices(devices);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchDevices();
  }, []);

  const handleDeviceSelect = (device: Device) => {
    setSelectedDevice(device);
  };

  const stats = {
    total: devices.length,
    online: devices.filter((d) => d.status === 'online').length,
    offline: devices.filter((d) => d.status === 'offline').length,
    maintenance: devices.filter((d) => d.status === 'maintenance').length,
  };

  return (
    <div className="dashboard" style={{ minHeight: '100vh', padding: '20px', fontFamily: 'system-ui, sans-serif' }}>
      <header style={{ marginBottom: '20px' }}>
        <h1 style={{ margin: 0 }}>Command & Control Dashboard</h1>
        <p style={{ margin: '5px 0 0', color: '#666' }}>LA / San Diego Area Monitoring</p>
      </header>

      {/* Stats Cards */}
      <div style={{ display: 'flex', gap: '15px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <div style={{ flex: '1 1 120px', padding: '15px', backgroundColor: '#f0f4f8', borderRadius: '8px', textAlign: 'center' }}>
          <strong style={{ display: 'block', fontSize: '24px', color: '#2196f3' }}>{stats.total}</strong>
          <span style={{ color: '#666' }}>Total Devices</span>
        </div>
        <div style={{ flex: '1 1 120px', padding: '15px', backgroundColor: '#e3f2fd', borderRadius: '8px', textAlign: 'center' }}>
          <strong style={{ display: 'block', fontSize: '24px', color: '#4caf50' }}>{stats.online}</strong>
          <span style={{ color: '#666' }}>Online</span>
        </div>
        <div style={{ flex: '1 1 120px', padding: '15px', backgroundColor: '#ffebee', borderRadius: '8px', textAlign: 'center' }}>
          <strong style={{ display: 'block', fontSize: '24px', color: '#f44336' }}>{stats.offline}</strong>
          <span style={{ color: '#666' }}>Offline</span>
        </div>
        <div style={{ flex: '1 1 120px', padding: '15px', backgroundColor: '#fff3e0', borderRadius: '8px', textAlign: 'center' }}>
          <strong style={{ display: 'block', fontSize: '24px', color: '#ff9800' }}>{stats.maintenance}</strong>
          <span style={{ color: '#666' }}>Maintenance</span>
        </div>
      </div>

      {/* Content */}
      {loading && <p>Loading devices...</p>}
      {error && <p style={{ color: '#f44336' }}>Error: {error}</p>}

      {!loading && !error && (
        <div style={{ display: 'flex', gap: '20px', height: '600px', minHeight: 0 }}>
          {/* Map */}
          <div style={{ flex: 1, height: '100%', borderRadius: '8px', overflow: 'hidden', border: '1px solid #ddd' }}>
            <MapContainer devices={devices} />
          </div>

          {/* Device List */}
          <div style={{ flex: 1, backgroundColor: '#f5f5f5', borderRadius: '8px', overflow: 'hidden', border: '1px solid #ddd' }}>
            <DeviceList devices={devices} onSelect={handleDeviceSelect} />
          </div>

          {/* Device Details Panel */}
          {selectedDevice && (
            <div style={{ flex: 1, backgroundColor: '#fff', borderRadius: '8px', padding: '20px', border: '1px solid #ddd', overflow: 'auto' }}>
              <h2 style={{ margin: '0 0 15px', fontSize: '20px' }}>{selectedDevice.name}</h2>
              <div style={{ marginBottom: '10px' }}>
                <strong>Type:</strong> {selectedDevice.type}
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Status:</strong>{' '}
                <span
                  style={{
                    padding: '4px 8px',
                    borderRadius: '4px',
                    backgroundColor: selectedDevice.status === 'online' ? '#e8f5e9' : selectedDevice.status === 'offline' ? '#ffebee' : '#fff3e0',
                    color: selectedDevice.status === 'online' ? '#2e7d32' : selectedDevice.status === 'offline' ? '#c62828' : '#e65100',
                  }}
                >
                  {selectedDevice.status.toUpperCase()}
                </span>
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>ID:</strong> {selectedDevice.id}
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Location:</strong> {selectedDevice.lat.toFixed(4)}, {selectedDevice.lon.toFixed(4)}
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>Last Seen:</strong> {selectedDevice.lastSeen}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
