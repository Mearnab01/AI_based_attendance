# SnapClass

**AI-Powered Attendance Management System**

---

## Overview

Manual attendance in classroom environments is slow, gameable, and operationally costly. SnapClass replaces that process entirely with a computer vision and voice recognition pipeline that identifies students from classroom photographs and audio recordings — no roll calls, no sign-in sheets.

Teachers upload group photos of their class or initiate a voice-based session. The system identifies enrolled students using face embeddings and voice embeddings stored per profile, marks attendance automatically, and logs the results against the correct subject and timestamp. Students authenticate into the platform using FaceID — a live camera scan matched against their stored embedding — eliminating password-based login entirely.

The system is built on Streamlit with a Supabase backend and is designed to be deployable as a single-command application on any standard cloud environment.

---

## Features

**Core Functionality**

- Face recognition login for students using live camera input matched against stored embeddings
- Batch AI attendance from one or more classroom photos per session, with per-photo source tracking
- Voice-based attendance as a secondary modality using audio embeddings
- Role-separated dashboards for teachers and students with independent authentication flows
- Subject management: teachers create, configure, and share subjects via generated codes
- Student enrollment via subject codes with unenroll support
- Full attendance history per subject with session-level aggregation (present count / total)

**Technical Features**

- Face embeddings and voice embeddings stored as JSONB in Supabase, decoupled from the classifier
- On-demand classifier retraining triggered post-registration to include new student data
- Multi-photo session support: detections across all uploaded images are merged before logging
- Attendance deduplication: a student detected in multiple photos within a session is marked present once
- Composite primary key junction table (`subject_students`) enforcing clean many-to-many enrollment
- Streamlit secrets management for zero-plaintext credential exposure in deployment
- Session state machine managing multi-step registration, login, and tab navigation

---

## Tech Stack

| Layer              | Technology                                                      |
| ------------------ | --------------------------------------------------------------- |
| Frontend / UI      | Streamlit, HTML/CSS via `st.markdown`                           |
| Database           | Supabase (PostgreSQL)                                           |
| Face Recognition   | Face embedding model via custom pipeline (`face_pipeline.py`)   |
| Voice Recognition  | Voice embedding model via custom pipeline (`voice_pipeline.py`) |
| Image Processing   | Pillow, NumPy                                                   |
| Data Handling      | Pandas                                                          |
| Environment Config | python-dotenv, Streamlit Secrets (`secrets.toml`)               |
| Fonts              | Google Fonts (Syne, DM Sans)                                    |

---

## Architecture and Flow

SnapClass is structured around two primary user roles — **Teacher** and **Student** — each with a dedicated screen and isolated session state.

**Authentication Layer**

- Teachers authenticate via username and hashed password stored in Supabase
- Students authenticate via live FaceID: a camera frame is processed through the face pipeline, and the detected embedding is matched against all stored student embeddings using the trained classifier
- On first visit, unrecognized students are routed to a registration flow where face and optional voice embeddings are captured, stored, and used to retrain the classifier in-session

**Attendance Pipeline**

1. Teacher selects a subject and uploads one or more classroom photos
2. Each photo is converted to a NumPy RGB array and passed to `predict_attendance()`
3. Detected student IDs are aggregated across all photos into a single dictionary keyed by student ID
4. The system queries all enrolled students for the selected subject from Supabase
5. Each enrolled student is marked present or absent based on detection results
6. Results are written to `attendance_logs` with a shared session timestamp
7. The result dialog surfaces a per-student breakdown before committing the log

**Voice Attendance**

An alternative path where enrolled students respond to a prompt; voice embeddings are matched against stored profiles and attendance is marked without any photo input.

**Data Flow Summary**

```
Camera / Photos
      |
      v
Face Pipeline (predict_attendance)
      |
      v
Detected Student IDs  <---  Supabase: subject_students (enrolled list)
      |
      v
Attendance Results DataFrame
      |
      v
Supabase: attendance_logs (INSERT)
```

---

## Folder Structure

```
snapclass/
|
|- app.py                        # Entry point, routes to home/teacher/student screen
|
|- .env                          # Local environment variables (never committed)
|- .env.example                  # Template for required environment variables
|- .gitignore
|- requirements.txt
|
|- .streamlit/
|   |- secrets.toml              # Streamlit deployment secrets (never committed)
|
|- src/
|   |
|   |- ui/
|   |   |- base_layout.py        # Global CSS, background theming, typography
|   |
|   |- components/
|   |   |- header.py             # header_home(), header_dashboard()
|   |   |- footer.py             # footer_home(), footer_dashboard()
|   |   |- subject_card.py       # Reusable subject card component
|   |   |- dialog_create_subject.py
|   |   |- dialog_share_subject.py
|   |   |- dialog_add_photo.py
|   |   |- dialog_attendance_results.py
|   |   |- dialog_voice_attendance.py
|   |   |- dialog_enroll.py
|   |
|   |- screens/
|   |   |- home_screen.py        # Landing page and role selection
|   |   |- teacher_screen.py     # Teacher auth, dashboard, tabs
|   |   |- student_screen.py     # Student FaceID login, dashboard
|   |
|   |- pipelines/
|   |   |- face_pipeline.py      # Embedding extraction, classifier training, prediction
|   |   |- voice_pipeline.py     # Voice embedding extraction and matching
|   |
|   |- database/
|       |- config.py             # Supabase client initialisation
|       |- db.py                 # All database query functions
```

---

## Setup Instructions

**Prerequisites**

- Python 3.10
- Conda (recommended) or any virtual environment manager
- A Supabase project with the schema described in the Database Schema section

> **Windows note:** Do not run `pip install -r requirements.txt` directly without following the steps below. The `resemblyzer` package has a hard dependency on `webrtcvad` which requires Microsoft C++ Build Tools to compile from source. The steps below route around this entirely using a prebuilt wheel.

---

**1. Clone the repository**

```bash
git clone https://github.com/your-username/snapclass.git
cd snapclass
```

**2. Create and activate a conda environment**

```bash
conda create -n snapclass python=3.10
conda activate snapclass
```

**3. Install the prebuilt webrtcvad wheel first**

This must be done before anything else. Installing it after will not prevent pip from trying to build the source version.

```bash
pip install webrtcvad-wheels --no-cache-dir
```

**4. Install resemblyzer without its dependencies**

`resemblyzer` declares `webrtcvad` as a dependency. The `--no-deps` flag prevents pip from pulling the source build version on top of the wheel you just installed.

```bash
pip install resemblyzer --no-deps
```

**5. Install the typing backport required by resemblyzer**

```bash
pip install typing
```

**6. Install the remaining dependencies**

```bash
pip install -r requirements.txt
```

**7. Verify the installation**

```bash
python -c "import resemblyzer; import webrtcvad; import supabase; print('all good')"
```

The output should be `all good`. If any import fails, check that Steps 3 and 4 completed without errors.

**8. Configure environment variables**

```bash
cp .env.example .env
```

Open `.env` and fill in your Supabase project URL and anon key. See the Environment Variables section below.

**9. Configure Streamlit secrets (for deployment or local parity)**

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

**10. Run the application**

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

---

## Environment Variables

The following variables are required. Copy `.env.example` to `.env` and populate each value.

```env
# .env.example

# Supabase project URL — found in your Supabase project settings under API
SUPABASE_URL=https://your-project-ref.supabase.co

# Supabase anon/public key — used for client-side database access
SUPABASE_KEY=your-supabase-anon-key
```

In local development, these are loaded via `python-dotenv`. In Streamlit Cloud deployment, the equivalent values are provided through `.streamlit/secrets.toml` and accessed via `st.secrets`, keeping credentials out of environment processes entirely.

---

## Database Schema

The application uses five tables in Supabase (PostgreSQL):

| Table              | Purpose                                                         |
| ------------------ | --------------------------------------------------------------- |
| `teachers`         | Teacher accounts with hashed credentials                        |
| `students`         | Student profiles with face and voice embeddings (JSONB)         |
| `subjects`         | Subjects owned by a teacher, with enrollment password           |
| `subject_students` | Junction table: many-to-many student-subject enrollment         |
| `attendance_logs`  | Per-session attendance records with timestamp and presence flag |

Row Level Security (RLS) policies should be configured in Supabase to restrict data access to authenticated contexts. The anon key used in this application is scoped to read/write operations only — no admin or service role key is exposed client-side.

---

## Security Considerations

- Credentials are never hardcoded. All secrets are loaded from `.env` locally and from `st.secrets` in deployment
- `.env` and `.streamlit/secrets.toml` are listed in `.gitignore` and must never be committed to version control
- The Supabase anon key used is scoped to the minimum required permissions. The service role key is not used anywhere in the application
- Student face and voice embeddings are stored as JSONB blobs — they are model-specific numerical vectors, not raw biometric images, and cannot be reverse-engineered into photographs
- Password fields in the `teachers` table should be stored as bcrypt hashes, not plaintext — ensure hashing is applied in `create_teacher()` before insertion
- For production deployment, Supabase RLS policies should be enabled and tested against all table operations

---

## Future Improvements

- **Liveness detection** — add anti-spoofing checks to the face login flow to prevent photo-based bypass attacks
- **Attendance analytics dashboard** — per-subject attendance trend charts, low-attendance alerts, and exportable CSV reports
- **Bulk student import** — allow teachers to import student rosters via CSV rather than individual registration
- **Mobile camera optimisation** — improve the camera input handling for low-light and wide-angle classroom scenarios
- **Notification system** — automated alerts to students when attendance drops below a configurable threshold
- **Admin role** — institution-level administrator account with cross-teacher visibility and audit logs
- **REST API layer** — decouple the ML pipelines behind a FastAPI service to enable integration with third-party LMS platforms
- **Progressive Web App (PWA)** — package the Streamlit frontend as an installable PWA for consistent mobile experience

---

## Author

Built by **Arnab**.

---

_SnapClass is an independent project. All rights reserved._
