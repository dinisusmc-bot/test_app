import { useState } from 'react';
import { Marker } from 'react-map-gl/maplibre';

interface DeviceMarkerProps {
  device: {
    id: string;
    name: string;
    lat: number;
    lon: number;
    status: 'online' | 'offline' | 'maintenance';
    type: string;
  };
  onClick: () => void;
}

export default function DeviceMarker({ device, onClick }: DeviceMarkerProps) {
  const [hovered, setHovered] = useState(false);

  const color =
    device.status === 'online' ? '#4caf50' :
    device.status === 'offline' ? '#f44336' : '#ff9800';

  return (
    <Marker
      latitude={device.lat}
      longitude={device.lon}
      onClick={onClick}
    >
      <div
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        style={{
          backgroundColor: color,
          width: hovered ? 24 : 16,
          height: hovered ? 24 : 16,
          borderRadius: '50%',
          border: '2px solid white',
          boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
          cursor: 'pointer',
          transition: 'all 0.2s',
        }}
        title={`${device.name} (${device.type}) - ${device.status}`}
      />
    </Marker>
  );
}
