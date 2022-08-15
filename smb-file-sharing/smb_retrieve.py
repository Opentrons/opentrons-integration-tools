# Retrieve a file from a remote SMB server and write it to the Opentrons
# robot's storage
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

# The name and path of the file on the remote server
REMOTE_PATH = "/ot_protocol_input.txt"
# How the file will be saved to the Opentrons robot
LOCAL_PATH = "/var/lib/jupyter/notebooks/smb/protocol_input.txt"

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

# Get the file from the server
tmp = tempfile.NamedTemporaryFile()
file_attributes, filesize = connection.retrieveFile(
    service_name=SERVICE_NAME,
    path=REMOTE_PATH,
    file_obj=tmp
    )

""" Followup actions """

# Write the file to the local disk
outfile = open(LOCAL_PATH, "wb")
tmp.seek(0)
# You could also directly use the contents here
contents = tmp.read()
outfile.write(contents)

# Clean up
tmp.close()
outfile.close()