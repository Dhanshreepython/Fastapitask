from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

class AssignmentNotification(BaseModel):
    recipient: str
    assignment_link: str
    deadline: datetime

assignments = {}

@app.post("/send-assignment/")
def send_assignment(notification: AssignmentNotification):
    assignments[notification.recipient] = {
        "link": notification.assignment_link,
        "deadline": notification.deadline,
        "status": "Pending"
    }
    return {"message": f"Assignment sent to {notification.recipient}. Complete it by {notification.deadline}"}

@app.get("/check-status/{recipient}")
def check_status(recipient: str):
    if recipient in assignments:
        return {"recipient": recipient, "status": assignments[recipient]}
    return {"message": "No assignment found for this recipient."}

@app.post("/submit-assignment/{recipient}")
def submit_assignment(recipient: str):
    if recipient in assignments:
        assignments[recipient]["status"] = "Submitted"
        return {"message": f"Assignment submitted by {recipient}."}
    return {"message": "No assignment found to submit."}
