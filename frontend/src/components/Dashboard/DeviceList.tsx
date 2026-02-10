interface Device {
  id: string;
  name: string;
  type: string;
  status: string;
}

interface DeviceListProps {
  devices: Device[];
  onSelect: (id: string) => void;
}

export default function DeviceList({ devices, onSelect }: DeviceListProps) {
  return (
    <div className="device-list" style={{ maxHeight: '600px', overflowY: 'auto' }}>
      {devices.length === 0 ? (
        <p>No devices found</p>
      ) : (
        devices.map((device) => (
          <div
            key={device.id}
            onClick={() => onSelect(device.id)}
            style={{
              padding: '10px',
              marginBottom: '10px',
              backgroundColor: device.status === 'online' ? '#e3f2fd' : '#ffebee',
              borderRadius: '8px',
              cursor: 'pointer',
              border: `2px solid ${device.status === 'online' ? '#2196f3' : '#f44336'}`,
            }}
          >
            <h4>{device.name}</h4>
            <p>Type: {device.type} | Status: {device.status}</p>
          </div>
        ))
      )}
    </div>
  );
}
