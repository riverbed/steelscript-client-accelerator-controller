#!/usr/bin/env python
'''
' Riverbed Community SteelScript
'
' CAC_rest_api.py
'
' Encoding: UTF8
' End of Line Sequence: LF
'
' Copyright (c) 2021 Riverbed Technology, Inc.
'
' This software is licensed under the terms and conditions of the MIT License
' accompanying the software ("License").  This software is distributed "AS IS"
' as set forth in the License.
'''


"""
This script presents a python example of using Command Line Interface (CLI)
to show services and license of a Client Accelerator appliance.
This example script should be executed as follows:
cac_rest_api.py <HOST> [-c access_code]
"""

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

import logging, sys
from steelscript.common.app import Application
from steelscript.common.service import OAuth
from steelscript.common import Service


class ClientAcceleratorControllerCLIApp(Application):
    def add_positional_args(self):
        self.add_positional_arg('host', 'Client Accelerator hostname or IP address')

    def add_options(self, parser):
        super(ClientAcceleratorControllerCLIApp, self).add_options(parser)

        parser.add_option('-c', '--oauth', help="access_code to connect to the api")

    def validate_args(self):
        super(ClientAcceleratorControllerCLIApp, self).validate_args()

        if not self.options.oauth:
            self.parser.error("Access_code needs to be specified")

    def main(self):
        
        cac = Service("appliance", self.options.host, auth=OAuth(self.options.oauth))

        print("\n********** Services **********\n")
        path = '/api/appliance/1.0.0/services'
        content_dict = cac.conn.json_request('GET', path)
        print(content_dict)

        print("\n********** License **********\n")
        path = '/api/appliance/1.0.0/status/license'
        content_dict=cac.conn.json_request('GET', path)
        print(content_dict)

        del cac

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    ClientAcceleratorControllerCLIApp().run()
