import pandas as pd
import openpyxl



# TCS FILES

df_servers = pd.read_csv('__tcs_servers_extract.csv')
df_apps = pd.read_csv("__tcs_applications_extract.csv")

# print(df_apps)

df3 = pd.merge(df_servers,df_apps, on=['App id in ADO'], how = "outer")
# print(df3)

df4=df3.drop(["Unnamed: 0_x", "Server id in ADO", "Unnamed: 0_y", "App id in ADO"], axis=1)
# df4=df3.drop([df3.columns[0], df3.columns[1]], axis=1)
# print(df4)

df4.to_csv('__tcs_extract.csv',index=False)
# print(df4)
# df4.to_excel('test.xlsx', sheet_name='tcs')



# MS FILES

df_servers = pd.read_csv('__ms_servers_extract.csv')
df_apps = pd.read_csv("__ms_applications_extract.csv")
df_map = pd.read_csv("__ms_mapping.csv")

# print(df_servers)
# print(df_apps)
# print(df_map)

df3 = pd.merge(df_servers,df_map, on=['Server id in ADO'])
df4 = pd.merge(df3,df_apps, on=['App id in ADO'], how = "outer")
# print(df4)

df5 = df4.drop(["Unnamed: 0", "Unnamed: 0_x", "Server id in ADO", "Unnamed: 0_y", "Unnamed: 0", "App id in ADO"], axis=1)
# df4=df3.drop([df3.columns[0], df3.columns[1]], axis=1)
# print(df5)

df5.to_csv('__ms_extract.csv',index=False)
# df5.to_excel('test-ms.xlsx', sheet_name='ms')



# UNION
df_tcs = pd.read_csv('__tcs_extract.csv')
df_ms = pd.read_csv("__ms_extract.csv")
# print(df_tcs)
# print(df_ms)
union_dfs = pd.concat([df_ms, df_tcs])
# union_dfs.to_csv('ADO_extract.csv',index=False)
# print(union_dfs)
# union_dfs.to_csv('ADO_extract.csv')
union_dfs.to_excel('ADO_extract.xlsx', sheet_name='total', index=False)
