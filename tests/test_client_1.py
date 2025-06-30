import requests
from datetime import datetime, timedelta
import time
import random

# API's URL
BASE_URL = "http://localhost:8000"

endpoints = []
today = datetime.now()

for i in range(20):
    last_access = today - timedelta(days=random.randint(0, 365))
    space_quota = random.choice([100, 256, 512, 1024])
    usage_percentage = random.uniform(0, 1.5)
    space_used = int(space_quota * usage_percentage)

    endpoint = {
        "endpoint_identifier": f"endpoint-{i}",
        "space_quota": space_quota,
        "space_used": space_used,
        "associated_email": f"team{i}@email.com",
        "last_access": last_access.isoformat()
    }
    endpoints.append(endpoint)

# Time recording
start_time = time.time()
total_requests = 0

for rule_id in [1, 2, 3, 4, 5]:  # Rules ID
    print(f"\n--- Testing Rule ID: {rule_id} ---\n")
    for ep in endpoints:
        response = requests.post(f"{BASE_URL}/evaluate/{rule_id}", json=ep)

        total_requests += 1
        try:
            result = response.json()
        except Exception:
            result = f"Parsing Error: {response.text}"

        print(f"Endpoint: {ep['endpoint_identifier']}")
        print("Result:", result)
        print()

end_time = time.time()
elapsed = end_time - start_time
avg = elapsed / total_requests if total_requests else 0

print("=== Performance Summary ===")
print(f"Total requests: {total_requests}")
print(f"Total time: {elapsed:.2f} seconds")
print(f"Avg per request: {avg:.4f} seconds")
