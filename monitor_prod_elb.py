#!/usr/bin/env python
#######################################################################################################################
#                                                                                                                     #
# THIS SCRIPT IS TO CHECK IF THE EC2 INSTANCE IS UNREGISTERED FROM THE EC2 ELASTIC LOAD BALANCER AND COUNT GOES BELOW #
# 2 PERIODICALLY.                                                                                                     #
# VERSION 1.0                                                                                                         #
# USAGE:                                                                                                              #
#       monitor_prod_elb.py                                                                                     #
#                                                                                                                     #
#######################################################################################################################
import boto3
import time
from pprint import pprint

import sys
import subprocess
import time
import os


class AwsElbAPI(object):
    """
    This is to create the multiple aws instances on specified subnets
    """

    def __init__(self, load_balancer_name, instance_id_list, filename):
        """
        To initialize the aws loadbalancer client to perform the operations on it.
        :param load_balancer_name:
        :param instance_id_list:
        """
        AWS_ACCESS_KEY_ID='<>'
        AWS_SECRET_ACCESS_KEY='<>'
        self.elb_client = boto3.client('elb',aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-west-2')
        self.load_balancer_name = load_balancer_name
        self.instance_id_list = instance_id_list
        self.filename = filename


    def describe_and_validate_loadbalancer_details(self):
        """
        To Check if the required instance(s) in aws ELB stays inService all the time. If it goes OutOfServices, This will send an alert to the group for the action.
        :return:
        """
        mailto = 'ElastAlertMonitorAll@aeris.net'
        if self.load_balancer_name is None:
            raise ValueError("Missing the aws loadbalancer value....")
        print("*************** ELB Details ******************")
        for instance in self.instance_id_list:
            available_instance_in_elb.append(instance)
            instance_health = self.elb_client.describe_instance_health(LoadBalancerName=self.load_balancer_name, Instances=[ { 'InstanceId': instance  }, ])
            if instance_health['InstanceStates'][0]['State'] == 'OutOfService':
                sub = "Subject: [ALERT] - Avnet production instance is outofservice \n\n"
                text = "Out of 2 instances(%s), one of the instance %s is now OutOfService from %s " % (self.instance_id_list[:], instance, self.load_balancer_name)
                with open(self.filename, 'a') as message:
                    message.write(sub)
                    message.write(text)
                print("[Instance %s is now OutOfService from %s " % (instance, self.load_balancer_name))
                # send mail
                cmd = '/usr/sbin/sendmail -f app-prod@gmail.com %s < /opt/devops/cron/message.file' % (mailto)
                os.system(cmd)
                break
            print("Instance %s is still InServices state for %s " % (instance, self.load_balancer_name))
        if os.path.exists('/opt/devops/cron/message.file'):
            os.remove('/opt/devops/cron/message.file')
            

def main():

    # parallel aws instanceID
    instance_id_list = ['i-gfg46571', 'i-e473jdts632407']

    # parallel aws ELB name
    load_balancer_name = 'MY-APP-PROD-ELB'

    # Test filename
    filename = '/opt/devops/cron/message.file'

    # elb object
    elb_operation = AwsElbAPI(load_balancer_name, instance_id_list, filename)

    # describe the details of elastic load balancer
    elb_operation.describe_and_validate_loadbalancer_details()


# Main execution point
if __name__ == '__main__':
    main()
