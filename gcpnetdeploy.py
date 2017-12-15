"""Deploy Networks"""
#! /usr/bin/python2.7

#Copyright 2017 lawny.co

import argparse
import time
from six.moves import input
import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
CREDENTIALS = GoogleCredentials.get_application_default()

COMPUTE = googleapiclient.discovery.build('compute', 'v1')

 #[START list_networks]
def list_networks(compute, project):
    """ list the available networks in the project """
    result = compute.networks().list(project=project).execute()
    return result['items']
# [END list_networks]

# [START create_external_network]
def create_external_network(compute, project):
    """ Create the new external network """
    network_body = {
        'name': 'devopsExternal',
        'description': 'External network for devops stack',
        'IPv4Range': '172.100.10.0/28',
        'gatewayIPv4': '172.100.10.1',
        'autoCreateSubnetworks': False,
        'routingConfig': {
            'routingMode': 'REGIONAL'
        }
    }

    return compute.networks().insert(
        project=project,
        body=network_body).execute()
# [END create_external_network]

# [START create_mgmt_network]
def create_mgmt_network(compute, project):
    """ Create the new management network """
    network_body = {
        'name': 'devopsMgmt',
        'description': 'Management network for devops stack',
        'IPv4Range': '192.100.10.0/28',
        'gatewayIPv4': '192.100.10.1',
        'autoCreateSubnetworks': False,
        'routingConfig': {
            'routingMode': 'REGIONAL'
        }
    }

    return compute.networks().insert(
        project=project,
        body=network_body).execute()
# [END create_mgmt_network]

# [START create_internal_network]
def create_internal_network(compute, project):
    """ Create the new internal network """
    network_body = {
        'name': 'devopsInternal',
        'description': 'Internal network for devops stack',
        'IPv4Range': '10.100.10.0/28',
        'gatewayIPv4': '10.100.10.1',
        'autoCreateSubnetworks': False,
        'routingConfig': {
            'routingMode': 'REGIONAL'
        }
    }

    return compute.networks().insert(
        project=project,
        body=network_body).execute()
# [END create_internal_network]

# [START wait_for_operation]
def wait_for_operation(compute, project, operation):
    """ Check the status of the current operation """
    print 'Waiting for operation to finish...'
    while True:
        result = compute.zoneOperations().get(
            project=project,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print "done."
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]

# [START Build the networks]
def main(project, wait=False):
    """ Execution of the steps """
    compute = googleapiclient.discovery.build('compute', 'v1')

    print 'Creating external network...'

    operation = create_external_network(compute, project)
    wait_for_operation(compute, project, operation['name'])

    print 'Creating Mangement network...'

    operation = create_mgmt_network(compute, project)
    wait_for_operation(compute, project, operation['name'])

    print 'Creating Internal network...'

    operation = create_internal_network(compute, project)
    wait_for_operation(compute, project, operation['name'])

    networks = list_networks(compute, project)

    print 'Networks in project %s:' % (project)
    for network in networks:
        print ' - ' + network['name']

    print """
Networks created.
"""
    if wait:
        input()

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    PARSER.add_argument('project_id', help='Your Google Cloud project ID.')

    ARGS = PARSER.parse_args()

    main(ARGS.project_id)
# [END Build the Networks]
