-- PostgreSQL schema for Command & Control system.
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Devices table
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) NOT NULL CHECK (device_type IN ('drone', 'sensor', 'camera', 'vehicle')),
    status VARCHAR(20) NOT NULL DEFAULT 'online' CHECK (status IN ('online', 'offline', 'maintenance')),
    location_lat FLOAT,
    location_lon FLOAT,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    extra_data JSONB DEFAULT '{}',
    zone VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Locations table
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    location_lat FLOAT NOT NULL,
    location_lon FLOAT NOT NULL,
    area_type VARCHAR(20) CHECK (area_type IN ('urban', 'suburban', 'industrial')),
    zone VARCHAR(50),
    extra_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    location_id UUID REFERENCES locations(id) ON DELETE SET NULL,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('alert', 'status_change', 'command_ack')),
    details JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    severity VARCHAR(20) CHECK (severity IN ('info', 'warning', 'critical')),
    resolved VARCHAR(20) DEFAULT 'pending' CHECK (resolved IN ('pending', 'resolved', 'ignored')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Commands table
CREATE TABLE commands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL,
    location_id UUID REFERENCES locations(id) ON DELETE SET NULL,
    command_type VARCHAR(50) NOT NULL CHECK (command_type IN ('patrol', 'survey', 'return', 'stop', 'resume')),
    payload JSONB DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'acknowledged', 'failed')),
    error_message VARCHAR(255),
    acknowledged_at TIMESTAMP,
    failed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX idx_devices_zone ON devices(zone);
CREATE INDEX idx_devices_status ON devices(status);
CREATE INDEX idx_devices_location ON devices(location_lat, location_lon);
CREATE INDEX idx_locations_zone ON locations(zone);
CREATE INDEX idx_events_device ON events(device_id);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_commands_status ON commands(status);
CREATE INDEX idx_commands_device ON commands(device_id);

-- Update updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables
CREATE TRIGGER update_devices_updated_at
    BEFORE UPDATE ON devices
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_locations_updated_at
    BEFORE UPDATE ON locations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_commands_updated_at
    BEFORE UPDATE ON commands
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
