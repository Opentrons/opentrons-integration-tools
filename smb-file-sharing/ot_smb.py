# pysmb wrapper that retrieves files from/stores files to an SMB server
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


""" SMB network actions """

# Set up the SMB connection
def smb_connect():
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

    return connection


# Retrieve a file from the SMB server
def smb_get_file(remote_path, local_path):
    connection = smb_connect()

    # Get the file from the server
    tmp = tempfile.NamedTemporaryFile()
    file_attributes, filesize = connection.retrieveFile(
        service_name=SERVICE_NAME,
        path=remote_path,
        file_obj=tmp
        )

    # Write the file to the local disk
    outfile = open(local_path, "wb")
    tmp.seek(0)
    # You could also directly use the contents here
    contents = tmp.read()
    outfile.write(contents)

    # Clean up
    tmp.close()
    outfile.close()


# Store an existing file on disk on the SMB server
def smb_store_file(remote_path, local_path):
    connection = smb_connect()

    tmp = open(local_path, "rb")

    connection.storeFile(
        SERVICE_NAME,
        remote_path,
        tmp,
        timeout=5
        )

    # Clean up
    tmp.close()


# Store a string variable as a file on the SMB server
def smb_store_value(remote_path, local_value):
    connection = smb_connect()

    # Make sure value is a string first
    my_value_str = str(local_value)

    # Convert string to bytes for tempfile write() function
    my_value_b = my_value_str.encode()

    tmp = tempfile.NamedTemporaryFile()
    tmp.write(my_value_b)

    tmp.seek(0)
    connection.storeFile(
        SERVICE_NAME,
        remote_path,
        tmp,
        timeout=5
        )

    # Clean up
    tmp.close()
