import requests
import json
import base64
import pandas as pd
from datetime import datetime
import time
import openpyxl


ORGANIZATION_NAME = 'g***'

# Personal Access Token (PAT) for authentication
pat = 'b***'

# Project ID for your Azure DevOps project
PROJECT_NAME = 'M***'

authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

cols_duration =  [
    "App id", 
    "App name", 
    "Feature id", 
    "Feature", 
    "User story id", 
    "User story", 
    "Task id", 
    "Task", 
    "Duration (min)"
]

df_duration = pd.DataFrame([], columns = cols_duration)



def get_childs_list(app_id):
    #
    #
    #
    url = f"https://dev.azure.com/{ORGANIZATION_NAME}/{PROJECT_NAME}/_apis/wit/workitems/{app_id}/?$expand=all"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization,
    }
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    
    # Get the child work items of the application
    user_story_work_items = response_json["relations"]

    child_ids = []
    for relation in user_story_work_items:
        if relation["rel"] == "System.LinkTypes.Hierarchy-Forward":
            url = relation["url"]
            parts = url.split('/')
            id = parts[-1]
            child_ids.append(id)
    childs_work_item_ids = child_ids
    # print(f"User story ids: {user_story_work_item_ids}")
    return childs_work_item_ids





def get_duration(workitem_id):
    #
    #
    #
    # workitem_id = int('173250')

    url = 'https://dev.azure.com/' + ORGANIZATION_NAME + '/' + PROJECT_NAME + '/_apis/wit/workItems/' + str(workitem_id) + '/updates?api-version=7.0'
    # print(url)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    changes = response.json()["value"]
    for state_change in reversed(changes):
        try:
            title = state_change["fields"]["System.Title"]['newValue'] 
            break
        except:
            title = None
    # print(title)
    
    
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
        try:
            in_progress_date = datetime.strptime(status_change["fields"]['Microsoft.VSTS.Common.StateChangeDate']['oldValue'], '%Y-%m-%dT%H:%M:%S.%fZ')
            closed_date = datetime.strptime(status_change["fields"]['Microsoft.VSTS.Common.StateChangeDate']['newValue'], '%Y-%m-%dT%H:%M:%S.%fZ')
            # print(in_progress_date)
            # print(closed_date)
            duration = closed_date - in_progress_date
            # print(duration)
            duration_sec = duration.seconds
            duration_min = duration_sec/60
            # print(f"duration is {duration_min} min")
        except:
            duration_min = None
    else:
        duration_min = None
        # print(f"N/A for the work item {workitem_id}")

    if duration_min is not None:
        duration_min = round(duration_min)

    return (duration_min, title)

# time = get_duration('workitem_id')
# print(time)





def save_duration_to_df(app_id, df_duration):
    #
    #
    #
    feature_ids = get_childs_list(app_id)
    # print(feature_ids)
    duration_x, app_title = get_duration(app_id)
    for feature_id in feature_ids:
        user_story_ids = get_childs_list(feature_id)
        duration_y, feature_title = get_duration(feature_id)
        # print(user_story_ids)
        for user_story_id in user_story_ids:
            task_ids = get_childs_list(user_story_id)
            duration_z, user_story_title = get_duration(user_story_id)
            # print(task_ids)
            for task_id in task_ids:
                duration, task_title = get_duration(task_id)
                new_row = [app_id, app_title, feature_id, feature_title, user_story_id, user_story_title, task_id, task_title, duration]
                new_df = pd.DataFrame([new_row], columns=cols_duration)
                df_duration = pd.concat([df_duration, new_df], ignore_index = True)  
    return df_duration



def get_list_of_migrated_apps():
    #
    #
    #
    list_of_apps = []
    # url = 'https://dev.azure.com/' + ORGANIZATION_NAME + '/' + PROJECT_NAME + '/_apis/wit/workItems/' + str(workitem_id) + '/updates?api-version=7.0'
    url = "https://dev.azure.com/" + ORGANIZATION_NAME + "/" + PROJECT_NAME + "/_apis/wit/wiql/e48e7c28-cdc5-4035-874d-695f4e7ae174"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    apps_raw_data = response.json()["workItems"]
    for app in apps_raw_data:
        list_of_apps.append(app["id"])
    return list_of_apps

# print(get_list_of_migrated_apps())
    


# 
# MAIN
#
start_time = time.time()/60 # sec


# app_id = "173026"
# df_duration = save_duration_to_df(app_id, df_duration)



list_of_apps = get_list_of_migrated_apps()
list_of_apps = list_of_apps[20:]

for app_id in list_of_apps:

    df_duration = save_duration_to_df(app_id, df_duration)
# print(df_duration)
# display(df_duration)

df_duration.to_excel('./results/ADO_MS_duration_extract_3.xlsx', sheet_name='duration', index=False)

end_time = time.time()/60 # sec
print(end_time - start_time)
