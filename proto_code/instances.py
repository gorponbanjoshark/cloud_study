# instances.py
# manage VM instance thingies
from proto_code.config import *
import json
from googleapiclient.discovery import build
from copy import deepcopy

import sys
from typing import Any

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1

# following lifted from https://cloud.google.com/compute/docs/samples/compute-instances-create-from-template-with-overrides
def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    This method will wait for the extended (long-running) operation to
    complete. If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def create_instance_from_template(
    project_id: str = PROJECT,
    zone: str = ZONE,
    instance_name: str = 'roving1',
    instance_template_name: str = 'roving-ssh-ready',
) -> compute_v1.Instance:
    """
    Creates a Compute Engine VM instance from an instance template, 
    Args:
        project_id: ID or number of the project you want to use.
        zone: Name of the zone you want to check, for example: us-west3-b
        instance_name: Name of the new instance.
        instance_template_name: Name of the instance template used for creating the new instance.

    Returns:
        Instance object.
    """
    instance_client = compute_v1.InstancesClient()
    instance_template_client = compute_v1.InstanceTemplatesClient()

    # Retrieve an instance template by name.
    instance_template = instance_template_client.get(
        project=project_id, instance_template=instance_template_name
    )

    instance = compute_v1.Instance()
    instance.name = instance_name
    # do we need this?
    #instance.disks = instance_template.properties.disks

    instance_insert_request = compute_v1.InsertInstanceRequest()
    instance_insert_request.project = project_id
    instance_insert_request.zone = zone
    instance_insert_request.instance_resource = instance
    instance_insert_request.source_instance_template = instance_template.self_link

    operation = instance_client.insert(instance_insert_request)
    wait_for_extended_operation(operation, "instance creation")

    return instance_client.get(project=project_id, zone=zone, instance=instance_name)



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