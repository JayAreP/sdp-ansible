# sdp_snapshotview

This module allows you to create and manage snapshot view objects on the SDP platform. 

## Parameters

The following parameters are permitted.

### Required
* `name` - (`string`) - The desired name for the resulting view object.
* `volumegroup` - (`string`) - The source volume group for the snapshot. 
* `snapshot` - (`string`) - The name of the snapshot that the view is being created for. 
* `retentionpolicy` - (`string`) - The retention policy for the view to be created against. 


## Examples
### 1. 
This example creates a host object named "LinuxHost" with 3 PWWNs. 
```yaml
sdp_snapshotview: 
    name: "ATSnap01-view"
    volumegroup: "ATVG01"
    snapshot: "ATSnap01"
    retentionpolicy: "Backup"
```
