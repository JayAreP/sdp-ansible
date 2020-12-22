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
sdpclass = "volumes"

def main():
  module_args = dict(
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    hostname=dict(type='str', required=True),
    name=dict(type='str', required=True),
    sizeInGB=dict(type='int', required=True),
    volumegroup=dict(type='str', required=True)
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
# Create the volume object (do not save yet)
  
  obj_request = sdp.new(sdpclass)
  obj_request.name = vars["name"]

  size = vars["sizeInGB"]*2**20
  obj_request.size = size

  findvg = sdp.search("volume_groups", name=vars["volumegroup"])
  vg = findvg.hits[0]
  obj_request.volume_group = vg

# Check to see if object already exists. 
  find = sdp.search(sdpclass, name=obj_request.name)

# If it does not, then save the above object as is.
  if len(find.hits) == 0:
    try:
        obj_request.save()
    except Exception as error:
        module.fail_json(msg=str(error))
    
    changed=True
# Otherwise, check the current object's secondary parameters against the request, and adjust as needed. 
  else:
    sdpobj = find.hits[0]
    if sdpobj.volume_group.name != vars["volumegroup"]:
      sdpobj.volume_group = vg
      sdpobj.save()
      changed=True
    elif sdpobj.size < size:
      sdpobj.size = size
      sdpobj.save()
      changed=True
    else:
      changed=False

# Check variables that may change here (size, group membership, etc)


# ------ No further change operations beyond this point. ------
# Once saved, invoke a find operation for the just-created object and use that to respond. 
  find = sdp.search(sdpclass, name=obj_request.name)
  sdpobj = find.hits[0]
  if len(find.hits) == 1:
    response = {}
    response["id"] = sdpobj.id
    response["name"] = sdpobj.name
    response["size"] = sdpobj.size
    response["volumegroup"] = sdpobj.volume_group.name

  module.exit_json(
    changed=changed,
    meta=response
  )


if __name__ == '__main__':
    main()