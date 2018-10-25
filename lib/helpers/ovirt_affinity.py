#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The ruby ovirt sdk module doesn't access affinity groups correctly

# by Paul Staniforth
# and Z. Cliffe Schreuders

import logging
import getpass

import ovirtsdk4 as sdk
import ovirtsdk4.types as types

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("affinitygroup")
parser.add_argument("vm_name_search")
parser.add_argument("ovirt_url")
parser.add_argument("ovirt_username")
parser.add_argument("ovirt_password")
args = parser.parse_args()
print(args.vm_name)
print(args.affinitygroup)


# logging.basicConfig(level=logging.DEBUG, filename='example.log')

# Create the connection to the server:
connection = sdk.Connection(
    url=args.ovirt_url,
    username=args.ovirt_username,
    password=args.ovirt_password,
    debug=True,
    log=logging.getLogger(),
)

# Locate the clusters service and use it to find the cluster
clusters_service = connection.system_service().clusters_service()
cluster = clusters_service.list(search='name=default')[0]

cluster_service = clusters_service.cluster_service(cluster.id)
cluster_affinitygroups_service = cluster_service.affinity_groups_service()

cluster_service = clusters_service.cluster_service(cluster.id)
cluster_affinitygroups_service = cluster_service.affinity_groups_service()

# cluster_affinitygroups_service.add(
#      types.AffinityGroup(
#         name='new_affinity_label10',
#         description='software defined',
#         vms_rule=types.AffinityRule(
#              enabled=True,
#              positive=True,
#              enforcing=True,
#         ),
#      ),
# )

# Get the reference to the "vms" service:
vms_service = connection.system_service().vms_service()

# Find the virtual machine:
vms = vms_service.list(search='name=' + args.vm_name_search)

affinitygroups = cluster_affinitygroups_service.list()

for affinitygroup in affinitygroups:
    print ("Affinity_Group: %s Affinity_Group ID: %s Description: %s Comment: %s"%(affinitygroup.name,affinitygroup.id,affinitygroup.description,affinitygroup.comment))
    if affinitygroup.name == args.affinitygroup:
        group_service = cluster_affinitygroups_service.group_service(affinitygroup.id)
        group_vms_service = group_service.vms_service()
        for vm in vms:
            group_vms_service.add(
                vm=types.Vm(
                    id=vm.id,
                )
            )

# Close the connection to the server:
connection.close()
