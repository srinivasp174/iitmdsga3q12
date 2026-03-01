from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)):
    
    # 1) Ticket Status
    ticket_match = re.search(r"ticket\s+(\d+)", q, re.IGNORECASE)
    if "status" in q.lower() and ticket_match:
        ticket_id = int(ticket_match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": ticket_id
            })
        }

    # 2) Schedule Meeting
    meeting_match = re.search(
        r"on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(.+)\.",
        q,
        re.IGNORECASE
    )
    if "schedule" in q.lower() and meeting_match:
        date = meeting_match.group(1)
        time = meeting_match.group(2)
        meeting_room = meeting_match.group(3)
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date,
                "time": time,
                "meeting_room": meeting_room
            })
        }

    # 3) Expense Balance
    expense_match = re.search(r"employee\s+(\d+)", q, re.IGNORECASE)
    if "expense" in q.lower() and expense_match:
        employee_id = int(expense_match.group(1))
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": employee_id
            })
        }

    # 4) Performance Bonus
    bonus_match = re.search(
        r"employee\s+(\d+).*?(\d{4})",
        q,
        re.IGNORECASE
    )
    if "bonus" in q.lower() and bonus_match:
        employee_id = int(bonus_match.group(1))
        year = int(bonus_match.group(2))
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": employee_id,
                "current_year": year
            })
        }

    # 5) Office Issue
    issue_match = re.search(
        r"issue\s+(\d+).*?department",
        q,
        re.IGNORECASE
    )
    dept_match = re.search(
        r"for\s+the\s+(.+)\s+department",
        q,
        re.IGNORECASE
    )

    if "report" in q.lower() and issue_match and dept_match:
        issue_code = int(issue_match.group(1))
        department = dept_match.group(1)
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": issue_code,
                "department": department
            })
        }

    return {"error": "Query not recognized"}