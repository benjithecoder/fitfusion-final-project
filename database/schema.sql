-- Drop tables if they already exist 
DROP TABLE IF EXISTS workout_logs;

DROP TABLE IF EXISTS exercises;

DROP TABLE IF EXISTS users;

--user table
CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

--exercises table (on row per exercise type)
CREATE TABLE
    exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT NOT NULL UNIQUE, -- eg. 'back_squat' this is for the computer 
        name TEXT NOT NULL, -- eg. 'Back Squat' this is for the human who reads it
        muscle_group TEXT NOT NULL -- eg. 'legs' This tells you what category the exercise belongs to:legs, chest , back,...
    );

--workout logs table (one row per logged set group)
CREATE TABLE
    workout_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- Each new log entry gets its own unique ID. like log 1 will get id = 1 , log nr 2 will get id = 2 etc 
        user_id INTEGER NOT NULL, -- who is the logged in user ? tom? anna ? carl ? 
        exercise_id INTEGER NOT NULL, -- This tells you which exercise the log belongs to.so ig squat = 1 and if the user is on the squat page, the log will always use: exercise_id = 1
        weight REAL NOT NULL, -- The type REAL means it can store decimal numbers too. like 80.2 kg
        reps INTEGER NOT NULL,
        sets_ INTEGER NOT NULL,
        logged_at DATE DEFAULT (DATE ('now')),
        FOREIGN KEY (user_id) REFERENCES user (id), -- ❌ You cannot insert a log for a user that doesn't exist
        FOREIGN KEY (exercise_id) REFERENCES exercises (id) -- ❌ You cannot insert a log for an exercise that doesn't exist
    );

--seed exercises (so i don't have to insert them manually later)
INSERT INTO
    exercises (slug, name, muscle_group)
VALUES
    ('back_squat', 'Back Squat', 'Legs'),
    ('bench_press', 'Bench Press', 'Chest'),
    ('barbell_row', 'Barbell Row', 'Back'),
    ('bicep_curl', 'Bicep Curl', 'Arms'),
    ('shoulder_press', 'Shoulder Press', 'Shoulders'),
    ('tricep_extension', 'Tricep Extension', 'Triceps');

-- Before users can log: back squat / bench pres, ...the app must KNOW those exercises exist so we tell it here that those are the 6 exercises that exist
-- so back squat gets the id = 1 , bench press gets id= 2 , barbell row gets id=3 etc...