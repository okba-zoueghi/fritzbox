#!/usr/bin/env python3

# Copyright (C) 2024
#
# Author: okba.zoueghi@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import requests
from enum import Enum
from xml.etree import ElementTree as ET
import time

class ConnectionStatus(Enum):
    """Enum for representing connection statuses."""
    CONNECTED = 0
    CONNECTING = 1
    DISCONNECTED = 2
    DISCONNECTING = 3
    PENDING_DISCONNECT = 4
    OTHER_CONNECTION_STATUS = 100

class RequestError(Enum):
    """Enum for representing different request errors."""
    NO_ERROR = 0
    HTTP_ERROR = 1
    CONNECTION_ERROR = 2
    TIMEOUT_ERROR = 3
    OTHER_ERROR = 100

class WANIPConnection:
    def __init__(self):
        self.service_urn = 'urn:schemas-upnp-org:service:WANIPConnection:1'
        self.control_url = '/igdupnp/control/WANIPConn1'
        self.action_GetExternalIPAddress = 'GetExternalIPAddress'
        self.action_ForceTermination = 'ForceTermination'
        self.action_GetStatusInfo = 'GetStatusInfo'

class Fritzbox:
    """Class for interacting with the Fritzbox router via UPnP."""
    def __init__(self, soap_url):
        """
        Initialize Fritzbox with the provided SOAP URL.

        Args:
            soap_url (str): The base URL for the Fritzbox SOAP API.
        """
        self.soap_url = soap_url
        self.WANIPConnection = WANIPConnection()

    @staticmethod
    def create_soap_request(service_urn, action):
        """
        Create SOAP request headers and body for a given action.

        Args:
            action (str): The SOAP action to perform.

        Returns:
            tuple: A tuple containing the headers and body for the SOAP request.
        """
        headers = {
            'SoapAction': f'{service_urn}#{action}',
            'Content-Type': 'text/xml; charset=utf-8'
        }
        body = f"""<?xml version="1.0" encoding="utf-8"?>
            <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                <s:Body>
                    <u:{action} xmlns:u=\"{service_urn}\"/>
                </s:Body>
            </s:Envelope>"""
        return (headers, body)

    def get_public_ip(self):
        """
        Get the public IP address of the Fritzbox.

        Returns:
            tuple: A tuple containing the request error code and the public IP address.
        """
        public_ip = None
        error_code = RequestError.NO_ERROR
        headers, body = Fritzbox.create_soap_request(self.WANIPConnection.service_urn, self.WANIPConnection.action_GetExternalIPAddress)
        try:
            response = requests.post(self.soap_url + self.WANIPConnection.control_url, headers = headers, data = body)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            # Find the tag containing the ExternalIPAddress
            ip_tag = root.find('.//NewExternalIPAddress')
            if ip_tag is not None:
                public_ip = ip_tag.text
            else:
                print("External IP Address not found in response.")

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            error_code = RequestError.HTTP_ERROR
        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            error_code = RequestError.CONNECTION_ERROR
        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
            error_code = RequestError.TIMEOUT_ERROR
        except requests.exceptions.RequestException as req_err:
            print(f'Request exception occurred: {req_err}')
            error_code = RequestError.OTHER_ERROR

        return (error_code, public_ip)

    def get_connection_status(self):
        """
        Get the connection status of the Fritzbox.

        Returns:
            tuple: A tuple containing the request error code and the connection status.
        """
        error_code = RequestError.NO_ERROR
        headers, body = Fritzbox.create_soap_request(self.WANIPConnection.service_urn, self.WANIPConnection.action_GetStatusInfo)
        connection_status = None
        try:
            response = requests.post(self.soap_url + self.WANIPConnection.control_url, headers = headers, data = body)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            # Find the tag containing the ExternalIPAddress
            connection_status_tag = root.find('.//NewConnectionStatus')
            if connection_status_tag is not None:
                if connection_status_tag.text == 'Connected':
                    connection_status = ConnectionStatus.CONNECTED
                elif connection_status_tag.text == 'Connecting':
                    connection_status = ConnectionStatus.CONNECTING
                elif connection_status_tag.text == 'Disconnecting':
                    connection_status = ConnectionStatus.DISCONNECTING
                elif connection_status_tag.text == 'Disconnected':
                    connection_status = ConnectionStatus.DISCONNECTED
                elif connection_status_tag.text == 'PendingDisconnect':
                    connection_status = ConnectionStatus.PENDING_DISCONNECT
                else:
                    connection_status = ConnectionStatus.OTHER_CONNECTION_STATUS

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            error_code = RequestError.HTTP_ERROR
        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            error_code = RequestError.CONNECTION_ERROR
        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
            error_code = RequestError.TIMEOUT_ERROR
        except requests.exceptions.RequestException as req_err:
            print(f'Request exception occurred: {req_err}')
            error_code = RequestError.OTHER_ERROR

        return (error_code, connection_status)


    def change_ip_address(self):
        """
        Change the public IP address by forcing a termination.

        Returns:
            RequestError: The request error code indicating the success or failure of the operation.
        """
        error_code = RequestError.NO_ERROR
        headers, body = Fritzbox.create_soap_request(self.WANIPConnection.service_urn, self.WANIPConnection.action_ForceTermination)
        try:
            response = requests.post(self.soap_url + self.WANIPConnection.control_url, headers = headers, data = body)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            error_code = RequestError.HTTP_ERROR
        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            error_code = RequestError.CONNECTION_ERROR
        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
            error_code = RequestError.TIMEOUT_ERROR
        except requests.exceptions.RequestException as req_err:
            print(f'Request exception occurred: {req_err}')
            error_code = RequestError.OTHER_ERROR

        return error_code

    def change_ip_address_block(self):
        """
        Change the public IP address and wait for reconnection.

        Returns:
            RequestError: The request error code indicating the success or failure of the operation.
        """
        error_code = RequestError.NO_ERROR
        error_code = self.change_ip_address()
        time.sleep(10)
        if error_code == RequestError.NO_ERROR:
            while True:
                error_code, connection_status = self.get_connection_status()
                if error_code != RequestError.NO_ERROR:
                    break
                if connection_status == ConnectionStatus.CONNECTED:
                    print('IP address changed')
                    break
                print('Reconneting pending, status: ', connection_status)
                time.sleep(2)

        return error_code
