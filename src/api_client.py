"""
api_client.py

Base class used for sending HTTP requests. Implements generic post, get, put 
and delete functions

Dependencies:
  - requests
"""

import requests

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        """
        Initializes the APIClient with the base URL and API key.
        """
        self.base_url = base_url.rstrip('/')  # Ensure no trailing slash
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def _request(self, method: str, endpoint: str, data=None, params=None):
        """
        Sends an HTTP request to the API.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"  # Ensure correct URL format
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=10,  # Set a timeout for requests
            )
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - {response.text}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        return None

    def get(self, endpoint: str, params=None):
        """
        Sends a GET request.
        """
        return self._request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data=None):
        """
        Sends a POST request.
        """
        return self._request("POST", endpoint, data=data)
    
    def put(self, endpoint: str, data=None):
        """
        Sends a PUT request.
        """
        return self._request("PUT", endpoint, data=data)
    
    def delete(self, endpoint: str):
        """
        Sends a DELETE request.
        """
        return self._request("DELETE", endpoint)