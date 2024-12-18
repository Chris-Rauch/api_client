'''
example.py
'''
#from src.api_client import APIClient
from src.robo_client import RoboClient
from config import auth



client = RoboClient(auth)
if client.login():
    print("logged in succesfully. Cookie is set")
else:
    print("Something went wrong...")

call_balance = client.config()['Callbalance']

data = {
    "whattodo": "SendTtsMessage",
    "jobname": "Testing12172024",
    "optcallerid": "9494709674",
    "messageid": "0",
    "messagetext": "Hello, this is a test. 1 2 3...3 2 1",
    "customername": "Chris Rauch",
    "extrareportemail": "rauch.christopher13@gmail.com",
    "phonelistgroupname": "Testing12172024",
    "contactlist": [{
        "name": "MONSTER QUALITY TRANSPORT INC",
        "phone": "714-329-0331",
        "var1": "First",
        "var2": None,
        "var3": None,
        "var4": None,
        "groupname": "Testing12172024"
    }],
    "rundatetime": "2024/12/18 12:30:00"
}

client.multiJob(data)
