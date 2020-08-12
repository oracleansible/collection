import os
import subprocess
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: hasstatus
short_description: To check the status to check high availability service
description:
    - To check the status of the local listener using lsnrctl utility
options:
    grid_home:
        description:
            - grid home directory
        required: true
    state:
        description:
            - The state to check the high availability service
        required: true
'''



os.environ['oracle_home'] = 'oracle_home'

os.environ['grid_home'] = 'grid_home'

MSG = ['']
if __name__ == '__main__':
    module = AnsibleModule(
        argument_spec=dict(
            nodename=dict(required=False),
            grid_home=dict(default=None, aliases=['gi']),
            state=dict(default="hasstatus", choices=["hasstatus", "cssstatus"])
        ),
        supports_check_mode=True
    )
    grid_home = module.params["grid_home"]
    state = module.params["state"]

    if state == 'hasstatus':
        proc = subprocess.Popen(["$GRID_HOME/bin/crsctl check has"], stdout=subprocess.PIPE, shell=True)
        (hasstatus, err) = proc.communicate()
    output = []
    output.append(hasstatus)
    STATUS = str(output)
    print("has_status:", STATUS)
    HASSERVICE = 'is online'
    if HASSERVICE in STATUS:
        MSG = 'Oracle High Availability Services %s' % (HASSERVICE)
        module.exit_json(MSG=MSG, changed=False)
    else:
        MSG = 'Oracle High Availability Services is not online'
        module.exit_json(MSG=MSG, changed=False)
