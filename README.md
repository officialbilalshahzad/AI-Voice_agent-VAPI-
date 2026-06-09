🎙️ Vapi AI Voice Agent Backend
An AI-powered voice agent backend for managing hospital appointments, built with FastAPI, SQLAlchemy, and Streamlit. Designed to integrate with Vapi for conversational voice interactions, enabling patients to schedule, cancel, and list appointments via natural language.

✨ Features
Schedule Appointments — Book a new appointment with patient name, reason, and preferred time.

Cancel Appointments — Cancel all appointments for a patient on a given date.

List Appointments — View all active (non-canceled) appointments for a specific date.

Streamlit Dashboard — A simple web UI for manual testing.

SQLite Database — Lightweight, file-based persistence with zero configuration.

📂 Project Structure
Plaintext
├── backend.py          # FastAPI server with appointment endpoints
├── database.py         # SQLAlchemy models, engine, and session management
├── dummy_frontend.py   # Streamlit dashboard for testing
├── db_demo.py          # Utility script for raw SQL queries against the DB
├── pyproject.toml      # Project metadata and dependencies
└── README.md           # Project documentation
🚀 Getting Started
1. Clone the Repository
Bash
git clone <repo-url>
cd vapi-voice-agent
2. Create a Virtual Environment & Install Dependencies
Using uv (recommended):

Bash
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
uv sync
Or using traditional pip:

Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install fastapi sqlalchemy streamlit uvicorn requests
3. Start the FastAPI Backend
Bash
python backend.py
The API will be available locally at http://127.0.0.1:4444. You can view the interactive documentation at http://127.0.0.1:4444/docs.

4. Run the Network Tunnel (For Vapi Integration)
Since Vapi runs in the cloud, it needs a public URL to talk to your local backend. Open a new terminal and run:

Bash
ngrok http 4444
Copy the secure forwarding URL provided by ngrok (e.g., https://xxxx.ngrok-free.app).

5. Launch the Streamlit Dashboard (Optional Testing)
Bash
streamlit run dummy_frontend.py
🔌 Vapi Integration Setup
Open your Vapi Dashboard.

Go to your Assistant or Tools settings.

Paste your ngrok URL followed by the endpoint name into the Webhook/Server URL fields.

Example: https://your-ngrok-url.ngrok-free.app/schedule_appointment/

Configure the parameters to match the API inputs below.

📡 API Endpoints Summary
All endpoints accept JSON payloads via POST.

Schedule Appointment (/schedule_appointment/)

JSON
{
  "patient_name": "Hassan",
  "reason": "Annual checkup",
  "start_time": "2026-06-15T10:00:00"
}
Cancel Appointments (/cancel_appointment/)

JSON
{
  "patient_name": "Hassan",
  "date": "2026-06-15"
}
List Appointments (/list_appointments/)

JSON
{
  "date": "2026-06-15"
}
🗄️ Database Inspection
The project automatically initializes an SQLite file (appointments_db.db) on its first run. To inspect the database records directly via raw SQL queries, execute the helper script:
