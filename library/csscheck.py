import os
import subprocess
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: cssstatus
short_description: To check the status to check cluster synchronization service
description:
    - To check the status of the css service
options:
    grid_home:
        description:
            - grid home binary
        required: true
    state:
        description:
            - The state to check the cluster synchronization service
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


    if state == 'cssstatus':
        proc = subprocess.Popen(["$GRID_HOME/bin/crsctl check css"], stdout=subprocess.PIPE, shell=True)
        (cssstatus, err) = proc.communicate()
    output = []
    output.append(cssstatus)
    STATUS = str(output)
    print("css_status:", STATUS)
    CSS = 'is online'
    if CSS in STATUS:
        MSG = 'Cluster Synchronization Services %s' % (CSS)
        module.exit_json(MSG=MSG, changed=False)
    else:
        MSG = 'Cluster Synchronization Services is not online'
        module.exit_json(MSG=MSG, changed=False)
