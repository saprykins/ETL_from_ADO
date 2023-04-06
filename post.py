import requests
import json
import base64

pat = 'j*'
organization = 'g*'
project = 'ADO%20Testing'
workitemtype = "task"


# 1/ get all apps
# 2/ get link for each application
# 3/ upload a task to application


# 1/ OK
def get_all_applications_list_from_ado():
    """
    The function uses query that is defined in ADO
    The mentioned query displays the list of all applications (for all waves in the projects)
    The function exists to create mapping between applications and servers
    """
    list_of_all_applications = []
    
    url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/wiql/0a894ff4-67d6-4115-b33e-3aa8a5945e3d"

    headers = {
        "Content-Type": "application/json-patch+json"
    }

    response = requests.get(
        url = url,
        headers=headers,
        auth=("", pat), 
    )

    applications_raw_data = response.json()["workItems"]
    for application in applications_raw_data:
        list_of_all_applications.append(application["id"])
    return list_of_all_applications

# app_list = get_all_applications_list_from_ado()
# print(len(app_list))
app_list = [172056]


# 2/

def get_app_url(application_wi_id):   
   
    url = 'https://dev.azure.com/' + organization + '/_apis/wit/workItems/' + str(application_wi_id) + '?$expand=all'
    
    headers = {
        "Content-Type": "application/json-patch+json"
    }

    response = requests.get(
        url = url,
        headers=headers,
        auth=("", pat), 
    )
    # print(response)
    lnk = response.json()["url"]
    return lnk

for app in app_list:
    lnk = get_app_url(app)
    print(lnk)




# 3/ 
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

"""
r = requests.post(
    url,
    data=json.dumps(body),
    headers=headers,
    auth=("", pat), 
    # timeout=60,
)

print(r)
"""
