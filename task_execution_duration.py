import requests
import base64
# import pandas as pd
from datetime import datetime


organization_url = 'g***'

# Personal Access Token (PAT) for authentication
pat = 'b***'

# Project ID for your Azure DevOps project
project_id = 'M***'

authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

# workitem_id = int('50609')
workitem_id = int('173250')

url = 'https://dev.azure.com/' + organization_url + '/' + project_id + '/_apis/wit/workItems/' + str(workitem_id) + '/updates?api-version=7.0'

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+ authorization
}
response = requests.get(
    url = url,
    headers=headers,
)

app_history = response.json()["value"]

# if status changed from in-progress to closed
status_change = None

for state_change in reversed(app_history):
    try:
        if state_change["fields"]["System.State"]['oldValue'] == "In-Progress" and state_change["fields"]["System.State"]['newValue'] == "Closed":
            status_change = state_change
            # print(status_change)
            break
    except:
        val = 0

# Calculate the duration of the work item in progress
if status_change is not None:
    in_progress_date = datetime.strptime(status_change["fields"]['Microsoft.VSTS.Common.StateChangeDate']['oldValue'], '%Y-%m-%dT%H:%M:%S.%fZ')
    closed_date = datetime.strptime(status_change["fields"]['Microsoft.VSTS.Common.StateChangeDate']['newValue'], '%Y-%m-%dT%H:%M:%S.%fZ')
    print(in_progress_date)
    print(closed_date)
    duration = closed_date - in_progress_date
    print(duration)
else:
    print(f"N/A for the work item {workitem_id}")
