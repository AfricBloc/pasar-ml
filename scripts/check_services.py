"""
Ping all running agents to confirm health.
"""
import requests

agents = {
    "Xiara": "http://localhost:8001",
    "Shogun": "http://localhost:8002",
    "Resolute": "http://localhost:8003",
    "Xena": "http://localhost:8004"
}

def run():
    print("🔍 Checking agent health endpoints...")
    for name, url in agents.items():
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print(f"✅ {name} is up.")
            else:
                print(f"⚠️ {name} responded with status {resp.status_code}.")
        except Exception as e:
            print(f"❌ {name} check failed: {e}")

if __name__ == "__main__":
    run()
