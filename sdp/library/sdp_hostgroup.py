#!/usr/bin/python

# Import the SDP module here as well. 
from krest import EndPoint
from ansible.module_utils.basic import *
import json
import os

try:
    import krest
    krestload = True
except ImportError:
    krestload = False

# Declare the class string 
sdpclass = "host_groups"

def main():
  module_args = dict(
    name=dict(type='str', required=True),
    description=dict(type='str', required=False),
    allowDifferentHostTypes=dict(type='bool', required=False)
  )

  module = AnsibleModule(argument_spec=module_args)

# store the params as a reference hashtable for use later as vars["value"]
  vars = module.params

# temp username, password, server vars
  sdpuser = os.environ.get('SDPUSER', '-1')
  sdppass = os.environ.get('SDPPASS', '-1')
  sdphost = os.environ.get('SDPHOST', '-1')

# KREST Check, fail if no module. 
  if not krestload:
      module.fail_json(msg='The krest module is required for this module (pip install krest).')

# Connect to server

  try:
    sdp = krest.EndPoint(sdphost, sdpuser, sdppass, ssl_validate=False)
  except Exception as error:
    module.fail_json(msg=str(error))

# ----- Below here is specific endpoint ops ------
# Create the volume object (do not save yet)
  
  obj_request = sdp.new(sdpclass)
  obj_request.name = vars["name"]
  if vars["description"]:
    obj_request.description = vars["description"]
  if vars["allowDifferentHostTypes"]:
    obj_request.allow_different_host_types = vars["allowDifferentHostTypes"]
  

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
    if vars["allowDifferentHostTypes"]:
      if sdpobj.allow_different_host_types != vars["allowDifferentHostTypes"]:
        sdpobj.allow_different_host_types = vars["allowDifferentHostTypes"]
        try:
          sdpobj.save()
        except Exception as error:
          module.fail_json(msg=str(error))
        changed=True
      else:
        changed=False
    if vars["description"]:
      if sdpobj.description != vars["description"]:
        sdpobj.description = vars["description"]
        try:
          sdpobj.save()
        except Exception as error:
          module.fail_json(msg=str(error))
        changed=True
      else:
        changed=False
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
    response["description"] = sdpobj.description
    response["allowDifferentHostTypes"] = sdpobj.allow_different_host_types


  module.exit_json(
    changed=changed,
    meta=response
  )

if __name__ == '__main__':
    main()