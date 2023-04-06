import requests
import json
import base64

pat = 'j*'
organization = 'g*'
project = 'ADO%20Testing'
workitemtype = "task"


# authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

# url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/workitems/$" + workitemtype + "?api-version=7.0"
url = "https://dev.azure.com/{}/{}/_apis/wit/workitems/${}?api-version=7.0".format(organization, project, workitemtype)

headers = {
    "Content-Type": "application/json-patch+json"
}

body = [
    {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "Sample Task 8"
    },
    {
    "op": "add",
    "path": "/fields/System.Description",
    "value": "has parent"
    },
    {
    "op": "add",
    "path": "/fields/System.IterationPath",
    "value": "ADO Testing\\Sprint 1"
    },
    {
    "op": "add",
    "path": "/fields/System.Parent",
    "value": "173988"
    },
    {
    "op": "add",
    "path": "/relations/-",
    "value": {
        "rel":"System.LinkTypes.Hierarchy-Reverse",
        "url":"https://dev.azure.com/go-gl-pr-migfactory-axa365/1e294b14-8de0-43b1-962a-4fe4275e31c7/_apis/wit/workItems/173988"
        }
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
