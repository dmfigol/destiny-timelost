## Python app to process data from spreadsheet with Timelost data
Python 3.7+ 
Setup environment variables: `GOOGLE_SHEET_KEY` (API key) and `GOOGLE_SHEET_ID`.  
Master sheet has ID (but access is currently restricted): `1f0V0VWWMOFWPLN4Yf-mHd2juh1X2EBboMr2YQsIzgps`  
Older version: `1Wr7c_ZOSabDx145B867KNv4qBpBH1pKHV55_UQXd_3w`  
[poetry](https://github.com/python-poetry/poetry) is being used for dependency management, which are installed using
`poetry install`  
To run the script, execute: `poetry run python main.py`

### Output

Creates file `clusters.txt` which contains the cluster of nodes connected to each other. `**` shows connecting side, `-` shows open side.
Check example of the written file in `output/clusters.txt` in the repository.