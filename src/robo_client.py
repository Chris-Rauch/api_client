'''
robo_client.py

Inherits APIClient class. RoboClient implements specific HTTP requests with API
endpoints already identified and data handlers implemented.

Requirements:
  - APIClient: The base class to handle HTTP requests
  - exceptions: Used for implementing custom exceptions
'''
from api_client import APIClient
import exceptions as re

class RoboClient(APIClient):
    # TODO implement basic auth verification
    def __init__(self, api_key, base_url = "https://robotalker.com/REST"):
        super().__init__(base_url, api_key)
        self.cookie = None
        self.jobName = None

    def login(self):
        """
        Logs into the RoboTalker API using Basic AUTH and stores the session cookie.

        Returns: True if successful, False otherwise.
        API Endpoint: /api/Login
        Responses:
            200: Successfully logged in; cookie stored.
            403: Authentication failed.
            500: Unknown error occurred.
        """
        endpoint = "/api/Login"
        try:
            response = super().get(endpoint)
            if response.status_code is 200 and "Set-Cookie" in response.headers:
                self.cookie = response.headers["Set-Cookie"].split(";")[0].strip()

                # update header
                self.headers["Cookie"] = self.cookie
                self.headers.pop("Authorization")
                return True
            else:
                raise re.LoginFailedException(response.status_code, response.json())
        except re.LoginFailedException as e:
            print(e)
        except Exception as e:
            print(e)
        return False
    
    def config(self):
        '''
        Retrieves account details including call and SMS balances.

        Returns: Configuration dictionary if successful, None otherwise.
        API Endpoint: /api/Config
        Example Response:
            {
            "AutoRecharge": "off",
            "Callbalance": "1038",
            "Smsbalance": "2076",
            "AutoResponderNumber": "Not setup",
            "ReportEmail": "gaac@mygaac.com"
            }
        '''
        endpoint = "/api/Config"
        config = None
        try:
            response = super().get(endpoint)
            if response.status_code is 200 and "Callbalance" in response.json():
                config = response.json()
            else:
                raise re.DataFailedException(endpoint=endpoint)
        except re.DataFailedException as e:
            print(e)
        except Exception as e:
            print(e)
        return config

    def multiJob(self, data):
        """
        Schedules a job with the specified data.

        Returns: Job details dictionary if successful, None otherwise
        Parameters:
            data (dict): Job details. See eof for an example
        API Endpoint: /api/MultiJob
        Responses:
        200: Job scheduled successfully.
        Example Response:
        {
            "JobName": "Testing12172024",
            "smsId": None, 
            "callId": "1019558"
        }
        """
        endpoint = "/api/MultiJob"
        job_details = None
        try:
            response = super().post(endpoint=endpoint, data=data)
            if response.status_code == 200 and "JobName" in response.json():
                job_details = response.json()
            else:
                raise re.DataFailedException(endpoint=endpoint)
        except Exception as e:
            print(e)
        return job_details
    
    def jobSummary(self, jobname):
        """
        Fetches the summary of a job by its name.

        Return: job_summary dictionary is successful, None otherwise
        Parameters:
            jobname (str): The name of the job to query.
        Returns: None (no implemented response handling yet).
        API Endpoint: /api/Jobsummary
        Example Response:
        {
            "call": {
                "TriggerStatus": "Completed",
                "StartTime": "12/17/2024 3:20:00 PM",
                "TotalContacts": 213,
                "Name": "LP 12/09/2024 to 12/13/2024",
                "Completed": 189,
                "Delivered": 76,
                "VoiceMail": 113,
                "LineBusy": 0,
                "NotAnswered": 0,
                "InvalidNumber": 24,
                "Id": 1019533
            },
            "sms": null
        }
        """
        endpoint = "/api/Jobsummary"
        param = {
            "jobname": jobname,
        }
        job_summary = None
        try:
            response = super().get(endpoint=endpoint, params=param)
            if response.status_code is 200 and "call" in response.json():
                job_summary = response.json()
            else:
                raise re.DataFailedException
        except re.DataFailedException as e:
            print(e)
        except Exception as e:
            # return 204 if jobname isn't valid
            print(e)
        return job_summary 