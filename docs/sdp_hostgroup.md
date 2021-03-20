# sdp_hostgroup

This module allows you to create and manage host group objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `name` - (`string`) - The desired name for the host group object.

### Optional
* `description` - (`string`) - The desired description text for the host group. 
* `allowDifferentHostTypes` - (`bool`) - Enable (or disable) the ability to permit mixed host types within this group. 

## Examples
### 1. 
This example creates a host group object named `HostGroup01` with a description and a restriction for a singular host type. 
```yaml
sdp_hostgroup:
    name: "HostGroup01"
    description: "TestDev Linux hosts"
    allowDifferentHostTypes: False
```

