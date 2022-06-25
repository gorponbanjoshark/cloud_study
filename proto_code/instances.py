# instances.py
# manage VM instance thingies
from proto_code.config import *
import json
from googleapiclient.discovery import build
from copy import deepcopy

def list_instances(project=PROJECT, zone=ZONE, names_only=False):
    """
    list instances of VMs
    :param project: gcp project
    :param zone: gcp zone
    :param names_only: just produce list of VM instance names
    """
    service = build('compute', 'v1')
    instances = service.instances()
    req = instances.list(project=project, zone=zone)
    response = req.execute()
    if names_only:
        return [item['name'] for item in response['items']]
    return response


def delete_instance(name, project=PROJECT, zone=ZONE):
    """ yeah delete an instance template
    :param name: the name
    :returns: HTTP request response
    """
    service = build('compute', 'v1')
    instances = service.instances()
    req = instances.delete(project=project, zone=zone, instance=name)
    return req.execute()