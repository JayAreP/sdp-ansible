#!/usr/bin/python

# Import the SDP module here as well. 
from krest import EndPoint
from ansible.module_utils.basic import *
import json

try:
    import krest
    krestload = True
except ImportError:
    krestload = False

# Declare the class string 
sdpclass = "hosts"

def main():
  module_args = dict(
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    hostname=dict(type='str', required=True),
    name=dict(type='str', required=True),
    type=dict(type='str', required=True),
    hostgroup=dict(type='str', required=False)
  )

  module = AnsibleModule(argument_spec=module_args)

# store the params as a reference hashtable for use later as vars["value"]
  vars = module.params

# temp username, password, server vars
  username = vars["username"]
  password = vars["password"]
  server = vars["hostname"]

# KREST Check, fail if no module. 
  if not krestload:
      module.fail_json(msg='The krest module is required for this module (pip install krest).')

# Connect to server

  try:
    sdp = krest.EndPoint(server, username, password, ssl_validate=False)
  except Exception as error:
    module.fail_json(msg=str(error))

# ----- Below here is specific endpoint ops ------
# Create the host object (do not save yet)
  obj_request = sdp.new(sdpclass)
  obj_request.name = vars["name"]
  obj_request.type = vars["type"]

# Check to see if object already exists. 
  find = sdp.search(sdpclass, name=obj_request.name)

# If it does not, then save the above object as is.
  if len(find.hits) == 0:
    try:
        obj_request.save()
    except Exception as error:
        module.fail_json(msg=str(error))
    
    changed=True

  else:
    sdpobj = find.hits[0]
    changed=False

# Check variables that may change here (size, group membership, etc)
  if vars["hostgroup"]:
    find = sdp.search(sdpclass, name=obj_request.name)
    sdpobj = find.hits[0]
    findhg = sdp.search("host_groups", name=vars["hostgroup"])
    hg = findhg.hits[0]
    if sdpobj.host_group:
      if sdpobj.host_group.name == vars["hostgroup"]:
        changed=False
      else:
        sdpobj.host_group = hg
        sdpobj.save()
        changed=True
    else:
      sdpobj.host_group = hg
      sdpobj.save()
      changed=True
  elif sdpobj.host_group:
    sdpobj.host_group = ""
    sdpobj.save()
    changed=True

# ------ No further change operations beyond this point. ------
# Once saved, invoke a find operation for the just-created object and use that to respond. 
  find = sdp.search(sdpclass, name=obj_request.name)
  sdpobj = find.hits[0]
  if len(find.hits) == 1:
    response = {}
    response["id"] = sdpobj.id
    response["name"] = sdpobj.name
    if vars["hostgroup"]:
      response["hostgroup"] = sdpobj.host_group.name
    else:
      response["hostgroup"] = ""

  module.exit_json(
    changed=changed,
    meta=response
  )


if __name__ == '__main__':
    main()