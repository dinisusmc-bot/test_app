import { useState } from 'react';
import Marker from 'react-map-gl/Marker';

interface DeviceMarkerProps {
  device: {
    id: string;
    name: string;
    lat: number;
    lon: number;
    status: string;
    type: string;
  };
  onClick: () => void;
}

export default function DeviceMarker({ device, onClick }: DeviceMarkerProps) {
  const [hovered, setHovered] = useState(false);

  const color = device.status === 'online' ? '#007cbf' : device.status === 'offline' ? '#e74c3c' : '#f39c12';

  return (
    <Marker
      latitude={device.lat}
      longitude={device.lon}
      onClick={(e) => {
        e.stopPropagation();
        onClick();
      }}
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
