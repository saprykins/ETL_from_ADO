# to be used to extract app state changes
# create an additional table that will store "app_id" - "history" relation
# where history = assessment time, migration time


import requests
import base64
import pandas as pd
from datetime import datetime


pat = 'i**'
organization = 'g**'
# project = 'A**'
project = 'M**'


# https://dev.azure.com/go-gl-pr-migfactory-axa365/Migration_Factory/_apis/wit/workItems/110355/updates?api-version=7.0
# exports only yet to start, 
# in fact: yet to start + ready for mig

authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')




# cols_history =  ["App id in ADO", "Phases", "Assessment duration", "Migration duration"]
cols_history =  ["App id in ADO", "Phases"]
df_history = pd.DataFrame([],  columns = cols_history)



def get_all_applications_list_from_ado():
    """
    The function uses query that is defined in ADO
    The mentioned query displays the list of all applications (for all waves in the projects)
    The function exists to create mapping between applications and servers
    """
    list_of_all_applications = []
    
    url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/wiql/e2c3101f-d2e2-4156-a57d-53b40a6fec6a" # all apps
    # url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/wiql/efa0655f-dada-47a0-95f1-fe6f15bc139e" # based on chosen waves
    
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    applications_raw_data = response.json()["workItems"]
    for application in applications_raw_data:
        list_of_all_applications.append(application["id"])
    return list_of_all_applications



def get_state_changes(application_id, df_history):
    url = 'https://dev.azure.com/' + organization + '/' + project + '/_apis/wit/workItems/' + str(application_id) + '/updates?api-version=7.0'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )

    # which states app went through
    app_states = []
    app_history = response.json()["value"]
    # app_history = response.json()
    # print(app_history)
    
    for state_change in app_history: # for each change 
        try:
            # record is json with 2 objects: old and new values 
            state_change_record = state_change["fields"]["System.State"]
            # print(state_change_record)
            if state_change_record['newValue']: 
                app_states.append(state_change_record['newValue'].lower())

            # print('new state is ', app_states)
            # date_change_record = state_change["fields"]["System.ChangedDate"]
            # state_change_representation = state_change_record["oldValue"] + ' -> '+ state_change_record['newValue']
                        

        except:
            assessment_duration = 0
            # state_change_record = state_change["fields"]["System.State"]
            # app_states.append([state_change_record["newValue"]])
            #
            #
            #
            # app_states.append(state_change_record["newValue"])
            #
            #
            #
            # print('')

    # return df_applications
    


    # display all phases without repetitions:
    representation_of_states_str = ''
    # print('---')
    # print(app_states)
    # print('---')



    if len(app_states) == 1:
        representation_of_states_str = app_states[0]
    elif len(app_states) == 2:
        representation_of_states_str = app_states[0] + ' -> '+ app_states[1]
    else: 
        for i in range(len(app_states)):
            if i == 0:
                representation_of_states_str = app_states[0]
            # elif i == max_i:
                # representation_of_states_str = representation_of_states_str + ' -> '+ app_states[-1]
            else:
                representation_of_states_str = representation_of_states_str + ' -> '+ app_states[i]


    # to get the latest state change
    """
    else:
        max_i = len(app_states) - 1
        for i in range(len(app_states)):
            if i == 0:
                representation_of_states_str = app_states[0][0]
            elif i == max_i:
                representation_of_states_str = representation_of_states_str + ' -> '+ app_states[i][0] + ' -> ' + app_states[i][1]
            else:
                representation_of_states_str = representation_of_states_str + ' -> '+ app_states[i][0]
        # print(representation_of_states_str)
    """




    new_row = [application_id, representation_of_states_str]
    new_df = pd.DataFrame([new_row], columns=cols_history)
    df_history = pd.concat([df_history, new_df], ignore_index = True)
    # print(df_history)
    return df_history



# MAIN



list_of_all_applications = get_all_applications_list_from_ado()
# list_of_all_applications = [112194] # 3
# list_of_all_applications = [111131] # 1
# list_of_all_applications = [110355] # 2

for application_id in list_of_all_applications:
    df_history = get_state_changes(application_id, df_history)

# print(df_history)



df_history.to_csv('./results/__ms_history.csv')

"""
days, seconds = migration_execution_duration.days, migration_execution_duration.seconds
hours = days * 24 + seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60

print('{} days, {} hours, {} minutes, {} seconds'.format(days, hours, minutes, seconds))
"""
