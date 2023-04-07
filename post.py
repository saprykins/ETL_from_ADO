import requests
import json
import base64

pat = 'j*'
organization = 'g*'
project = 'ADO%20Testing'
workitemtype = "Playbook"

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

'''
for app in app_list:
    lnk = get_app_url(app)
    print(lnk)
'''



# 3/
def add_task_to_one_tcs_app(app):
    # url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/workitems/$" + workitemtype + "?api-version=7.0"
    url = "https://dev.azure.com/{}/{}/_apis/wit/workitems/${}?api-version=7.0".format(organization, project, workitemtype)

    headers = {
        "Content-Type": "application/json-patch+json"
    }

    # "System.Title": "2 - Assess"
    # "Custom.Playbook_Phase": "2 - Assess" # NOT IMPLEMENTED CUZ PROVOKES ERROR
    # "Custom.PlaybookActivities": "2.2 Detailed application assessment"
    # "Custom.PlaybookSubActivities": "Application discovery (platform, database, security, operations)"
    # "Custom.PlaybookOwner": "TCS",
    # "Custom.PlaybookOwnerTeam": "Migration team" # not always
    # "Custom.PlaybookDetails": "List of servers, DB, IP address, matrix flow… / ADS done in parallel",

    body = [
        {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "3 - Prepare"
        },
        #{
        #"op": "add",
        #"path": "/fields/Custom.Playbook_Phase",
        #"value": "8 - Decom"
        #},
        {
        "op": "add",
        "path": "/fields/Custom.PlaybookActivities",
        "value": "3.6 System preparation"
        },
        {
        "op": "add",
        "path": "/fields/Custom.PlaybookSubActivities",
        "value": "Service account"
        },

        {
        "op": "add",
        "path": "/fields/Custom.PlaybookOwner",
        "value": "TCS"
        },
        {
        "op": "add",
        "path": "/fields/Custom.PlaybookOwnerTeam",
        # "value": "Migration team"
        "value": "Application owner"
        },
        {
        "op": "add",
        "path": "/fields/Custom.PlaybookDetails",
        "value": "Check if Service account is used, and if it uses admin role. More deails: 'https://confluence.axa.com/confluence/display/PIaaSExit/Task%3A+Service+account+-+admin'"
        },
        {
        "op": "add",
        "path": "/fields/System.Parent",
        "value": app
        },
        {
        "op": "add",
        "path": "/relations/-",
        "value": {
            "rel":"System.LinkTypes.Hierarchy-Reverse",
            "url":get_app_url(app)
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


# MAIN

app_list = get_all_applications_list_from_ado()
# print(app_list)
# app_list = [172056] # POC

# app = app_list[0]
# print(app)

for app in app_list:
    add_task_to_one_tcs_app(app)
