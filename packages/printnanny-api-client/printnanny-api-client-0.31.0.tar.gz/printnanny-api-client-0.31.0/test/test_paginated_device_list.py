# coding: utf-8

"""
    printnanny-api-client

    Official API client library for print-nanny.com  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Contact: leigh@print-nanny.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import printnanny_api_client
from printnanny_api_client.models.paginated_device_list import PaginatedDeviceList  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestPaginatedDeviceList(unittest.TestCase):
    """PaginatedDeviceList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedDeviceList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.paginated_device_list.PaginatedDeviceList()  # noqa: E501
        if include_optional :
            return PaginatedDeviceList(
                count = 123, 
                next = 'http://api.example.org/accounts/?page=4', 
                previous = 'http://api.example.org/accounts/?page=2', 
                results = [
                    printnanny_api_client.models.device.Device(
                        id = 56, 
                        bootstrap_release = null, 
                        cloudiot_device = null, 
                        cameras = [
                            printnanny_api_client.models.camera.Camera(
                                id = 56, 
                                deleted = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                active = True, 
                                device = 56, 
                                name = 'Raspberry Pi Cam', 
                                camera_type = null, )
                            ], 
                        janus_local_url = '', 
                        dashboard_url = '', 
                        printer_controllers = [
                            printnanny_api_client.models.printer_controller.PrinterController(
                                id = 56, 
                                software = null, 
                                created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                polymorphic_ctype = 56, 
                                user = 56, 
                                device = 56, )
                            ], 
                        release_channel = null, 
                        user = null, 
                        last_task = null, 
                        active_tasks = [
                            printnanny_api_client.models.task.Task(
                                id = 56, 
                                last_status = null, 
                                task_type = 'monitor_start', 
                                active = True, 
                                task_type_display = '', 
                                created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                device = 56, )
                            ], 
                        active_cameras = [
                            printnanny_api_client.models.camera.Camera(
                                id = 56, 
                                deleted = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                active = True, 
                                device = 56, 
                                name = 'Raspberry Pi Cam', 
                                camera_type = null, )
                            ], 
                        monitoring_active = True, 
                        created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        hostname = '', )
                    ]
            )
        else :
            return PaginatedDeviceList(
        )

    def testPaginatedDeviceList(self):
        """Test PaginatedDeviceList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
