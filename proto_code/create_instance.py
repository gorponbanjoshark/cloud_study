import json
from googleapiclient.discovery import build
from copy import deepcopy

# usage
# from proto_code.create_instance import *
# the_data = get_json('templates/instance-test1')
# insert_instance_template(the_data, 'new-delete-me')
# list_all_instance_templates()


def get_json(file_path=None):
    """ just read a local json and return as dict
    """   
    with open('templates/instance-test1') as fh:
        tempdata = fh.read()
    return json.loads(tempdata)

# lists all instance templates
def list_all_instance_templates():
    """ dump all instance templates.
    :return dump of all templates
    """
    service = build('compute', 'v1')
    instance_template = service.instanceTemplates()
    req = instance_template.list(project='dopest-project-ever-351102')
    return req.execute()

# inserts a template
def insert_instance_template(data, name=None):
    """ insert an instance template. name must be unique
    :param name: name teh instance template
    :returns: HTTP request response
    """
    local_data = deepcopy(data)
    if name:
        local_data['name'] = name
    service = build('compute', 'v1')
    instance_template = service.instanceTemplates()
    hey = service.instanceTemplates()
    req = hey.insert(project='dopest-project-ever-351102', body=local_data)
    return req.execute()
