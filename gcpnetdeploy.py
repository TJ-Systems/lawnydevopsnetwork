#! /usr/bin/python2.7
"""Deploy Networks"""

#Copyright 2017 lawny.co

import argparse
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
        'name': 'devops-external',
        'description': 'External network for devops stack',
        'IPv4Range': '172.16.10.0/28',
        'gatewayIPv4': '172.16.10.1',
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
        'name': 'devops-mgmt',
        'description': 'Management network for devops stack',
        'IPv4Range': '192.168.10.0/28',
        'gatewayIPv4': '192.168.10.1',
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
        'name': 'devops-internal',
        'description': 'Internal network for devops stack',
        'IPv4Range': '10.100.10.0/28',
        'gatewayIPv4': '10.100.10.1',
        'routingConfig': {
            'routingMode': 'REGIONAL'
        }
    }

    return compute.networks().insert(
        project=project,
        body=network_body).execute()
# [END create_internal_network]

# [START Build the networks]
def main(project, wait=False):
    """ Execution of the steps """
    compute = googleapiclient.discovery.build('compute', 'v1')

    print 'Creating external network...'

    create_external_network(compute, project)

    print 'Creating Mangement network...'

    create_mgmt_network(compute, project)

    print 'Creating Internal network...'

    create_internal_network(compute, project)

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
