import requests
import json
import base64

pat = 'j*'
organization = 'g*'
project = 'ADO%20Testing'
workitemtype = "task"


# authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/workitems/$" + workitemtype + "?api-version=7.0"
url = "https://dev.azure.com/{}/{}/_apis/wit/workitems/${}?api-version=7.0".format(organization, project, workitemtype)

headers = {
    "Content-Type": "application/json-patch+json"
}

body = [
    {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "Sample Task 3"
    }
]

r = requests.post(
    url,
    data=json.dumps(body),
    headers=headers,
    auth=("", pat), 
    # timeout=60,
)


print(r)

