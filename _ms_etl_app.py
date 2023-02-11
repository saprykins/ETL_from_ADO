# FUTURE IMPROVEMENTS
# wave can be received from ADO, so the fnc "get_app_list_for_the_wave" to be updated
# child is not verified, here forward should mean child
# getting the if from line is done from left, can be from right to decrease read time
# wave of app can be extracted with additional read of item, parent_id contains wave_id
# if main ...
# currently all referenced by ado ids, it's NOK if we'll use several projects
# don't get server list in app table


import requests
import base64
import pandas as pd


pat = '7m***'
organization = 'g***'
project = 'Migration_Factory'

authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

url = 'https://dev.azure.com/' + organization + '/' + project + '/_apis/wit/workItems/83460/updates?api-version=7.0'
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
for state_change in app_history:
    try:
        # record is json with 2 objects: old and new values 
        state_change_record = state_change["fields"]["System.State"]
        date_change_record = state_change["fields"]["System.ChangedDate"]
        
        # state_change_representation = state_change_record["oldValue"] + ' -> '+ state_change_record['newValue']
        
        app_states.append([state_change_record["oldValue"], state_change_record['newValue']])
        
        # calculating assessment duration
        # prep -> ready
        if (state_change_record["oldValue"] == 'Assessment (Preparation)') and (state_change_record['newValue'] == 'Ready for Migration'):

            # when the status changed to "ready for migration"
            time_stamp_end_str = date_change_record["newValue"][:-1] + '+00:00'
            
            # when the status changed to "assessment"
            time_stamp_start_str = date_change_record["oldValue"][:-1] + '+00:00'
            
            # translate string to date
            time_stamp_end = datetime.strptime(time_stamp_end_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            time_stamp_start = datetime.strptime(time_stamp_start_str, "%Y-%m-%dT%H:%M:%S.%f%z")

            assessment_duration = time_stamp_end - time_stamp_start
            print(assessment_duration)


        # calculating migration execution (
        # if both sign-off and migration execuction mentioned
        # mig exec -> sign-off
        if (state_change_record["oldValue"] == 'Migration Execution') and (state_change_record['newValue'] == 'Sign-Off'):

            # when the status changed to "ready for migration"
            time_stamp_end_str = date_change_record["newValue"][:-1] + '+00:00'
            
            # when the status changed to "assessment"
            time_stamp_start_str = date_change_record["oldValue"][:-1] + '+00:00'
            
            # translate string to date
            time_stamp_end = datetime.strptime(time_stamp_end_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            time_stamp_start = datetime.strptime(time_stamp_start_str, "%Y-%m-%dT%H:%M:%S.%f%z")

            migration_execution_duration = time_stamp_end - time_stamp_start
            print(migration_execution_duration)
        
        
        # calculating migration execution
        # if no migration execuction mentioned, but there is ready for migration state
        # ready for mig -> sign-off (w/o mig exec)
        elif (state_change_record["oldValue"] == 'Ready for Migration') and (state_change_record['newValue'] == 'Sign-Off'):

            # when the status changed to "ready for migration"
            time_stamp_end_str = date_change_record["newValue"][:-1] + '+00:00'
            
            # when the status changed to "assessment"
            time_stamp_start_str = date_change_record["oldValue"][:-1] + '+00:00'
            
            # translate string to date
            time_stamp_end = datetime.strptime(time_stamp_end_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            time_stamp_start = datetime.strptime(time_stamp_start_str, "%Y-%m-%dT%H:%M:%S.%f%z")

            migration_execution_duration = time_stamp_end - time_stamp_start
            # print(time_stamp_start.minute)
            # print(migration_execution_duration.seconds) # does exist

            print(migration_execution_duration)
            
            days, seconds = migration_execution_duration.days, migration_execution_duration.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60

            print('{} days, {} hours, {} minutes, {} seconds'.format(days, hours, minutes, seconds))

    except:
        print("i")


# display all phases without repetitions:
representation_of_states_str = ''

# to get the latest state change
max_i = len(app_states) - 1

for i in range(len(app_states)):
    if i == 0:
        representation_of_states_str = app_states[0][0]
    elif i == max_i:
        representation_of_states_str = representation_of_states_str + ' -> '+ app_states[i][0] + ' -> ' + app_states[i][1]
    else:
        representation_of_states_str = representation_of_states_str + ' -> '+ app_states[i][0]
print(representation_of_states_str)
