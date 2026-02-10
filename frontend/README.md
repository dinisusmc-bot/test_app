# Command & Control Dashboard

React + TypeScript frontend with MapLibre GL JS for geospatial visualization of devices in LA and San Diego areas.

## Features

- **Interactive Map**: Real-time device tracking with MapLibre GL JS
- **Device List**: View all devices with status indicators (online/offline/maintenance)
- **Device Details**: Click devices on map or list to see details
- **Simulated Data**: 8 sample devices across LA and San Diego areas
- **Real-time Updates**: WebSocket integration for live status updates

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.tsx    # Main dashboard layout
│   │   │   └── DeviceList.tsx   # Device list component
│   │   ├── Map/
│   │   │   ├── MapContainer.tsx # Map container component
│   │   │   └── DeviceMarker.tsx # Device marker component
│   │   └── Device/
│   │       └── DeviceDetails.tsx # Device details panel
│   ├── services/
│   │   ├── api.ts               # API client with axios
│   │   └── websocket.ts         # WebSocket service
│   ├── App.tsx                  # Main app component
│   └── main.tsx                 # Entry point
├── public/
├── package.json
└── vite.config.ts
```

## API Integration

- **Backend URL**: `http://localhost:45847/api/v1`
- **WebSocket URL**: `ws://localhost:45847/ws`

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

The app will start on `http://localhost:5173`.

## Components

### Dashboard
Main layout with:
- Stats cards (total, online, offline, maintenance devices)
- Interactive map on the left
- Device list on the right
- Device details panel when selecting a device

### MapContainer
- Displays device markers on the map
- Click markers to see device info
- Shows popup with device details

### DeviceList
- Lists all devices with status badges
- Click to select device and show details

## Development

```bash
npm run dev        # Start dev server
npm run build      # Build for production
npm run preview    # Preview production build
npm run lint       # Run ESLint
```

## Technologies

- **React 18** with TypeScript
- **Vite** - Fast build tool and dev server
- **MapLibre GL JS** - Interactive maps
- **axios** - HTTP client
- **WebSocket API** - Real-time updates

## API Endpoints

### Devices
- `GET /api/v1/devices` - List all devices
- `GET /api/v1/devices/{id}` - Get device details

### Locations
- `GET /api/v1/locations` - List all locations

## Status Colors

- **Green (#4caf50)**: Online
- **Red (#f44336)**: Offline
- **Orange (#ff9800)**: Maintenance
