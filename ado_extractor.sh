#!/bin/sh
source ./venv/bin/activate

ACCOUNT_KEY="1***"

rm -f ./results/*.csv
rm -f ./results/*.xlsx
python _ms_etl_app_w_dates_end_date.py
python _tcs_etl_app_w_dates_enddate.py
python get_ms_history.py
python get_tcs_history.py
python _read_csv.py
python replace_columns.py


# sends files to Azure azuredevops-fs
az storage file upload --account-name azuredevopsblobstorage --account-key $ACCOUNT_KEY --share-name azuredevops-fs --source results/ADO_TCS_extract.xlsx
az storage file upload --account-name azuredevopsblobstorage --account-key $ACCOUNT_KEY --share-name azuredevops-fs --source results/ADO_MS_extract.xlsx

az storage file upload --account-name azuredevopsblobstorage --account-key $ACCOUNT_KEY --share-name azuredevops-fs --source results/ADO_TCS_outer_join.xlsx
az storage file upload --account-name azuredevopsblobstorage --account-key $ACCOUNT_KEY --share-name azuredevops-fs --source results/ADO_MS_outer_join.xlsx

az storage file upload --account-name azuredevopsblobstorage --account-key $ACCOUNT_KEY --share-name azuredevops-fs --source results/ADO_extract.xlsx
