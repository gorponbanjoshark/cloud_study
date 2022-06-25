import json
from googleapiclient.discovery import build
from copy import deepcopy
from proto_code.config import *
#
# usage
# from proto_code.templates import *
# the_data = get_json('templates/roving-ssh-ready')
# insert_instance_template(the_data)
# list_all_instance_templates()

def get_json(file_path=None):
    """ just read a local json and return as dict
    """   
    with open(file_path) as fh:
        tempdata = fh.read()
    return json.loads(tempdata)


# lists all instance templates
def list_all_instance_templates():
    """ dump all instance templates.
    :return dump of all templates
    """
    service = build('compute', 'v1')
    instance_template = service.instanceTemplates()
    req = instance_template.list(project=PROJECT)
    return req.execute()


def get_instance_template_names():
    """ just return the name of all instance_templates
    """
    return [item['name'] for item in list_all_instance_templates()['items']]


# inserts a template
def insert_instance_template(data, name=None):
    """ insert an instance template. name must be unique
    :param name: name teh instance template
    :returns: HTTP request response
    
    https://developers.google.com/resources/api-libraries/documentation/compute/v1/python/latest/compute_v1.instanceTemplates.html
    """
    local_data = deepcopy(data)
    if name:
        local_data['name'] = name
    service = build('compute', 'v1')
    instance_template = service.instanceTemplates()
    hey = service.instanceTemplates()
    req = hey.insert(project=PROJECT, body=local_data)
    return req.execute()


def delete_instance_template(name, project=PROJECT):
    """ yeah delete an instance template
    :param name: the name
    :returns: HTTP request response
    """
    service = build('compute', 'v1')
    instance_template = service.instanceTemplates()
    hey = service.instanceTemplates()
    req = hey.delete(project=project, instanceTemplate=name)
    return req.execute()

def update_template(name='roving-ssh-ready'):
    """
    delete and recreate template instance
    :param name: name of template instance. must match filename within templates/
    :returns all instance template names found
    """
    if name in get_instance_template_names():
        delete_instance_template(name)
    the_data = get_json(f'templates/f{name}')
    insert_instance_template(the_data)
    return list_all_instance_templates()

