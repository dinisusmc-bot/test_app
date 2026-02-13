import { useState, useMemo } from 'react';
import Map from 'react-map-gl/maplibre';
import type { ViewStateChangeEvent, MapLayerMouseEvent } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';

interface Asset {
  id: string;
  name: string;
  asset_type: string;
  status: 'available' | 'in_use' | 'maintenance' | 'offline';
  lat: number;
  lon: number;
  last_seen: string;
  is_friendly: boolean;
}

interface GeoMapSimulationProps {
  assets: Asset[];
  center?: [number, number];
  zoom?: number;
}

export default function GeoMapSimulation({ 
  assets, 
  center = [-118.2437, 34.0522], 
  zoom = 10 
}: GeoMapSimulationProps) {
  const [viewport, setViewport] = useState({
    latitude: center[1],
    longitude: center[0],
    zoom: zoom,
  });
  
  const [selectedEnemy, setSelectedEnemy] = useState<Asset | null>(null);
  const [isEngaging, setIsEngaging] = useState(false);
  const [currentProgress, setCurrentProgress] = useState(0);
  const [missileSource, setMissileSource] = useState<{lat: number, lon: number} | null>(null);
  const [missileTarget, setMissileTarget] = useState<{lat: number, lon: number} | null>(null);
  const [nearestFriendlyId, setNearestFriendlyId] = useState<string | null>(null);

  // Sample enemy assets
  const enemyAssets = useMemo(() => [
    { id: 'enemy-1', name: 'Enemy-Alpha', asset_type: 'drone', status: 'offline' as const, lat: 34.0522 + 0.01, lon: -118.2437 + 0.01, last_seen: new Date().toISOString(), is_friendly: false },
    { id: 'enemy-2', name: 'Enemy-Beta', asset_type: 'sensor', status: 'offline' as const, lat: 34.0522 - 0.01, lon: -118.2437 - 0.01, last_seen: new Date().toISOString(), is_friendly: false },
    { id: 'enemy-3', name: 'Enemy-Gamma', asset_type: 'camera', status: 'offline' as const, lat: 34.0522 + 0.005, lon: -118.2437 + 0.005, last_seen: new Date().toISOString(), is_friendly: false },
  ], []);

  // Calculate Euclidean distance
  const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
    const latDiff = lat2 - lat1;
    const lonDiff = lon2 - lon1;
    return Math.sqrt(latDiff * latDiff + lonDiff * lonDiff);
  };

  // Find nearest friendly to enemy
  const findNearestFriendly = (enemy: Asset, friendlyList: Asset[]): Asset | null => {
    if (friendlyList.length === 0) return null;
    let nearest: Asset | null = null;
    let minDistance = Infinity;
    friendlyList.forEach(friendly => {
      const dist = calculateDistance(enemy.lat, enemy.lon, friendly.lat, friendly.lon);
      if (dist < minDistance) {
        minDistance = dist;
        nearest = friendly;
      }
    });
    return nearest;
  };

  const handleEnemyClick = (enemy: Asset) => {
    const friendlyAssets = assets.filter(a => 
      a.status === 'available' || a.status === 'in_use'
    );
    const nearest = findNearestFriendly(enemy, friendlyAssets);
    setNearestFriendlyId(nearest?.id || null);
    setSelectedEnemy(enemy);
  };

  const handleCancelEngagement = () => {
    setIsEngaging(false);
    setCurrentProgress(0);
    setMissileSource(null);
    setMissileTarget(null);
    setSelectedEnemy(null);
    setNearestFriendlyId(null);
  };

  // Filter friendly assets
  const friendlyAssets = useMemo(() => {
    return assets.filter(a => a.status === 'available' || a.status === 'in_use');
  }, [assets]);

  // Get nearest friendly
  const nearestFriendly = useMemo(() => {
    if (!selectedEnemy || !nearestFriendlyId) return null;
    return friendlyAssets.find(a => a.id === nearestFriendlyId) || null;
  }, [selectedEnemy, nearestFriendlyId, friendlyAssets]);

  // Auto-engage when confirming
  const startEngagement = () => {
    if (selectedEnemy && nearestFriendly) {
      setMissileSource({ lat: nearestFriendly.lat, lon: nearestFriendly.lon });
      setMissileTarget({ lat: selectedEnemy.lat, lon: selectedEnemy.lon });
      setCurrentProgress(0);
      setIsEngaging(true);
    }
  };

  // Simulate missile animation
  const startMissileAnimation = () => {
    const interval = setInterval(() => {
      setCurrentProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsEngaging(false);
          setCurrentProgress(0);
          setMissileSource(null);
          setMissileTarget(null);
          return 100;
        }
        return prev + 2;
      });
    }, 100);
    setTimeout(() => {
      if (isEngaging && currentProgress < 100) {
        clearInterval(interval);
        setIsEngaging(false);
        setCurrentProgress(0);
        setMissileSource(null);
        setMissileTarget(null);
      }
    }, 30000);
  };

  // Start animation when engaging
  if (isEngaging && missileSource && missileTarget && currentProgress === 0) {
    startMissileAnimation();
  }

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <Map
        {...viewport}
        mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
        onMove={(evt: ViewStateChangeEvent) => setViewport(evt.viewState)}
        onClick={(e: MapLayerMouseEvent) => {
          if (e.originalEvent && e.originalEvent.type === 'click') {
            setSelectedEnemy(null);
            setNearestFriendlyId(null);
          }
        }}
      >
        {/* Friendly Markers - Green */}
        {assets.map((asset) => (
          <div
            key={asset.id}
            onClick={(e) => {
              e.stopPropagation();
              if (selectedEnemy && !isEngaging && nearestFriendlyId) {
                startEngagement();
              }
            }}
            style={{
              position: 'absolute',
              left: `calc(50% + ((${asset.lon} - ${center[0]}) * ${zoom} * 1000))`,
              top: `calc(50% - ((${asset.lat} - ${center[1]}) * ${zoom} * 1000))`,
              width: '24px',
              height: '24px',
              borderRadius: '50%',
              backgroundColor: '#4caf50',
              border: '2px solid #1b5e20',
              boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transform: 'translate(-50%, -50%)',
              transition: 'all 0.2s',
            }}
            title={`${asset.name} - Friendly`}
          >
            <div style={{
              width: '10px',
              height: '10px',
              backgroundColor: 'white',
              borderRadius: '50%'
            }} />
          </div>
        ))}

        {/* Enemy Markers - Red */}
        {enemyAssets.map((asset) => (
          <div
            key={asset.id}
            onClick={(e) => {
              e.stopPropagation();
              handleEnemyClick(asset);
            }}
            style={{
              position: 'absolute',
              left: `calc(50% + ((${asset.lon} - ${center[0]}) * ${zoom} * 1000))`,
              top: `calc(50% - ((${asset.lat} - ${center[1]}) * ${zoom} * 1000))`,
              width: '24px',
              height: '24px',
              borderRadius: '50%',
              backgroundColor: '#f44336',
              border: '2px solid #b71c1c',
              boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transform: 'translate(-50%, -50%)',
              transition: 'all 0.2s',
            }}
            title={`${asset.name} - Enemy`}
          >
            <div style={{
              width: '14px',
              height: '4px',
              backgroundColor: 'white',
              transform: 'rotate(45deg)'
            }} />
          </div>
        ))}

        {/* Engagement Line */}
        {missileSource && missileTarget && (
          <div
            style={{
              position: 'absolute',
              top: '0',
              left: '0',
              width: '100%',
              height: '100%',
              pointerEvents: 'none',
            }}
          >
            <svg
              style={{
                width: '100%',
                height: '100%',
                position: 'absolute',
                top: '0',
                left: '0',
              }}
            >
              <line
                x1={`${((missileSource.lon - center[0]) * zoom * 1000) + 50}%`}
                y1={`${50 - ((missileSource.lat - center[1]) * zoom * 1000)}%`}
                x2={`${((missileTarget.lon - center[0]) * zoom * 1000) + 50}%`}
                y2={`${50 - ((missileTarget.lat - center[1]) * zoom * 1000)}%`}
                stroke="rgba(255, 215, 0, 0.8)"
                strokeWidth="3"
              />
            </svg>
          </div>
        )}

        {/* Missile Animation */}
        {missileSource && missileTarget && (
          <div
            key="missile"
            style={{
              position: 'absolute',
              left: `${50 + ((missileSource.lon + (missileTarget.lon - missileSource.lon) * (currentProgress / 100) - center[0]) * zoom * 1000)}%`,
              top: `${50 - ((missileSource.lat + (missileTarget.lat - missileSource.lat) * (currentProgress / 100) - center[1]) * zoom * 1000)}%`,
              width: '20px',
              height: '20px',
              borderRadius: '50%',
              backgroundColor: '#ffeb3b',
              border: '2px solid #fbc02d',
              boxShadow: '0 0 10px rgba(255, 235, 59, 0.8)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transform: 'translate(-50%, -50%)',
              transition: 'all 0.2s',
            }}
            title={`Missile ${currentProgress}%`}
          >
            <div style={{
              width: '10px',
              height: '10px',
              backgroundColor: 'orange',
              borderRadius: '50%'
            }} />
          </div>
        )}
      </Map>

      {/* Engagement Panel */}
      {isEngaging && (
        <div style={{
          position: 'absolute',
          top: '20px',
          right: '20px',
          width: '320px',
          backgroundColor: 'rgba(0, 0, 0, 0.9)',
          borderRadius: '8px',
          padding: '20px',
          color: 'white',
          zIndex: 1000,
        }}>
          <h3 style={{ margin: '0 0 15px', fontSize: '18px' }}>
            🎯 Missile Engagement
          </h3>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>
              Select Friendly Asset:
            </label>
            <select
              value={nearestFriendlyId || ''}
              onChange={(e) => {
                const asset = friendlyAssets.find(a => a.id === e.target.value);
                if (asset && selectedEnemy) {
                  setMissileSource({ lat: asset.lat, lon: asset.lon });
                  setMissileTarget({ lat: selectedEnemy.lat, lon: selectedEnemy.lon });
                  setNearestFriendlyId(asset.id);
                }
              }}
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '4px',
                border: '1px solid #444',
                backgroundColor: '#222',
                color: 'white',
                fontSize: '14px',
              }}
            >
              <option value="">-- Select Friendly --</option>
              {friendlyAssets.map(asset => (
                <option key={asset.id} value={asset.id}>
                  {asset.name} ({asset.asset_type})
                </option>
              ))}
            </select>
          </div>

          <div style={{ backgroundColor: 'rgba(76, 175, 80, 0.1)', borderRadius: '6px', padding: '15px', marginBottom: '15px' }}>
            <h4 style={{ margin: '0 0 10px', fontSize: '14px' }}>
              🚀 Missile In Flight
            </h4>
            
            <div style={{ marginBottom: '10px' }}>
              <div style={{ 
                width: '100%', 
                height: '8px', 
                backgroundColor: '#333',
                borderRadius: '4px',
                overflow: 'hidden',
              }}>
                <div style={{
                  width: `${currentProgress}%`,
                  height: '100%',
                  backgroundColor: '#ffeb3b',
                  transition: 'width 0.2s ease',
                }} />
              </div>
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between',
                fontSize: '12px',
                marginTop: '5px',
              }}>
                <span>Progress</span>
                <span>{currentProgress}%</span>
              </div>
            </div>

            <div style={{ fontSize: '12px', color: '#888' }}>
              <p style={{ margin: '2px 0' }}>
                From: {missileSource?.lat.toFixed(4)}, {missileSource?.lon.toFixed(4)}
              </p>
              <p style={{ margin: '2px 0' }}>
                To: {missileTarget?.lat.toFixed(4)}, {missileTarget?.lon.toFixed(4)}
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              onClick={handleCancelEngagement}
              style={{
                flex: 1,
                padding: '12px',
                borderRadius: '6px',
                border: 'none',
                backgroundColor: '#f44336',
                color: 'white',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 'bold',
              }}
            >
              Cancel
            </button>
            <button
              onClick={startEngagement}
              style={{
                flex: 1,
                padding: '12px',
                borderRadius: '6px',
                border: 'none',
                backgroundColor: '#4caf50',
                color: 'white',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 'bold',
              }}
            >
              Launch
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
