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


pat = 'uk**'
organization = 'go**'
project = 'AX**'

authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')


# initialization dataFrame
cols =  ["App id in ADO", "Title", "Servers", "Environment", "State", "Entity", "Date", "Wave"]
cols_servers = ["Server id in ADO", "Title", "FQDN", "Sign-off Ops", "Sign-off Cyber"]
cols_map_servers_apps = ["Server id in ADO", "App id in ADO"]

df_applications = pd.DataFrame([],  columns = cols)
df_servers = pd.DataFrame([],  columns = cols_servers)
df_map_server_vs_app = pd.DataFrame([],  columns = cols_map_servers_apps)


def get_app_list_for_the_wave(list_of_applications):
    """
    Extract app ids
    histroy: a way of getting the list of applications related to specific waves was not found
    it was possible to get a list of applications and related waves

    This takes the result of this query and saves in a list only app ids (without waves)
    The waves should be specified in ADO UI
    
    this is second wave: 89758 (MEX_wave2), 87108(AFA_wave2)
    """
    
    url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/wiql/f50dc2a7-f6d5-43d6-aa2f-f9e77ebc4b48"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    try:
        wi_relations = response.json()["workItemRelations"]
    except: 
        wi_relations = ""

    for relation in wi_relations:
        if (relation["rel"] == None):
            list_of_applications.append(relation["target"]["id"])
    return list_of_applications


def save_application_wi_into_data_frame(application_wi_id, df_applications):   
    """
    Get a working item title, parent, status 
    and saves it into a dataframe
    application_wi_id - the application for which data is extracted
    df_applications - used as storage object
    """
    
    url = 'https://dev.azure.com/' + organization + '/_apis/wit/workItems/' + str(application_wi_id) + '?$expand=all'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    # application item Title
    wi_title = response.json()["fields"]["System.Title"]

    # application item Environment
    try:
        wi_env = response.json()["fields"]["Custom.EnvironmentTargetSubscription"]
    except: 
        wi_env = ""
    
    # application item entity
    try:
        wi_entity = response.json()["fields"]["Custom.Entity"]
    except: 
        wi_entity = ""

    # application item state
    try:
        wi_state = response.json()["fields"]["System.State"]
    except: 
        wi_state = ""

    # application item assessment date
    try:
        wi_date = response.json()["fields"]["Custom.PlannedPreAssessmentStart"]
    except: 
        wi_date = ""

    wi_wave = "wave_2"

    # add list of servers
    list_of_ids_of_servers = []
    list_of_ids_of_servers = get_server_wi_ids_from_application(application_wi_id)

    new_row = [application_wi_id, wi_title, list_of_ids_of_servers, wi_env, wi_state, wi_entity, wi_date, wi_wave]
    new_df = pd.DataFrame([new_row], columns=cols)
    
    # load data into a DataFrame object:
    df_applications = pd.concat([df_applications, new_df], ignore_index = True)

    return df_applications


def get_server_wi_ids_from_feature(feature_id):
    """
    Given feature_id the function gets data on its children
    It verified if feature name is "Servers"
    And get its children ids
    """

    url = 'https://dev.azure.com/' + organization + '/_apis/wit/workItems/' + str(feature_id) + '?$expand=all'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }

    response = requests.get(
        url = url,
        headers=headers,
    )
    
    list_of_ids_of_servers = []

    feature_title = response.json()["fields"]["System.Title"]
    if feature_title == "Servers":
        relations = response.json()["relations"]
        for relation in relations: 
            if relation["rel"] == "System.LinkTypes.Hierarchy-Forward":
                raw_id = relation['url']
                start_line = raw_id.find('workItems/') + 10
                server_id = int(raw_id[start_line:])
                list_of_ids_of_servers.append(server_id)

    return list_of_ids_of_servers



def get_server_wi_ids_from_application(application_id):
    """
    Given app_id, this function gets ids of its servers
    """

    url = 'https://dev.azure.com/' + organization + '/_apis/wit/workItems/' + str(application_id) + '?$expand=all'
    servers_id = []
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    
    # go through features of an app
    # not all applications have servers stored in ADO
    try:
        wi_relations = response.json()["relations"]
    except: 
        wi_relations = ""

    for relation in wi_relations:
        if relation["rel"] == "System.LinkTypes.Hierarchy-Forward":
            # need to go deeper to find servers
            # features can be servers or playbook
            raw_id = relation['url']
            start_line = raw_id.find('workItems/') + 10
            feature_id = int(raw_id[start_line:])
            # print(feature_id) # correct
            list_of_ids_of_servers = get_server_wi_ids_from_feature(feature_id)
            if len(list_of_ids_of_servers)>0:
                # print(list_of_ids_of_servers)
                servers_id = servers_id + list_of_ids_of_servers

        # should we keep it (only 1 feature with servers)
        elif relation["rel"] == "System.LinkTypes.Hierarchy-Reverse":
            # get wave name
            raw_id = relation['url']
            start_line = raw_id.find('workItems/') + 10
            parent_id = int(raw_id[start_line:])
            # print(parent_id)

        # print(relation)
    return servers_id


def get_sign_off_status(sign_off_id): 
    """
    input - id of sign-off
    output - state and sign_off_type (cyber (0), ops(1), entity(2), dba(3))
    output in tuple
    """
    
    url = 'https://dev.azure.com/' + organization + '/_apis/wit/workItems/' + str(sign_off_id)
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    # verification of which sign-off-type
    sign_off_title = response.json()["fields"]["System.Title"]
    if sign_off_title == "Cyber Defense Team Sign-Off":
        sign_off_type = '0'
        state = response.json()["fields"]["System.State"]
    elif sign_off_title == "Operations Team Sign-Off":
        sign_off_type = '1'
        state = response.json()["fields"]["System.State"]
    elif sign_off_title == "DBA Team Sign-Off":
        sign_off_type = '3'
        state = response.json()["fields"]["System.State"]
    elif sign_off_title == "Entity Sign-Off":
        sign_off_type = '2'
        state = response.json()["fields"]["System.State"]

    sign_off_data = [sign_off_type, state]
    return sign_off_data


def save_server_wi_into_data_frame(server_wi_id, df_servers):
    """
    Get a server hostname, statuses
    and saves it into a dataframe
    """
    
    url = 'https://dev.azure.com/' + organization + '/_apis/wit/workItems/' + str(server_wi_id) + '?$expand=all'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    # server item Title
    wi_title = response.json()["fields"]["System.Title"]

    # server hostname
    try:
        wi_hostname = response.json()["fields"]["Custom.HostName"]
    except: 
        wi_hostname = ""

    # need insert sign-off state    
    # working item Relations
    try:
        relations = response.json()["relations"]
    except: 
        relations = ""

    sign_off_ops_state = ''
    sign_off_cyber_state = ''
    for relation in relations: 
        if relation['rel'] == 'System.LinkTypes.Hierarchy-Forward':
            # ids of sign-offs
            raw_id = relation['url']
            start_line = raw_id.find('workItems/') + 10
            sign_off_id = int(raw_id[start_line:])

            # list with 2 fields: 1/0 for cyber, 1 for ops; 2/state
            sign_off_data = get_sign_off_status(sign_off_id)
            if sign_off_data[0] == '0':
                sign_off_cyber_state = sign_off_data[1]

            elif sign_off_data[0] == '1':
                sign_off_ops_state = sign_off_data[1]
            
    new_row = [server_wi_id, wi_title, wi_hostname, sign_off_ops_state, sign_off_cyber_state]
    new_df = pd.DataFrame([new_row], columns=cols_servers)

    # load data into a DataFrame object:
    df_servers = pd.concat([df_servers, new_df], ignore_index = True)

    return df_servers


def get_all_servers_list_from_ado():
    """
    The function uses query that is defined in ADO
    The mentioned query displays the list of all servers
    """
    list_of_all_servers = []
    
    url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/wiql/a0d0d3a8-4a88-4bde-bdf3-4e2b2d803c15"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }
    response = requests.get(
        url = url,
        headers=headers,
    )
    servers_raw_data = response.json()["workItems"]
    for server in servers_raw_data:
        list_of_all_servers.append(server["id"])
    return list_of_all_servers



def get_all_applications_list_from_ado():
    """
    The function uses query that is defined in ADO
    The mentioned query displays the list of all applications (for all waves in the projects)
    The function exists to create mapping between applications and servers
    """
    list_of_all_applications = []
    
    url = "https://dev.azure.com/" + organization + "/" + project + "/_apis/wit/wiql/ba4ac073-2c3d-485a-a36f-2cbb53267487"
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


def save_map_server_vs_app(application_wi_id, df_map_server_vs_app): 
    """
    Get a map between ids (servers vs applications)
    """
    
    list_of_servers = get_server_wi_ids_from_application(application_id)
    for server_id_ado in list_of_servers: 
        new_row = [server_id_ado, application_wi_id]
        new_df = pd.DataFrame([new_row], columns=cols_map_servers_apps)
        # load data into a DataFrame object:
        df_map_server_vs_app = pd.concat([df_map_server_vs_app, new_df], ignore_index = True)  
    return df_map_server_vs_app






# MAIN
# global storage var
list_of_applications = []
list_of_applications = get_app_list_for_the_wave(list_of_applications)

# display the list of ids of apps
'''
for application in list_of_applications:
    print(application)
'''

# display the table with apps and details
for application_id in list_of_applications: 
    df_applications = save_application_wi_into_data_frame(application_id, df_applications)

# print(df_applications)
df_applications.to_csv('applications_extract.csv')



# get list of servers
# for each server save into df

list_of_servers = get_all_servers_list_from_ado()
for server in list_of_servers:
    df_servers = save_server_wi_into_data_frame(server, df_servers)

# print(df_servers)
df_servers.to_csv('extract_servers.csv')


# map applications with servers
list_of_all_applications = get_all_applications_list_from_ado()
for application_id in list_of_all_applications: 
    df_map_server_vs_app = save_map_server_vs_app(application_id, df_map_server_vs_app)

# print(df_map_server_vs_app)
df_map_server_vs_app.to_csv('extract_map_servers_vs_applications.csv')
