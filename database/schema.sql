-- MediBridge AI -- PostgreSQL schema
-- Run with: psql -U postgres -d medibridge -f database/schema.sql
-- (The FastAPI app also auto-creates these tables on startup in dev mode
--  via SQLAlchemy; use this file + Alembic migrations for production.)

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- PATIENTS
-- ============================================================
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    age INTEGER,
    gender VARCHAR(30),
    preferred_language VARCHAR(50) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SYMPTOMS
-- source: 'patient_reported' | 'document_supported' | 'physician_verified'
-- ============================================================
CREATE TABLE IF NOT EXISTS symptoms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,

    name VARCHAR(150),
    duration VARCHAR(100),
    severity VARCHAR(50),

    source VARCHAR(50) DEFAULT 'patient_reported',
    confidence FLOAT DEFAULT 0.6,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- CONVERSATIONS + MESSAGES
-- ============================================================
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,
    status VARCHAR(30) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversation_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20), -- 'patient' | 'ai'
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- REPORTS (uploaded documents / lab results)
-- ============================================================
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,

    filename VARCHAR(255),
    file_path TEXT,

    ocr_text TEXT,
    extracted_data JSONB,

    source VARCHAR(50) DEFAULT 'document_supported',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- MEDICATIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS medications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,

    name VARCHAR(200),
    dosage VARCHAR(100),
    frequency VARCHAR(100),

    source VARCHAR(50) DEFAULT 'patient_reported',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- MEDICAL HISTORY (past conditions, surgeries, allergies, family history)
-- ============================================================
CREATE TABLE IF NOT EXISTS medical_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,

    category VARCHAR(100), -- 'condition' | 'surgery' | 'allergy' | 'family_history'
    description TEXT,

    source VARCHAR(50) DEFAULT 'patient_reported',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ALERTS (red-flag hits surfaced to clinicians)
-- ============================================================
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,

    rule_id VARCHAR(50),
    name VARCHAR(255),
    priority VARCHAR(20) DEFAULT 'routine', -- 'routine' | 'urgent'
    message TEXT,
    acknowledged BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- VERIFICATION RECORDS
-- Tracks the three-layer verification lifecycle for any piece of
-- information: patient_reported -> document_supported -> physician_verified
-- ============================================================
CREATE TABLE IF NOT EXISTS verification_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,

    information_type VARCHAR(100), -- 'symptom' | 'report_finding' | 'medication' | 'medical_history'
    information_id UUID,

    status VARCHAR(50) DEFAULT 'patient_reported',

    verified_by UUID,
    verified_at TIMESTAMP
);

-- ============================================================
-- DOCTORS (minimal auth table for the prototype)
-- ============================================================
CREATE TABLE IF NOT EXISTS doctors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    specialty VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Indexes
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_symptoms_patient_id ON symptoms(patient_id);
CREATE INDEX IF NOT EXISTS idx_reports_patient_id ON reports(patient_id);
CREATE INDEX IF NOT EXISTS idx_alerts_patient_id ON alerts(patient_id);
CREATE INDEX IF NOT EXISTS idx_alerts_acknowledged ON alerts(acknowledged);
CREATE INDEX IF NOT EXISTS idx_conversations_patient_id ON conversations(patient_id);
CREATE INDEX IF NOT EXISTS idx_conversation_messages_conversation_id ON conversation_messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_verification_records_patient_id ON verification_records(patient_id);
