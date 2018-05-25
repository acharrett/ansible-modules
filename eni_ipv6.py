#!/usr/bin/python
# Module for enaling IPv6 on an AWS EC2 ENI
#
# Example usage:
#  - name: Enable IPv6 on the ENI
#    eni_ipv6:
#      region: "us-east-1"
#      network_interface: "eni-abczyx"
#    register: eni_ipv6

from ansible.module_utils.basic import *
import boto3

def main():
    fields = {
        "region": {"required": True, "type": "str"},
        "network_interface": {"required": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    region_name = module.params['region']
    eni_id = module.params['network_interface']

    ec2_resource = boto3.resource('ec2', region_name=region_name)
    ec2_client = boto3.client('ec2', region_name=region_name)
    network_interface = ec2_resource.NetworkInterface(eni_id)
    changed = False

    if len(network_interface.ipv6_addresses) == 0:
        ec2_client.assign_ipv6_addresses(NetworkInterfaceId=eni_id,Ipv6AddressCount=1)
        changed=True

    network_interface = ec2_client.describe_network_interfaces(NetworkInterfaceIds = [ eni_id ])
    output = network_interface['NetworkInterfaces'][0]

    module.exit_json(changed=changed, eni=output)

if __name__ == '__main__':
    main()
