# File Sharing with SMB

### Introduction

Server Message Block (SMB) is a convenient way to share files between computers on the same local area network (LAN). One way to do this that is compatible with the Opentrons software is [pysmb](https://miketeo.net/blog/projects/pysmb).

### SMB Server Setup

With this library, another computer on your LAN has to act as the remote SMB server. This means that one or more files or folders on that computer will be shared on the network, and the Opentrons robot can retrieve them and optionally store files there.

Your SMB setup will depend on the operating system of your server computer. This is the setup for Windows:

[Create a local user or administrator account in Windows](https://support.microsoft.com/en-us/windows/create-a-local-user-or-administrator-account-in-windows-20de74e0-ac7f-3502-a866-32915af2a34d)

[File sharing over a network in Windows](https://support.microsoft.com/en-us/windows/file-sharing-over-a-network-in-windows-b58704b2-f53a-4b82-7bc1-80f9994725bf)

The "local account" that you create is actually the credentials for the network share: you set this username and password in Python in order to access the share. If you want to store files on the server as well as retrieve them, you will need to give read/write access to the account. In addition to the instructions above, you may also need to set "Properties"->"Sharing"->"Advanced Sharing" for the files/folders to share.

### Opentrons Software Setup

Using SSH or the Jupyter Notebook terminal, install pysmb with pip:
`pip install pysmb`

### Using pysmb
This repository contains three examples that show how to use pysmb to retrieve and store files. This code can easily be wrapped in an Opentrons Python protocol. These examples also work with larger and more complicated types of files, like photos.

### More Resources
https://pypi.org/project/pysmb/

https://pysmb.readthedocs.io/en/latest/index.html

https://en.wikipedia.org/wiki/Server_Message_Block
