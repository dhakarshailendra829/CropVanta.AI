"""Simple authenticated API latency benchmark. Run API first; supply credentials via env."""
import os, statistics, time
import requests

BASE = os.getenv("CROPVANTA_API", "http://127.0.0.1:8000")
EMAIL = os.getenv("CROPVANTA_EMAIL", "")
PASSWORD = os.getenv("CROPVANTA_PASSWORD", "")
ITERATIONS = int(os.getenv("BENCHMARK_ITERATIONS", "50"))

if not EMAIL or not PASSWORD:
    raise SystemExit("Set CROPVANTA_EMAIL and CROPVANTA_PASSWORD for an existing test account.")
token_response = requests.post(f"{BASE}/auth/token", data={"username": EMAIL, "password": PASSWORD}, timeout=10)
token_response.raise_for_status()
headers = {"Authorization": f"Bearer {token_response.json()['access_token']}"}
payload = {"nitrogen": 90, "phosphorus": 42, "potassium": 43, "temperature": 20.8, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9}

# Warm-up request is excluded from the timing sample.
requests.post(f"{BASE}/predict", json=payload, headers=headers, timeout=30).raise_for_status()
samples = []
for _ in range(ITERATIONS):
    start = time.perf_counter()
    response = requests.post(f"{BASE}/predict", json=payload, headers=headers, timeout=30)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.raise_for_status()
    samples.append(elapsed_ms)
ordered = sorted(samples)
p95 = ordered[min(len(ordered)-1, int(0.95 * len(ordered)))]
print(f"Requests: {len(samples)}")
print(f"Mean: {statistics.mean(samples):.2f} ms")
print(f"Median/p50: {statistics.median(samples):.2f} ms")
print(f"p95: {p95:.2f} ms")
print("Note: this is local API latency; report deployment/network conditions with any resume metric.")
