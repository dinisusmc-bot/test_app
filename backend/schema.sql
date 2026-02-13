-- PostgreSQL schema for GeoMap simulation with Assets and Engagements.
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Assets table (friendly and enemy icons)
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(50) NOT NULL CHECK (asset_type IN ('drone', 'sensor', 'camera', 'vehicle')),
    status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'in_use', 'maintenance', 'offline')),
    lat FLOAT,
    lon FLOAT,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    extra_data JSONB DEFAULT '{}',
    zone VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    is_friendly BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Engagements table (missile tracking)
CREATE TABLE engagements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    friendly_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    enemy_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'completed', 'cancelled')),
    progress FLOAT DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    estimated_completion TIMESTAMP,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    engagement_id UUID REFERENCES engagements(id) ON DELETE SET NULL,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('alert', 'status_change', 'command_ack', 'engagement_start', 'engagement_end')),
    details JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    severity VARCHAR(20) CHECK (severity IN ('info', 'warning', 'critical')),
    resolved VARCHAR(20) DEFAULT 'pending' CHECK (resolved IN ('pending', 'resolved', 'ignored')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Commands table
CREATE TABLE commands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    engagement_id UUID REFERENCES engagements(id) ON DELETE SET NULL,
    command_type VARCHAR(50) NOT NULL CHECK (command_type IN ('patrol', 'survey', 'return', 'stop', 'resume', 'engage', 'disengage')),
    payload JSONB DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'acknowledged', 'failed')),
    error_message VARCHAR(255),
    acknowledged_at TIMESTAMP,
    failed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX idx_assets_zone ON assets(zone);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_assets_location ON assets(lat, lon);
CREATE INDEX idx_assets_friendly ON assets(is_friendly);
CREATE INDEX idx_engagements_status ON engagements(status);
CREATE INDEX idx_engagements_friendly ON engagements(friendly_id);
CREATE INDEX idx_engagements_enemy ON engagements(enemy_id);
CREATE INDEX idx_events_asset ON events(asset_id);
CREATE INDEX idx_events_engagement ON events(engagement_id);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_commands_status ON commands(status);
CREATE INDEX idx_commands_asset ON commands(asset_id);

-- Update updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables
CREATE TRIGGER update_assets_updated_at
    BEFORE UPDATE ON assets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_engagements_updated_at
    BEFORE UPDATE ON engagements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_commands_updated_at
    BEFORE UPDATE ON commands
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
