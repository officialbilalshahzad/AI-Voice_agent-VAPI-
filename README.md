🎙️ Production-Grade AI Voice Support & Hospital Appointment AgentAn asynchronous Python backend engineering framework designed to power low-latency conversational voice agents. This application couples a FastAPI microservice layer with a SQLAlchemy 2.0 ORM database engine to handle live hospital appointment data.Engineered specifically as a webhook and function-calling provider for enterprise voice pipelines like Vapi, the system translates real-time, natural language audio streams into validated transactional database mutations (INSERT, UPDATE, SELECT) over a secure network tunnel.🏗️ Technical Architecture & Network MatrixThe application decouples functional concerns across an event-driven network topology:Voice Telephony Gateway (Vapi): Orchestrates live analog stream handling, real-time Speech-to-Text (STT) parsing, and Text-to-Speech (TTS) response synthesis.Network Edge Tunneling (ngrok): Exposes an encrypted public gateway (https://*.ngrok-free.app) to route remote cloud webhooks and tool calls into the local development environment safely.Core Service Layer (FastAPI Engine): Executes non-blocking ASGI routing logic, strict data contract parsing, and conditional runtime validations.Persistence Layer (SQLAlchemy ORM): Manages connection pooling, transaction lifecycles, and relational mappings directly against an optimized local SQLite instance.Plaintext  ┌────────────────┐           Inbound Audio Stream          ┌────────────────┐
  │  Patient Phone │ ──────────────────────────────────────> │  Vapi Gateway  │
  │ (User Telephony)│ <────────────────────────────────────── │  (STT/LLM/TTS) │
  └────────────────┘            Synthesized Voice            └────────────────┘
                                                                     │
                                                            Secure Public Webhook URL
                                                                     ▼
                                                             ┌────────────────┐
                                                             │  ngrok Tunnel  │
                                                             └────────────────┘
                                                                     │
                                                            Local Loopback (Port 4444)
                                                                     ▼
┌──────────────────┐       SQLAlchemy Object Mapping       ┌────────────────┐
│ SQLite Database  │ <──────────────────────────────────── │ FastAPI Engine │
│(appointments.db) │                                       │  (backend.py)  │
└──────────────────┘                                       └────────────────┘
✨ Enterprise-Grade FeaturesSub-Second Tool Execution: Optimized API interfaces engineered to integrate flawlessly with Vapi’s dynamic function-calling environment.Asynchronous Execution Block: Built entirely on modern Python ASGI architecture to guarantee concurrent transaction processing.Strict Type Assertions: Leverages Pydantic data validation schemas to filter out corrupted payloads and enforce structural compliance.Deterministic Single-Day Bounds: Implements robust temporal boundary filtering using datetime.combine(date, time.min) to enforce explicit [start_dt, end_dt) evaluation, completely neutralizing multi-day date leakage bugs.Interactive Inspection Suite: Includes an integrated Streamlit frontend for isolated integration testing and a decoupled database engine script (db_demo.py) for raw transactional logging.📂 Project Directory ArchitecturePlaintext├── backend.py          # FastAPI service layer containing structural schemas, endpoints, and routers
├── database.py         # ORM mapping models, database connection setups, and session generators
├── dummy_frontend.py   # Interactive Streamlit dashboard for end-to-end component testing
├── db_demo.py          # Decoupled utility script for executing raw database diagnostics
├── pyproject.toml      # Modern dependency specification and project package metadata
└── README.md           # Production system documentation (This file)
🛠️ API Contracts & Specifications1. Schedule AppointmentEndpoint: POST /schedule_appointment/Description: Persists a newly booked slot into the relational database ledger.FieldTypeDescriptionpatient_namestringAbsolute legal name of the patient.reasonstringClinical reason/symptom descriptive context.start_timestringExplicit ISO 8601 string payload (e.g., 2026-06-15T14:30:00).Example Request Payload:JSON{
  "patient_name": "M Bilal Shahzad",
  "reason": "Routine clinical diagnostics and healthcare checkup",
  "start_time": "2026-06-15T14:30:00"
}
2. Cancel Day AppointmentsEndpoint: POST /cancel_appointment/Description: Soft-cancels active appointments matching the patient name within single-day bounds.FieldTypeDescriptionpatient_namestringTarget patient identity match parameters.datestringTarget date formatting string (ISO 8601, e.g., 2026-06-15).3. List Daily ScheduleEndpoint: POST /list_appointments/Description: Exposes active schedules chronologically sorted for a defined target block.FieldTypeDescriptiondatestringSpecific single-day querying bound (ISO 8601, e.g., 2026-06-15).🗄️ Database Relational SchemaAppointment Table PropertiesThe schema leverages an auto-managed file-based SQLite structure (appointments_db.db) spawned instantly at startup.Column NameData TypeKey ConstraintsFunctional DescriptionidIntegerPrimary Key (Auto-Increment)Internal tracking index field.patient_nameStringNot NullPatient classification label.reasonStringNullableMedical visit brief metadata context.start_timeDateTimeNot NullScheduled execution timestamp context.canceledBooleanDefault: FalseSoft-deletion flag indicator.created_atDateTimeDefault: func.now()Record instantiation auditing timestamp.⚙️ Installation & Deployment MatrixPrerequisitesPython 3.11+uv (High-performance dependency manager) or traditional pipStep 1: Environment SetupClone this repository workspace and instantiate virtual isolation spaces:Bashgit clone <repo-url>
cd vapi-voice-agent

# Using uv (Highly Recommended for lightning-fast speeds):
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# Alternatively, using native pip:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install fastapi sqlalchemy streamlit uvicorn requests
Step 2: Spin Up the FastAPI Microservice EngineExecute the main server thread to deploy application schemas and begin listening to internal loops:Bashpython backend.py
The engine initializes immediately on http://127.0.0.1:4444. Verify operational capabilities by launching the native OpenAPI schema suite directly at http://127.0.0.1:4444/docs.Step 3: Instantiate Network Edge Tunneling (ngrok)To bridge external cloud infrastructure (Vapi) down to your local machine, open a secondary, independent terminal space and run:Bashngrok http 4444
ngrok will output a secure public-facing URI (e.g., https://xyz123.ngrok-free.app). Copy this base URL.Step 4: Configure the External Vapi InterfaceNavigate to your cloud-managed Vapi Dashboard.Within your Assistant Tools Setup, declare your explicit tool integrations (schedule_appointment, cancel_appointment, list_appointments).Set your Webhook Server URL using the active ngrok tunnel address:Target Path: https://your-ngrok-url.ngrok-free.app/schedule_appointment/Trigger a live cellular voice evaluation to monitor natural language payload processing.
