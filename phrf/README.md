Processing PHRF fleet data to predict PHRF ratings

Steps as follows:
- Obtain the latest PHRF fleet data from the PHRF website 
- Convert the data to a XLS file using Adobe Reader "Save as Excel" feature
- Add macro from [clean-xls.vb](clean-xls.vb) to the XLS file
- Run this macro to clean up the data
- Create [sun_dragon.csv](data%2Fsun_dragon.csv) with boat parameters
- Use the cleaned up xlsm file as input to the [read_fleet_roster.py](read_fleet_roster.py) script

