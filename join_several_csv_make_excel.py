import pandas as pd
import openpyxl

df_servers = pd.read_csv('tcs_servers_extract.csv')
df_apps = pd.read_csv("tcs_applications_extract.csv")

# print(df_apps)

df3 = pd.merge(df_servers,df_apps, on=['App id in ADO'])
# print(df3)

df4=df3.drop(["Unnamed: 0_x", "Server id in ADO", "Unnamed: 0_y", "App id in ADO"], axis=1)
# df4=df3.drop([df3.columns[0], df3.columns[1]], axis=1)
# print(df4)

# df4.to_csv('test.csv')
df4.to_excel('test.xlsx', sheet_name='tcs')
