interface Device {
  id: string;
  name: string;
  type: string;
  status: 'online' | 'offline' | 'maintenance';
  lat: number;
  lon: number;
  lastSeen: string;
}

interface DeviceListProps {
  devices: Device[];
  onSelect: (device: Device) => void;
}

export default function DeviceList({ devices, onSelect }: DeviceListProps) {
  if (devices.length === 0) {
    return (
      <div style={{ padding: '20px', height: '100%', overflowY: 'auto' }}>
        <p style={{ color: '#666', textAlign: 'center' }}>No devices found</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '10px', height: '100%', overflowY: 'auto' }}>
      <h3 style={{ margin: '0 0 15px', fontSize: '16px' }}>Devices ({devices.length})</h3>
      {devices.map((device) => (
        <div
          key={device.id}
          onClick={() => onSelect(device)}
          style={{
            padding: '12px',
            marginBottom: '8px',
            backgroundColor: '#fff',
            borderRadius: '6px',
            cursor: 'pointer',
            border: `2px solid ${device.status === 'online' ? '#4caf50' : device.status === 'offline' ? '#f44336' : '#ff9800'}`,
            transition: 'all 0.2s',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.boxShadow = 'none';
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h4 style={{ margin: 0, fontSize: '14px', fontWeight: 500 }}>{device.name}</h4>
            <span
              style={{
                padding: '3px 8px',
                borderRadius: '4px',
                fontSize: '11px',
                fontWeight: 500,
                backgroundColor: device.status === 'online' ? '#e8f5e9' : device.status === 'offline' ? '#ffebee' : '#fff3e0',
                color: device.status === 'online' ? '#2e7d32' : device.status === 'offline' ? '#c62828' : '#e65100',
              }}
            >
              {device.status.toUpperCase()}
            </span>
          </div>
          <p style={{ margin: '6px 0 0', fontSize: '12px', color: '#666' }}>
            {device.type} • {device.id.slice(0, 8)}...
          </p>
        </div>
      ))}
    </div>
  );
}
