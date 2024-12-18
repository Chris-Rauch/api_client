'''
exceptions.py

Custom exception messages to help with debugging and error finding

Requirements:
  - None
'''

class RoboClientException(Exception):
    '''Base Exception for all RoboClient related errors'''
    def __init__(self, *args):
        super().__init__(*args or "An error occurred in RoboClient")
    
class LoginFailedException(RoboClientException):
    def __init__(self, status_code, json_result, msg="Failed to login"):
        super().__init__(msg)
        self.status_code = status_code
        self.json_result = json_result

class DataFailedException(RoboClientException):
    def __init__(self, endpoint, msg="Having trouble interacting with endpoint."):
        super().__init__(f"{msg} Endpoint: {endpoint}")