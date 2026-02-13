import GeoMapSimulation from './components/Map/GeoMapSimulation';

function App() {
  // Sample assets data (mix of friendly and enemy)
  const assets = [
    { id: 'asset-1', name: 'Friendly-Drone-LA-101', asset_type: 'drone', status: 'available' as const, lat: 34.0522, lon: -118.2437, is_friendly: true, last_seen: new Date().toISOString() },
    { id: 'asset-2', name: 'Friendly-Sensor-LA-102', asset_type: 'sensor', status: 'in_use' as const, lat: 34.06, lon: -118.25, is_friendly: true, last_seen: new Date().toISOString() },
    { id: 'asset-3', name: 'Friendly-Camera-LA-103', asset_type: 'camera', status: 'available' as const, lat: 34.04, lon: -118.24, is_friendly: true, last_seen: new Date().toISOString() },
    { id: 'asset-4', name: 'Friendly-Vehicle-SA-104', asset_type: 'vehicle', status: 'maintenance' as const, lat: 34.05, lon: -118.23, is_friendly: true, last_seen: new Date().toISOString() },
    { id: 'asset-5', name: 'Friendly-Drone-SA-105', asset_type: 'drone', status: 'available' as const, lat: 32.7157, lon: -117.1611, is_friendly: true, last_seen: new Date().toISOString() },
  ];

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <GeoMapSimulation assets={assets} />
    </div>
  );
}

export default App;
