'''
robo_client.py

Inherits APIClient class. RoboClient implements specific HTTP requests with API
endpoints already identified and data handlers implemented.

Requirements:
  - APIClient: The base class to handle HTTP requests
  - exceptions: Used for implementing custom exceptions
'''
from api_client.src.api_client import APIClient
import api_client.src.exceptions as re
import requests

class RoboClient(APIClient):
    '''RoboClient'''
    
    def __init__(self, api_key, base_url = "https://robotalker.com"):
        super().__init__(base_url, api_key)
        self.cookie = None
        self.job_name = None

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
        endpoint = "/REST/api/Login"
        try:
            response = super().get(endpoint)
            
            # if get was successful
            if response != None and response.status_code == 200 and "Set-Cookie" in response.headers:
                self.cookie = response.headers["Set-Cookie"].split(";")[0].strip()
                self.headers["Cookie"] = self.cookie
                self.headers.pop("Authorization")
                return True
            raise re.LoginFailedException(response.status_code, response.json())
        except re.LoginFailedException as e:
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
        endpoint = "/REST/api/Config"
        config = None
        try:
            response = super().get(endpoint)
            if response.status_code == 200 and "Callbalance" in response.json():
                config = response.json()
            else:
                raise re.DataFailedException(endpoint=endpoint)
        except re.DataFailedException as e:
            print(e)
        return config

    def multi_job(self, job_name, message_text, robo_contacts, start_time, end_time = None):
        """
        Schedules a job with the specified data.

        Returns: Job details as a dictionary if successful, None otherwise
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
        endpoint = "/REST/api/MultiJob"
        job_details = None
        for i in range(len(robo_contacts)):
            robo_contacts[i]['groupname'] = job_name

        data = {
            "whattodo": "SendTtsMessage",
            "jobname": job_name,
            "optcallerid": "9494709674",
            "messageid": "0",
            "messagetext": message_text,
            "customername": "Chris Rauch",
            "extrareportemail": "rauch.christopher13@gmail.com",
            "phonelistgroupname": job_name,
            "contactlist": robo_contacts,
            "rundatetime": start_time,
            "enddatetime": end_time
        }

        try:
            if self._check_times(start_time, end_time):
                raise InvalidScheduleTime(endpoint)

            response = super().post(endpoint=endpoint, data=data)
            if response.status_code == 200 and "JobName" in response.json():
                job_details = response.json()
            
            else:
                raise re.DataFailedException(endpoint=endpoint)
        except re.InvalidScheduleTime as e:
            print(e)
        except re.DataFailedException as e:
            print(e)
        return job_details

    def multi_job_collection(self, job_name, contacts, start_time, end_time):
        message_text = "Hello, this is General Agents Acceptance. This is the #var1# courtesy call to follow up on the remaining balance bill we sent you for contract number $var2 for the amount of $var3. For more information please give us a call at 949-470-9674. Thank you and have a great day!"
        self.multi_job(job_name, message_text, contacts, start_time, end_time)
    
    def job_summary(self, jobname):

        """
        Fetches the summary of a job by its name.

        Return: The job summary as a dictionary is successful, None otherwise
        Parameters:
            jobname (str): The name of the job to query.
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
        endpoint = "/REST/api/Jobsummary"
        param = {
            "jobname": jobname,
        }
        job_summary = None
        try:
            response = super().get(endpoint=endpoint, params=param)
            if response.status_code == 200 and "call" in response.json():
                job_summary = response.json()
            else:
                raise re.DataFailedException
        except re.DataFailedException as e:
            print(e)
        return job_summary

    def get_job_details(self, job_id: str, user_id = '2402'):
        '''
        Fetches job details for a specified job. 

        Parameters: 
        job_id (str): job id as a string. This is returned when posting in
        multi_job_post()
        user_id (str): user_id as a string. This also returned in multi_job_post()
        Return: Job Details as a dictionary. If the robotalker server hasn't
        completed the job or if the GET request fails, return None

        '''
        endpoint = '/GetJobDetail.ashx?'
        param = {
            "jobID": job_id,
            "userId": user_id
        }
        
        job_details = None
        try:
            response = super().get(endpoint=endpoint, params=param)
            if response.status_code == 200 and "No record found." == response.text:
                job_details = None
            elif response.status_code == 200 and "ContactName" in response.text:
                job_details = response.json()
            else:
                raise re.DataFailedException
        except re.DataFailedException as e:
            print(e)
        return job_details

    def poll_job_details(self, interval: int, job_id: str, user_id = '2402'):
        '''
        Polls robotalker's GetJobDetail.ashx? endpoint by calling get_job_details
        at the specified interval. Will time out after 20min
        Parameters:
          interval (int): wait time between function calls in seconds
          job_id (str): identifies the target job to request info.
          user_id (str): an account identifier. Remains constant per user.
        Note - job_details is returned i a dictionary by POST methods (multi_job and multi_job_collection)
             - user_id can be found in user settings at robotalker.com
        Return:
          returns the job details as a list of dicts if successful
          returns None if the the function times out (20min) or if unsuccessful
        '''
        if interval <= 0:
            raise ValueError("Interval must be greater than 0")
        
        timeout = 20*60 # 20 minutes in seconds
        start_time = time.time()

        while True:
            job_details = get_job_details(job_id, user_id)
            
            # return details if successful
            if job_details:
                return job_details

            # return None if timed out
            elif (time.time() - start_time) > timeout:
                print("Polling timed out after 20 minutes")
                return None

            # wait and try again
            else: 
                time.sleep(interval)

    def _check_times(self, start_time, end_time):
        ''' 
        I don't want the user to be able to send calls out after business hours
        '''
        return False
