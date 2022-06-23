from google.cloud.compute_v1 import InstanceTemplate
with open('templates/instance-test1') as fh:
    tempdata = fh.read()
mytemp = InstanceTemplate.from_json(tempdata, ignore_unknown_fields=True)

