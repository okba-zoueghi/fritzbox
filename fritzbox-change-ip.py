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

import argparse
from fritzbox import RequestError, ConnectionStatus, Fritzbox

def main():
    parser = argparse.ArgumentParser(description='Fritzbox UPnP Control Script')
    parser.add_argument('--url', type=str, default='http://fritz.box:49000', help='The base URL for the Fritzbox SOAP API')
    args = parser.parse_args()

    fritzbox = Fritzbox(args.url)

    # Get and display the current public IP
    error_code, public_ip = fritzbox.get_public_ip()
    if error_code == RequestError.NO_ERROR:
        print("Current IP is:", public_ip)
    else:
        print("Failed to get public IP:", error_code)

    # Attempt to change the public IP address
    error_code = fritzbox.change_ip_address_block()
    if error_code == RequestError.NO_ERROR:
        print("Successfully changed IP address.")
    else:
        print("Failed to change IP address:", error_code)
        return

    # Get and display the new public IP
    error_code, public_ip = fritzbox.get_public_ip()
    if error_code == RequestError.NO_ERROR:
        print("New IP is:", public_ip)
    else:
        print("Failed to get new public IP:", error_code)

main()
