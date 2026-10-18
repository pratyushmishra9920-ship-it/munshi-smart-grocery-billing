
import json
import time
import urllib.request

url = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen3.5:4b",
    "prompt": "Reply only OK",
    "stream": False,
    "think": False,
    "options": {
        "num_predict": 5,
        "temperature": 0,
    },
    "keep_alive": "5m",
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    start = time.perf_counter()

    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.loads(response.read().decode("utf-8"))

    print("Ollama API connection successful!")
    print("Response:", result.get("response", ""))
    print(f"Time taken: {time.perf_counter() - start:.1f} seconds")

except Exception as exc:
    print(f"Test failed: {type(exc).__name__}: {exc}")
