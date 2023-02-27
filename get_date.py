import pandas as pd
# import openpyxl

df = pd.read_csv('./results/__afa_dates.csv')

def get_mig_date(playbook_id):
    date = df.loc[df["Mig pm WI"] == playbook_id, "Mig date"]
    # print(date[0])
    return date[0]

print(get_mig_date(137834))
