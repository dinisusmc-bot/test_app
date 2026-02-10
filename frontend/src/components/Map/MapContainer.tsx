import Map from 'react-map-gl';
import DeviceMarker from './DeviceMarker';
import 'maplibre-gl/dist/maplibre-gl.css';

interface Device {
  id: string;
  name: string;
  type: string;
  status: 'online' | 'offline' | 'maintenance';
  lat: number;
  lon: number;
  lastSeen: string;
}

interface MapContainerProps {
  devices: Device[];
  center?: [number, number];
  zoom?: number;
}

export default function MapContainer({ devices, center = [-118.2437, 34.0522], zoom = 10 }: MapContainerProps) {
  const [viewport, setViewport] = useState({
    latitude: center[1],
    longitude: center[0],
    zoom: zoom,
  });
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const [popupOffset, setPopupOffset] = useState({ top: 0, bottom: 0, left: 0, right: 0 });

  return (
    <Map
      {...viewport}
      width="100%"
      height="100%"
      style={{ width: '100%', height: '100%' }}
      mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
      onMove={(evt) => setViewport(evt.viewState)}
      onClick={(e) => {
        if (e.originalEvent.type === 'click') {
          setSelectedDevice(null);
        }
      }}
    >
      {/* Device Markers */}
      {devices.map((device) => (
        <DeviceMarker
          key={device.id}
          device={device}
          onClick={() => setSelectedDevice(device)}
        />
      ))}

      {/* Popup for selected device */}
      {selectedDevice && (
        <Popup
          latitude={selectedDevice.lat}
          longitude={selectedDevice.lon}
          onClose={() => setSelectedDevice(null)}
          offset={popupOffset}
          className="device-popup"
          style={{ maxWidth: '250px' }}
        >
          <div style={{ padding: '10px' }}>
            <h4 style={{ margin: '0 0 5px', fontSize: '14px' }}>{selectedDevice.name}</h4>
            <div style={{ fontSize: '12px', color: '#666' }}>
              <p style={{ margin: '2px 0' }}>Type: {selectedDevice.type}</p>
              <p style={{ margin: '2px 0' }}>
                Status:{' '}
                <span
                  style={{
                    color: selectedDevice.status === 'online' ? '#4caf50' : selectedDevice.status === 'offline' ? '#f44336' : '#ff9800',
                  }}
                >
                  {selectedDevice.status}
                </span>
              </p>
              <p style={{ margin: '2px 0' }}>Last seen: {selectedDevice.lastSeen}</p>
            </div>
          </div>
        </Popup>
      )}
    </Map>
  );
}
