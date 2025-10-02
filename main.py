import csv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI()

# Enable CORS to allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["GET"],  # We're only using GET
    allow_headers=["*"],
)

# Load CSV data into memory once (adjust the filename if needed)
STUDENTS_CSV = "student.csv"
students_data: List[Dict[str, str | int]] = []

with open(STUDENTS_CSV, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Convert studentId to int for cleaner JSON output
        row["studentId"] = int(row["studentId"])
        students_data.append(row)

@app.get("/api")
async def get_students(request: Request):
    # Get all `class` query parameters (multiple allowed)
    classes = request.query_params.getlist("class")

    # If no class filtering was specified, return all
    if not classes:
        return {"students": students_data}

    # Filter by classes, preserving CSV order
    filtered = [
        student for student in students_data
        if student["class"] in classes
    ]
    return {"students": filtered}

@app.get("/")
async def root():
    return {"message": "FastAPI is running. Try /api"}
