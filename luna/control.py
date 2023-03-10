#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control Class for the CLI
"""
__author__      = "Sumit Sharma"
__copyright__   = "Copyright 2022, Luna2 Project [CLI]"
__license__     = "GPL"
__version__     = "2.0"
__maintainer__  = "Sumit Sharma"
__email__       = "sumit.sharma@clustervision.com"
__status__      = "Production"

from multiprocessing import Process, Queue
from luna.utils.helper import Helper
from luna.utils.presenter import Presenter
from luna.utils.rest import Rest
from luna.utils.log import Log

class Control():
    """
    Control class is a power control area.
    It is responsible to perform all power related
    operations on the Nodes.
    """

    def __init__(self, args=None):
        self.logger = Log.get_logger()
        self.args = args
        self.route = "control"
        self.action = "power"
        if self.args["power"] and self.args["action"]:
            self.logger.debug(f'Arguments Supplied => {self.args}')
            if self.args["action"] == "status":
                self.power_status()
            elif self.args["action"] == "on":
                self.power_on()
            elif self.args["action"] == "off":
                self.power_off()
            else:
                Helper().show_error("Not a valid option.")
        else:
            Helper().show_error("Select a service and action to be performed, See with -h.")


    def getarguments(self, parser, subparsers):
        """
        Method will provide all the arguments
        related to the Control Process class.
        """
        control_menu = subparsers.add_parser('control', help='Control Nodes.')
        control_args = control_menu.add_subparsers(dest='power')
        power_parser = control_args.add_parser('power', help='Power Operations')
        power_menu = power_parser.add_subparsers(dest='action')
        ## >>>>>>> Control Command >>>>>>> status
        status_parser = power_menu.add_parser('status', help='Status of Node(s)')
        status_parser.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        status_parser.add_argument('node', help='Node Name or Node Hostlist')
        ## >>>>>>> Control Command >>>>>>> on
        on_parser = power_menu.add_parser('on', help='Power On Node(s)')
        on_parser.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        on_parser.add_argument('node', help='Node Name or Node Hostlist')
        ## >>>>>>> Control Command >>>>>>> of
        off_parser = power_menu.add_parser('off', help='Power Off Node(s)')
        off_parser.add_argument('-d', '--debug', action='store_true', help='Get debug log')
        off_parser.add_argument('node', help='Node Name or Node Hostlist')
        return parser


    def power_status(self):
        """
        This method provide the status of one or more nodes.
        """
        http_code = 000
        http_response = None
        response = False
        node_status = {}
        if self.args['node']:
            hostlist = Helper().get_hostlist(self.args['node'])
            if len(hostlist) == 1:
                uri = f'{self.action}/{self.args["node"]}/{self.args["action"]}'
                result = Rest().get_raw(self.route, uri)
                http_code = result.status_code
                http_response = result.json()
            elif len(hostlist) > 1:
                uri = f'{self.route}/{self.action}'
                payload = {"control": {"power": {self.args["action"]: {"hostlist": self.args['node'] } } } }
                result = Rest().post_raw(uri, payload)
                http_code = result.status_code
                http_response = result.json()
                
                
                def dig_data(code=None, request_id=None, count=None):
                    import time
                    # time.sleep(2)
                    uri = f'control/status/{request_id}'
                    response = Rest().get_raw(uri)
                    code = response.status_code
                    http_response = response.json()
                    if code == 200:
                        count, status = Helper().control_print(count, http_response)
                        return dig_data(code, request_id, count)
                    elif code == 400:
                        print("All Done")
                        return True
                    else:
                        print(f"Something Went Wrong {code}")
                        return False

                
                
                request_id = None
                if http_code == 200:
                    if 'request_id' in http_response['control']['power']:
                        count, filter = Helper().control_print(1, http_response)
                        request_id = http_response['control']['power']['request_id']
                        check = dig_data(http_code, request_id, count)
                        print(f'checking {check}')


                # if REQID:
                # NESTED(CODE):
                #     SLEEP(2)
                #     CALL: GET_RAW TIll CODE == 200
                #     PRINT TABLE
                #     IF CODE == 200:
                #         RETURN NESTED(CODE)
                #     ELIF CODE == 400:
                #         RETURN True
                #     ELSE:
                #         RETURN False
                

                # CHECK = NESTED(200)

                # if http_code == 200:
                #     if 'request_id' in http_response['control']['power']:
                #         request_id = http_response['control']['power']['request_id']
                #         print(request_id)
                #         print(http_response)
                #         queue = Queue()
                #         process = Process(target=Helper().control_status, args=(queue, request_id, node_status))
                #         process.start()
                #         print(f"Schedule job status ====>>> {process.is_alive()}")

                #         if process.is_alive():
                #             print(f"Job queue status ====>>> {queue.get()}")
                #         result = {"message": "Ansible Installation is Running."}



                    # if 'control' in http_response:
                    #     if http_response['control']['power']['failed']['hostlist']:
                    #         node_status['failed'] = http_response['control']['power']['failed']['hostlist']
                            # hostlist = http_response['control']['power']['failed']['hostlist'].split(',')
                            # for node in hostlist:
                            #     # node_status[node] = 'failed'
                            #     node_status['failed'] = node
                                # node_status['node'].append(node)
                                # node_status['status'].append('failed')





            # num = 1
            # node = 'node001'
            # status = 'ON'
            # header = f'| S.No.|     Node Name      |       Status      |'
            # # line = f'| {num}    |     {node}         |       {status}    |'
            # line = '| {}    |     {}         |       {}    |'
            # print('-------------------------------------------------')
            # print(header)
            # print('-------------------------------------------------')
            # for x in range(20):
            #     print(line.format(x, f'node00{x}', status))
            # print('-------------------------------------------------')




            else:
                print("Incorrect host list")
            # print(len(hostlist))
            # print(uri)
            # print(http_code)
            # print(http_response)
        # print(node_status)
        # self.logger.debug(f'Service URL => {uri}')
        # result = Rest().get_raw(self.route, uri)
        # self.logger.debug(f'Response => {result}')
        # if result:
        #     http_code = result.status_code
        #     result = result.json()
        #     result = result['service'][self.args["service"]]
        #     if http_code == 200:
        #         response = Helper().show_success(f'{self.args["action"]} performed on {self.args["service"]}')
        #         Helper().show_success(f'{result}')
        #     else:
        #         Helper().show_error(f'HTTP error code is: {http_code} ')
        #         Helper().show_error(f'{result}')
        return response


    def power_on(self):
        """
        This method power on one or more nodes.
        """
        response = False
        uri = f'{self.route}/{self.action}'
        self.logger.debug(f'Service URL => {uri}')
        result = Rest().get_raw(self.route, uri)
        self.logger.debug(f'Response => {result}')
        if result:
            http_code = result.status_code
            result = result.json()
            result = result['service'][self.args["service"]]
            if http_code == 200:
                response = Helper().show_success(f'{self.args["action"]} performed on {self.args["service"]}')
                Helper().show_success(f'{result}')
            else:
                Helper().show_error(f'HTTP error code is: {http_code} ')
                Helper().show_error(f'{result}')
        return response


    def power_off(self):
        """
        This method power off one or more nodes.
        """
        response = False
        uri = f'{self.route}/{self.action}'
        self.logger.debug(f'Service URL => {uri}')
        result = Rest().get_raw(self.route, uri)
        self.logger.debug(f'Response => {result}')
        if result:
            http_code = result.status_code
            result = result.json()
            result = result['service'][self.args["service"]]
            if http_code == 200:
                response = Helper().show_success(f'{self.args["action"]} performed on {self.args["service"]}')
                Helper().show_success(f'{result}')
            else:
                Helper().show_error(f'HTTP error code is: {http_code} ')
                Helper().show_error(f'{result}')
        return response