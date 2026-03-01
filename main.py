from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re
import json

app = FastAPI()

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

        # -----------------------------
        # 1) Ticket Status
        # -----------------------------
        ticket_match = re.search(r"ticket\s+(\d+)", q_lower)
        if ticket_match:
            return {
                "name": "get_ticket_status",
                "arguments": json.dumps({
                    "ticket_id": int(ticket_match.group(1))
                })
            }

        # -----------------------------
        # 2) Schedule Meeting
        # Detect date + time + room
        # -----------------------------
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", q)
        time_match = re.search(r"\d{2}:\d{2}", q)

        # capture last words as meeting room after "at" or "in"
        room_match = re.search(r"(?:at|in)\s+(.+)", q, re.IGNORECASE)

        if date_match and time_match and room_match:
            return {
                "name": "schedule_meeting",
                "arguments": json.dumps({
                    "date": date_match.group(0),
                    "time": time_match.group(0),
                    "meeting_room": room_match.group(1).strip().rstrip(".")
                })
            }

        # -----------------------------
        # 3) Expense Balance
        # -----------------------------
        if "expense" in q_lower:
            emp_match = re.search(r"employee\s+(\d+)", q_lower)
            if emp_match:
                return {
                    "name": "get_expense_balance",
                    "arguments": json.dumps({
                        "employee_id": int(emp_match.group(1))
                    })
                }

        # -----------------------------
        # 4) Performance Bonus
        # -----------------------------
        if "bonus" in q_lower:
            emp_match = re.search(r"employee\s+(\d+)", q_lower)
            year_match = re.search(r"\b(20\d{2})\b", q_lower)

            if emp_match and year_match:
                return {
                    "name": "calculate_performance_bonus",
                    "arguments": json.dumps({
                        "employee_id": int(emp_match.group(1)),
                        "current_year": int(year_match.group(1))
                    })
                }

        # -----------------------------
        # 5) Office Issue
        # -----------------------------
        issue_match = re.search(r"issue\s+(\d+)", q_lower)
        dept_match = re.search(r"(?:for|to)\s+(?:the\s+)?(.+?)\s+department", q, re.IGNORECASE)

        if issue_match and dept_match:
            return {
                "name": "report_office_issue",
                "arguments": json.dumps({
                    "issue_code": int(issue_match.group(1)),
                    "department": dept_match.group(1).strip()
                })
            }

        # Always return valid JSON
        return {
            "name": "unknown",
            "arguments": json.dumps({})
        }

    except Exception:
        return JSONResponse(
            content={
                "name": "error",
                "arguments": json.dumps({})
            }
        )
