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
sdpclass = "mappings"

def main():
  module_args = dict(
    hostname=dict(type='str', required=True),
    volumename=dict(type='str', required=True)
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

  # Store the volume
  volreqclass = "volumes"
  vols = sdp.search(volreqclass, name=vars["volumename"])

  # Store the host
  hostreqclass = "hosts"
  hosts = sdp.search(hostreqclass, name=vars["hostname"])

  if len(vols.hits) == 1:
      vol = vols.hits[0]
      obj_request.volume = vol
  else:
      error = "Volume {} was not found.".format(vars["volumename"])
      module.fail_json(msg=str(error))

  if len(hosts.hits) == 1:
      host = hosts.hits[0]
      obj_request.host = host
  else:
      error = "Host {} was not found.".format(vars["hostname"])
      module.fail_json(msg=str(error))

  find = sdp.search(sdpclass, __limit=9999)
  for f in find.hits:
      if f.host.id == host.id and f.volume.id == vol.id:
          sdpobj = f
          break

# If it does not, then save the above object as is.
  try: sdpobj
  except NameError: sdpobj = None
  if sdpobj is None:
    try:
        result = obj_request.save()
    except Exception as error:
        module.fail_json(msg=str(error))
    changed = True
  else:
      result = sdpobj
      changed = False
    
# ------ No further change operations beyond this point. ------
# Once saved, invoke a find operation for the just-created object and use that to respond. 
  find = sdp.search(sdpclass, id=result.id)
  sdpobj = find.hits[0]
  if len(find.hits) == 1:
    response = {}
    response["id"] = sdpobj.id
    response["hostname"] = sdpobj.host.name
    response["volume"] = sdpobj.volume.name

  module.exit_json(
    changed=changed,
    meta=response
  )

if __name__ == '__main__':
    main()