import requests

class APIClient:
    def __init__(self):
        self.base_url = "https://your-project.up.railway.app/api"
        self.token = None

    def login(self, username, password):
        try:
            response = requests.post(f"{self.base_url}/token/", json={
                "username": username,
                "password": password
            }, timeout=7)
            if response.status_code == 200:
                self.token = response.json().get("access")
                return {"success": True, "token": self.token}
            return {"success": False, "error": "Invalid credentials"}
        except requests.exceptions.RequestException:
            return {"success": False, "error": "Network connection error"}

    def fetch_data(self):
        if not self.token:
            return {"success": False, "error": "Not authenticated"}
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/items/", headers=headers, timeout=7)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            return {"success": False, "error": "Failed to fetch data"}
        except requests.exceptions.RequestException:
            return {"success": False, "error": "Offline or network failure"}