# Fritzbox SOAP API Script

This repository contains a Python script to interact with a Fritzbox router using SOAP API. The script allows you to get the public IP address, check the connection status, and force the router to change its IP address.
UPnP shall be enabled in the fritzbox.

http://fritz.box:49000/tr64desc.xml (or \<ip of your fritzbox>:49000/tr64desc.xml) can be used to view the supported SOAP services.

This should work on most fritzbox routers (any fritzbox that supports the service WANIPConnection:1).

This was tested on FRITZ!Box 7530 AX on FRITZ!OS 7.57.

## Functions

- Get the public IP address of the Fritzbox router.
- Check the connection status of the router.
- Force the router to change its IP address.

## Use Cases

Some services typically restrict functionalities based on IP addresses. E.g., https://mega.nz/ restricts the amount of data that can be downloaded based of the IP address. After downloading 5Gbytes https://mega.nz/ disallows the IP address to download futher data.
To be able to download data again, the owner of the IP address shall wait 6 hours. This script can be used to automate changing the IP address of a fritzbox router which allows to bypass the https://mega.nz/ download restriction. The script can be called each time the https://mega.nz/ quota
is exceeded (or each time before starting a download) to allow unlimited download.

For unlimited https://mega.nz/ download using a fritzbox, refer to my other repo: https://github.com/okba-zoueghi/mega-download.git

## Clone and Install Dependencies

Clone:

```shell
git clone https://github.com/okba-zoueghi/fritzbox.git
```

Install python dependencies:

```shell
cd fritzbox
pip install -r requirements.txt
```

## Usage

### Use CLI

Calling the script without argument will use the following fritbox url and port: http://fritz.box:49000

```shell
fritzbox-change-ip.py
```

If your fritzbox has another address, you can use the script as follows:

```shell
fritzbox-change-ip.py --url '<ip of your fritzbox>:<SOAP port>'
```

### Use in a python script

```python
  from fritzbox import RequestError, ConnectionStatus, Fritzbox
  fritzbox = Fritzbox('http://fritz.box:49000')

  # Get and display public IP address
  error_code, public_ip = fritzbox.get_public_ip()
  if error_code == RequestError.NO_ERROR:
      print("Public IP is:", public_ip)
  else:
      print("Failed to get public IP:", error_code)

  # Get and display connection status
  error_code, connection_status = fritzbox.get_connection_status()
  if error_code != RequestError.NO_ERROR:
      print("Connection status:", connection_status)

  # Attempt to change the public IP address
  error_code = fritzbox.change_ip_address_block()
  if error_code == RequestError.NO_ERROR:
      print("Successfully changed IP address.")
  else:
      print("Failed to change IP address:", error_code)
```
