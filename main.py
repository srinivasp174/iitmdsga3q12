from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = ""):
    try:
        q_lower = q.lower()

        # ---------------------------------------
        # 1) Ticket Status
        # ---------------------------------------
        ticket_match = re.search(r"ticket\s+(\d+)", q_lower)
        if ticket_match and "status" in q_lower:
            ticket_id = int(ticket_match.group(1))
            return {
                "name": "get_ticket_status",
                "arguments": json.dumps({
                    "ticket_id": ticket_id
                })
            }

        # ---------------------------------------
        # 2) Schedule Meeting (Flexible)
        # Supports:
        # - schedule meeting on YYYY-MM-DD at HH:MM in Room
        # - set meeting for YYYY-MM-DD, HH:MM at Room
        # ---------------------------------------
        meeting_match = re.search(
            r"(schedule|set).*?(\d{4}-\d{2}-\d{2})[, ]+\s*(\d{2}:\d{2}).*?(?:in|at)\s+(.+)",
            q,
            re.IGNORECASE
        )

        if meeting_match:
            date = meeting_match.group(2)
            time = meeting_match.group(3)
            meeting_room = meeting_match.group(4).strip().rstrip(".")

            return {
                "name": "schedule_meeting",
                "arguments": json.dumps({
                    "date": date,
                    "time": time,
                    "meeting_room": meeting_room
                })
            }

        # ---------------------------------------
        # 3) Expense Balance
        # ---------------------------------------
        expense_match = re.search(r"employee\s+(\d+)", q_lower)
        if expense_match and "expense" in q_lower:
            employee_id = int(expense_match.group(1))
            return {
                "name": "get_expense_balance",
                "arguments": json.dumps({
                    "employee_id": employee_id
                })
            }

        # ---------------------------------------
        # 4) Performance Bonus
        # ---------------------------------------
        bonus_match = re.search(
            r"employee\s+(\d+).*?(\d{4})",
            q_lower
        )
        if bonus_match and "bonus" in q_lower:
            employee_id = int(bonus_match.group(1))
            current_year = int(bonus_match.group(2))

            return {
                "name": "calculate_performance_bonus",
                "arguments": json.dumps({
                    "employee_id": employee_id,
                    "current_year": current_year
                })
            }

        # ---------------------------------------
        # 5) Office Issue
        # ---------------------------------------
        issue_match = re.search(r"issue\s+(\d+)", q_lower)
        dept_match = re.search(
            r"(?:for|to)\s+(?:the\s+)?(.+?)\s+department",
            q,
            re.IGNORECASE
        )

        if issue_match and dept_match:
            issue_code = int(issue_match.group(1))
            department = dept_match.group(1).strip()

            return {
                "name": "report_office_issue",
                "arguments": json.dumps({
                    "issue_code": issue_code,
                    "department": department
                })
            }

        # ---------------------------------------
        # Default fallback (always valid JSON)
        # ---------------------------------------
        return {
            "name": "unknown",
            "arguments": json.dumps({})
        }

    except Exception:
        # Never return HTML errors
        return JSONResponse(
            content={
                "name": "error",
                "arguments": json.dumps({})
            }
        )
