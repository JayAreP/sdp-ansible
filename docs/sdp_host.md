# sdp_hosts

This module allows you to create and manage host objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `name` - (`string`) - The desired name for the host object.
* `type` - (`string`) - The desired host type for the object. Accepted values are:
    * `Linux`
    * `Windows`
    * `ESX`

### Optional
* `pwwn` - (`list`) - The desired list of port WWNs for the host object. 
* `iqn` - (`string`) - The desired iSCSI initiator name (iqn) for the host object. 

## Examples
### 1. 
This example creates a host object named "LinuxHost" with 3 PWWNs. 
```yaml
sdp_host: 
    name: "testHost"
    type: "Linux"
    pwwn: 
        - "00:11:22:33:44:55:66:66"
        - "00:11:22:33:44:55:66:77"
        - "00:11:22:33:44:55:66:88"
```

### 2. 
This example creates a host object named "WindowsHost" with no further initiator information. 
```yaml
sdp_host: 
    name: "windowsHost"
    type: "Linux"
```

You may do this in cases where the iqn is not yet know, and update it at a later date once the iqn has been resolved:
```yaml
sdp_host: 
    name: "windowsHost"
    type: "Linux"
    iqn: "iqn.1991-05.microsoft:windowshost"
```