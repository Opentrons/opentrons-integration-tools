# Store a file generated in real time onto a remote SMB server
# For more information, see:
# https://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html

import tempfile
from smb.SMBConnection import SMBConnection


""" SMB network settings """

# The username for the network share
USERNAME = ""
# The password for the network share
PASSWORD = ""
# The NetBIOS name of the Opentrons robot (picked by you)
MY_NAME = ""
# The NetBIOS name of the remote server
REMOTE_NAME = ""
# The IP address of the remote server
REMOTE_IP = ""
# 139 for SMB over NetBIOS (what we are doing here)
PORT = 139
# The name of the shared folder on the remote server
SERVICE_NAME = ""

# How the file will be saved on the remote server
REMOTE_PATH = "/ot_data_results.txt"

""" SMB network actions """

# Set up the SMB connection
connection = SMBConnection(
    username=USERNAME,
    password=PASSWORD,
    my_name=MY_NAME,
    remote_name=REMOTE_NAME,
    use_ntlm_v2=True
    )

assert connection.connect(
    ip=REMOTE_IP,
    port=PORT,
    timeout=10
    )

tmp = tempfile.NamedTemporaryFile()
tmp.write(b'Super useful results')

tmp.seek(0)
connection.storeFile(
    service_name=SERVICE_NAME,
    path=REMOTE_PATH,
    file_obj=tmp,
    timeout=5
    )

""" Followup actions """

# Clean up

tmp.close()