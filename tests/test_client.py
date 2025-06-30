import requests
from datetime import datetime

# API's URL
BASE_URL = "http://localhost:8000"

# Examples of endpoints
endpoints = [
    {
        "endpoint_identifier": "endpoint-0",
        "space_quota": 512,
        "space_used": 104,
        "associated_email": "team1@email.com",
        "last_access": "2025-05-01T00:00:00"
    },
    {
        "endpoint_identifier": "endpoint-1",
        "space_quota": 512,
        "space_used": 304,
        "associated_email": "team5@email.com",
        "last_access": "2025-03-11T00:00:00"
    },
    {
        "endpoint_identifier": "endpoint-2",
        "space_quota": 100,
        "space_used": 135,
        "associated_email": "team2@email.com",
        "last_access": "2024-08-12T00:00:00"
    },
    {
        "endpoint_identifier": "endpoint-3",
        "space_quota": 512,
        "space_used": 404,
        "associated_email": "team3@email.com",
        "last_access": "2024-12-25T00:00:00"
    },
    {
        "endpoint_identifier": "endpoint-4",
        "space_quota": 512,
        "space_used": 5,
        "associated_email": "team4@email.com",
        "last_access": "2025-02-28T00:00:00"
    }
]

for rule_id in [1, 2, 3, 4, 5]:  # rules ids
    print(f"\n--- Testing Rule ID: {rule_id} ---\n")
    for ep in endpoints:
        response = requests.post(f"{BASE_URL}/evaluate/{rule_id}", json=ep)
        print(f"Endpoint: {ep['endpoint_identifier']}")
        print("Result:", response.json())
        # print("Status code:", response.status_code)
        # print("Raw response:", response.text)
        print()
