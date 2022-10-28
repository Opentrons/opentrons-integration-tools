# Google Sheets
There is a great Python package called [gspread](https://pypi.org/project/gspread/) that lets you access values that are in a Google Sheets spreadsheet. This can be a very convenient way to pass variables or data to your protocol.
### One-time Setup
1. Install the package on the Opentrons system with `pip install gspread`.

2. Follow the instructions here to set up a Google service account: https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
### Example Protocol
The protocol here shows how you can get variables that are stored in a spreadsheet. It is also possible to use gspread to create and edit spreadsheets.
