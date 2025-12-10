


 # FitFusion – Workout Logging & Exercise Guide Platform

# Video Demo: https://www.youtube.com/watch?v=DNhFKrgtGLo

# Description:

FitFusion is a web application built for CS50x 2025.  
It combines **exercise tutorials**, **real workout tracking**, and a clean UI.

The project teaches users how to perform exercises correctly while also allowing them to log their sets, weight, reps, and track progress across multiple exercises. Every user has their own account, and their data is stored securely in a SQLite database.

# Features

# User Authentication
- Users can register with an email + password  
- Passwords are securely hashed using Werkzeug  
- Login uses Flask sessions  
- A Logout button dynamically appears when logged in  
- All exercise pages require login (login-required protection)

# Workout Logging System
Each exercise page includes:
- A Log tab that allows users to:
  - Add new sets
  - Edit previous sets
  - Delete sets
- All logs are timestamped using SQLite defaults
- Logs are displayed in a clean table with:
  - Weight
  - Sets
  - Reps
  - Date
  - Action buttons (edit/delete)

# Three-Tab Exercise Layout
Each exercise page includes:
- **About** — explanation of the movement  
- **Guide** — step-by-step instructions  
- **Log** — workout tracking

Tabs switch using custom JavaScript, and the UI remembers the active tab after form submissions using URL hashes. This avoids page resets forcing users back into the About tab.


---

# Backend Implementation (Flask)

# Database
The SQLite database contains three tables:

- **users** — id, email, password_hash  
- **exercises** — id, slug, name, muscle group  
- **workout_logs** — id, user_id, exercise_id, weight, sets, reps, logged_at  

Every log entry is associated with both:
- A specific exercise
- A specific user

# Routes
Key Flask routes include:

- `/register` — account creation  
- `/login` — session creation  
- `/logout` — session removal  
- `/back-squat.html`, `/chest.html`, `/back.html`, etc.  
  - These display the exercise page  
  - Allow POST for logging/editing/deleting sets  
  - Load logs on every page visit  

Flask `"GET"` displays the page, while `"POST"` handles form submissions.

---

# Frontend Implementation

# HTML & Jinja
- Jinja loops display logs dynamically  
- Conditional logic (`{% if edit_log_id %}`) enables edit mode  
- Hidden forms send `delete_log_id`, `edit_log_id`, `update_log_id` to Flask

# CSS (style.css)
- Neon accents for tabs and buttons
- Responsive design for mobile

# JavaScript (main.js)
Controls:
- Tab switching
- Remembering active tab via `window.location.hash`
- Showing/hiding the correct content panels

---

# Design Choices and Rationale

# Why Flask + SQLite?
Simple, lightweight, and ideal for CS50 projects. No external services needed.

# Why hash-based tab memory?
POST requests reload the page. Without hash memory, the page always reverted to the About tab. Using URL hashes keeps the user experience smooth without complex logic.

# Why separate pages for each exercise?
Although I could have made one dynamic `/exercise/<slug>` route, I kept individual pages for clarity while learning. This also made debugging easier early in development. A refactor into a single dynamic route is possible for future improvement.

---

# Conclusion

FitFusion is a complete workout logging system with:
- User accounts  
- Editable logs  
- Multiple exercises  
- A polished UI  
- Full backend + frontend integration  

It represents everything I learned during CS50x:  
HTML, CSS, JavaScript, Python, Flask, SQLite, routing, sessions, hashing, GET/POST, templating, and debugging.

This project taught me how full-stack applications work from top to bottom.



