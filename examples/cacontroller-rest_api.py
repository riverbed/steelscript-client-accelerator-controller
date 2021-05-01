#!/usr/bin/env python
'''
' Riverbed Community SteelScript
'
' cacontroller-rest_api.py
'
' Encoding: UTF8
' End of Line Sequence: LF
'
' Description
' 
'     The script shows how to connect to the REST API of a Client Accelerator Controller appliance.
'     It uses the SteelScript service framework to connect and then call GET method to fetch services and licenses of the appliance
'
' Usage:
'     
'    python cacontroller-rest_api.py {cacontroller_fqdn or ip} --access_code {access_code}
'
' Copyright (c) 2021 Riverbed Technology, Inc.
' This software is licensed under the terms and conditions of the MIT License accompanying the software ("License").  This software is distributed "AS IS" as set forth in the License.
'''

import logging, sys

from steelscript.common.app import Application
from steelscript.common.service import OAuth
from steelscript.common import Service


class ClientAcceleratorControllerCLIApp(Application):
    def add_positional_args(self):
        self.add_positional_arg('host', 'Client Accelerator hostname or IP address')

    def add_options(self, parser):
        super(ClientAcceleratorControllerCLIApp, self).add_options(parser)

        parser.add_option('--access_code', help="access_code to connect to the api")

    def validate_args(self):
        super(ClientAcceleratorControllerCLIApp, self).validate_args()

        if not self.options.access_code:
            self.parser.error("Access_code needs to be specified")

    def main(self):

        cacontroller = Service("cacontroller", self.options.host,
        enable_auth_detection=False,
        supports_auth_basic=False,supports_auth_oauth=True,
        auth=OAuth(self.options.access_code),
        override_auth_info_api='/api/common/1.0.0/auth_info',
        override_oauth_token_api= '/api/common/1.0.0/oauth/token',
        override_services_api='/api/appliance/1.0.0/services'
        )

        print("\n********** Services **********\n")
        path = '/api/appliance/1.0.0/services'
        content_dict = cacontroller.conn.json_request('GET', path)
        print(content_dict)

        print("\n********** License **********\n")
        path = '/api/appliance/1.0.0/status/license'
        content_dict=cacontroller.conn.json_request('GET', path)
        print(content_dict)

        del cacontroller

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    ClientAcceleratorControllerCLIApp().run()
