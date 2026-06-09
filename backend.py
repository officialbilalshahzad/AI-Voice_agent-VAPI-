import datetime as dt
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
import uvicorn

# Step1: Import Database objects
from database import init_db, Appointment, get_db

init_db()

# Step3: Create Data Contracts using Pydantic Models
class AppointmentRequest(BaseModel):
    patient_name: str
    reason: str
    start_time: dt.datetime

class AppointmentResponse(BaseModel):
    id: int
    patient_name: str
    reason: str | None
    start_time: dt.datetime
    canceled: bool
    created_at: dt.datetime

    # This allows FastAPI to read SQLAlchemy models directly without manual conversion
    class Config:
        from_attributes = True

class CancelAppointmentRequest(BaseModel):
    patient_name: str
    date: dt.date

class CancelAppointmentResponse(BaseModel):
    canceled_count: int

class ListAppointmentRequest(BaseModel):
    date: dt.date

# Step2: Create FastAPI application
app = FastAPI()

# schedule appt
@app.post("/schedule_appointment/", response_model=AppointmentResponse)
def schedule_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
    new_appointment = Appointment(
        patient_name=request.patient_name,
        reason=request.reason,
        start_time=request.start_time,
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment  # FastAPI automatically converts this to AppointmentResponse

# cancel appt
@app.post("/cancel_appointment/", response_model=CancelAppointmentResponse)
def cancel_appointment(request: CancelAppointmentRequest, db: Session = Depends(get_db)):   
    start_dt = dt.datetime.combine(request.date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)

    result = db.execute(
        select(Appointment)
        .where(Appointment.patient_name == request.patient_name)
        .where(Appointment.start_time >= start_dt)
        .where(Appointment.start_time < end_dt)
        .where(Appointment.canceled == False)
    )

    appointments = result.scalars().all()
    if not appointments:
        
        raise HTTPException(status_code=404, detail="No matching appointment found in our system")

    for appointment in appointments:
        appointment.canceled = True
    
    db.commit()
    return CancelAppointmentResponse(canceled_count=len(appointments))

# list appt
@app.post("/list_appointments/", response_model=list[AppointmentResponse])
def list_appointments(request: ListAppointmentRequest, db: Session = Depends(get_db)):
    start_dt = dt.datetime.combine(request.date, dt.time.min)
    end_dt = start_dt + dt.timedelta(days=1)
    
    result = db.execute(
        select(Appointment)
        .where(Appointment.canceled == False)
        .where(Appointment.start_time >= start_dt)
        .where(Appointment.start_time < end_dt)
        .order_by(Appointment.start_time.asc())
    )
    
    
    appointments = result.scalars().all()
    return appointments

if __name__ == "__main__":

    uvicorn.run("backend:app", host="127.0.0.1", port=8501, reload=True)