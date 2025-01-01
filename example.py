'''
example.py
'''
#from src.api_client import APIClient
from src.robo_client import RoboClient
import file_handlers.config_file
#from config import auth

config = file_handlers.config_file.ConfigFile("C:\\Users\\rauch\\Downloads\\config.json")
config.read_file()
client = RoboClient(config.get_auth())

if not client.login():
    print("Something went wrong...")

job_details = client.get_job_details('1020698')
if job_details:
    print(job_details)
'''
job_details = client.multi_job("testing12272024", "Hello, this is your $var1 test",[{
        "name": "MONSTER QUALITY TRANSPORT INC",
        "phone": "714-329-0331",
        "var1": "First",
        "var2": None,
        "var3": None,
        "var4": None,
        "groupname": "Testing12172024"
    }], "2024/12/27 12:30:00")
if job_details:
    print(job_details)
'''