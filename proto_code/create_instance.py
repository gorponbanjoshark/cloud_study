#from google.cloud.compute_v1 import InstanceTemplate
#with open('templates/instance-test1') as fh:
#    tempdata = fh.read()
#mytemp = InstanceTemplate.from_json(tempdata, ignore_unknown_fields=True)

# lists all instance templates
from googleapiclient.discovery import build
service = build('compute', 'v1')
instance_template = service.instanceTemplates()
req = instance_template.list(project='dopest-project-ever-351102')
response = req.execute()
response
