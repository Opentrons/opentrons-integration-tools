# Store a file from the Opentrons robot's storage onto a remote SMB server
# For more information, see:
# https://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html

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

# The file on the Opentrons robot to store
LOCAL_PATH = "/var/lib/jupyter/notebooks/smb/protocol_results.txt"
# How the file will be saved on the remote server
REMOTE_PATH = "/ot_protocol_results.txt"


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

tmp = open(LOCAL_PATH, "rb")

connection.storeFile(
	service_name=SERVICE_NAME,
	path=REMOTE_PATH,
	file_obj=tmp,
	timeout=5
	)

""" Followup actions """

# Clean up
tmp.close()