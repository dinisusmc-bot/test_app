import { useState } from 'react';
import MapContainer from '../Map/MapContainer';
import DeviceList from '../DeviceList';

export default function Dashboard() {
  const [selectedDevice, setSelectedDevice] = useState<string | null>(null);
  const [devices, setDevices] = useState([]);

  return (
    <div className="dashboard" style={{ padding: '20px', minHeight: '100vh' }}>
      <header style={{ marginBottom: '20px' }}>
        <h1>Command & Control Dashboard</h1>
        <p>LA / San Diego Area Monitoring</p>
      </header>

      <div className="dashboard-content" style={{ display: 'flex', gap: '20px' }}>
        <div style={{ flex: 1, height: '600px' }}>
          <MapContainer />
        </div>
        
        <div style={{ flex: 1 }}>
          <DeviceList devices={devices} onSelect={setSelectedDevice} />
        </div>
      </div>
    </div>
  );
}
