import { useState, useRef, useEffect } from 'react';
import Map, { Source, Layer } from 'react-map-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface MapContainerProps {
  center?: [number, number];
  zoom?: number;
}

export default function MapContainer({ center = [-118.2437, 34.0522], zoom = 10 }: MapContainerProps) {
  const [viewport, setViewport] = useState({
    latitude: center[1],
    longitude: center[0],
    zoom: zoom,
  });

  return (
    <Map
      {...viewport}
      width="100%"
      height="400px"
      style={{ width: '100%', height: '400px' }}
      mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
      onMove={(evt) => setViewport(evt.viewState)}
    >
      <Source id="points" type="geojson" data={{
        type: 'FeatureCollection',
        features: []
      }}>
        <Layer
          id="points"
          type="circle"
          paint={{ 'circle-radius': 8, 'circle-color': '#007cbf' }}
        />
      </Source>
    </Map>
  );
}
