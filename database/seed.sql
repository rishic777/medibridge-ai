-- Demo data for local development / presentations.
-- Run with: psql -U postgres -d medibridge -f database/seed.sql

INSERT INTO patients (id, name, age, gender, preferred_language)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'Rishi Kumar', 21, 'male', 'en'),
    ('22222222-2222-2222-2222-222222222222', 'Ananya Iyer', 34, 'female', 'hi')
ON CONFLICT (id) DO NOTHING;

INSERT INTO symptoms (patient_id, name, duration, severity, source, confidence)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'fever', '3 days', 'moderate', 'patient_reported', 0.7),
    ('11111111-1111-1111-1111-111111111111', 'body pain', '2 days', 'mild', 'patient_reported', 0.6),
    ('22222222-2222-2222-2222-222222222222', 'chest pain', '1 day', 'severe', 'patient_reported', 0.8),
    ('22222222-2222-2222-2222-222222222222', 'breathing difficulty', '1 day', 'moderate', 'patient_reported', 0.75);

INSERT INTO alerts (patient_id, rule_id, name, priority, message)
VALUES
    (
        '22222222-2222-2222-2222-222222222222',
        'RF001',
        'Chest pain with breathing difficulty',
        'urgent',
        'Potentially urgent symptoms detected. Please seek immediate clinical assessment.'
    );

INSERT INTO doctors (name, email, hashed_password, specialty)
VALUES
    ('Dr. Sharma', 'sharma@medibridge.demo', 'CHANGE_ME_HASH', 'General Medicine')
ON CONFLICT (email) DO NOTHING;
