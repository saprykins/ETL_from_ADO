import pandas as pd
import openpyxl







# TCS FILES

df_servers = pd.read_csv('./results/__tcs_servers_extract.csv')
df_apps = pd.read_csv("./results/__tcs_applications_extract.csv")
df_history = pd.read_csv("./results/__tcs_history.csv")
# print(df_apps)

df3 = pd.merge(df_servers,df_apps, on=['App id in ADO'], how = "outer")
df4 = pd.merge(df3, df_history, on=['App id in ADO'])

# print(df4.T)

df_tcs = df4.drop(["Unnamed: 0_x", "Unnamed: 0_y", "App id in ADO"], axis=1)
# df_tcs = df4.drop(["Unnamed: 0_x", "Server id in ADO", "Unnamed: 0_y", "App id in ADO"], axis=1)
# df4=df3.drop([df3.columns[0], df3.columns[1]], axis=1)
# pritn(df_tcs)
# df4.to_csv('./results/__xxx_tcs.csv',index=False)


# for internal usage
df3_outer_join = pd.merge(df_servers,df_apps, on=['App id in ADO'], how = 'outer')
df4_outer_join = df3_outer_join.drop(["Unnamed: 0_x", "Unnamed: 0_y"], axis=1)
# print(df4)



# print(df4)
# df4.to_excel('test.xlsx', sheet_name='tcs')
df4_outer_join.to_excel('./results/ADO_TCS_outer_join.xlsx', sheet_name='tcs_all', index=False)





# MS FILES

df_servers = pd.read_csv('./results/__ms_servers_extract.csv')
df_apps = pd.read_csv("./results/__ms_applications_extract.csv")
df_map = pd.read_csv("./results/__ms_mapping.csv")
df_history = pd.read_csv("./results/__ms_history.csv")

# print(df_servers)
# print(df_apps)
# print(df_map)

df3 = pd.merge(df_servers,df_map, on=['Server id in ADO'])

# df4 = pd.merge(df3,df_apps, on=['App id in ADO'], how = "outer")
df4 = pd.merge(df3,df_apps, on=['App id in ADO'])

df_4c = df4.drop(["Unnamed: 0", "Unnamed: 0_x", "Unnamed: 0_y", "Unnamed: 0"], axis=1)
# df_4c = df4.drop(["Unnamed: 0", "Unnamed: 0_x", "Server id in ADO", "Unnamed: 0_y", "Unnamed: 0"], axis=1)

# df_x.to_csv('./results/__xxx_ms.csv',index=False)




df5 = pd.merge(df_4c, df_history, on=['App id in ADO'])
# print(df5)
# df5.to_csv('./results/__xxx_ms.csv',index=False)



# print(df4)

df_ms = df5.drop(["Unnamed: 0", "Unnamed: 0", "App id in ADO"], axis=1)
# df_ms.to_csv('./results/__xxx_ms.csv',index=False)
#
#
#
# df_ms = df5.drop(["Server id in ADO", "Unnamed: 0_y", "Unnamed: 0", "App id in ADO"], axis=1)
#
#
#


# df_ms = df4.drop(["Unnamed: 0", "Unnamed: 0_x", "Unnamed: 0_y", "Unnamed: 0"], axis=1)
# df4=df3.drop([df3.columns[0], df3.columns[1]], axis=1)
# print(df5)

# df5.to_csv('./results/__ms_extract.csv',index=False)

# df5.to_excel('test-ms.xlsx', sheet_name='ms')


df4_outer_join = pd.merge(df3,df_apps, on=['App id in ADO'], how = "outer")
df5_outer_join = df4_outer_join.drop(["Unnamed: 0", "Unnamed: 0_x", "Unnamed: 0_y", "Unnamed: 0"], axis=1)
df5_outer_join.to_excel('./results/ADO_MS_outer_join.xlsx', sheet_name='ms_all', index=False)
# df5_outer_join.to_csv('./results/__xxx.csv',index=False)




# UNION
# df_tcs = pd.read_csv('./results/__tcs_extract.csv')
# df_ms = pd.read_csv("./results/__ms_extract.csv")
# print(df_tcs)
# print(df_ms)
union_dfs = pd.concat([df_ms, df_tcs])
union_dfs = union_dfs.drop(["Unnamed: 0"], axis=1)
# union_dfs = pd.concat([df_tcs])
# union_dfs.to_csv('ADO_extract.csv',index=False)
# print(union_dfs)
# union_dfs.to_csv('./results/ADO_extract.csv')


# copies for factories
df_tcs.to_excel('./results/ADO_TCS_extract.xlsx', sheet_name='tcs', index=False)
df_ms.to_excel('./results/ADO_MS_extract.xlsx', sheet_name='ms', index=False)

union_dfs.to_excel('./results/ADO_extract.xlsx', sheet_name='total', index=False)
# union_dfs.to_excel('./results/XXX', sheet_name='total', index=False)
