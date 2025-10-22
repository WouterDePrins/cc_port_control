# catalyst_auth/client.py

import requests
import urllib3
from typing import Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CCAPI:
    def __init__(self, base_url: str, username: str, password: str, verify_ssl: bool = False):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self._token: Optional[str] = None

    def authenticate(self) -> str:
        """Authenticate and store the token internally."""
        auth_endpoint = f"{self.base_url}/dna/system/api/v1/auth/token"
        response = requests.post(
            auth_endpoint,
            auth=(self.username, self.password),
            verify=self.verify_ssl
        )
        response.raise_for_status()
        token = response.json().get("Token")
        if not token:
            raise ValueError("Token not found in response.")
        self._token = token
        return token

    def get_token(self) -> str:
        """Get or refresh the token."""
        if not self._token:
            self.authenticate()
        return self._token

    def _headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "X-Auth-Token": self.get_token()
        }

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        url = f"{self.base_url}{path}"
        response = requests.get(url, headers=self._headers(), params=params, verify=self.verify_ssl)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, data: Optional[dict] = None) -> dict:
        url = f"{self.base_url}{path}"
        response = requests.post(url, headers=self._headers(), json=data, verify=self.verify_ssl)
        response.raise_for_status()
        return response.json()

    def put(self, path: str, data: Optional[dict] = None) -> dict:
        url = f"{self.base_url}{path}"
        response = requests.put(url, headers=self._headers(), json=data, verify=self.verify_ssl)
        response.raise_for_status()
        return response.json()
