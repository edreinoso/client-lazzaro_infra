import boto3
import json
import os


# Global vars: boto3 init
cw_client = boto3.client('cloudwatch')

class cwd_service():

    def create_client_dashboard(self):
        """
          dashboard per client
        """
        pass
    
    def append_client_compute(self, dhb_name):
        """
          dashboard overview, all clients
        """
        self.dhb_name = dhb_name
        response = cw_client.get_dashboard(
            DashboardName=dhb_name
        )

        widgets = json.loads(response['DashboardBody'])

        new_client_widget = {
            "type":"metric",
            "x":0,
            "y":0,
            "width":8,
            "height":3,
            "properties":{
            "sparkline":True,
            "view":"singleValue",
            "metrics":[
                [
                    "AWS/ECS",
                    "MemoryUtilization",
                    "ServiceName",
                    client,
                    "ClusterName",
                    cluster
                ],
                [
                    ".",
                    "CPUUtilization",
                    ".",
                    ".",
                    ".",
                    "."
                ]
            ],
            "region":"eu-central-1",
            "title":client
            }
        }

        widgets['widgets'].append(new_client_widget)

        # append client info in the file
        cw_client.put_dashboard(
            DashboardName=dhb_name,
            DashboardBody=json.dumps(widgets)
        )