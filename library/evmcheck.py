import os
import subprocess
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: evmstatus
short_description: To check the status of event manager
description:
    - To check the status of the event manager
options:
    grid_home:
        description:
            - grid home
        required: true
    state:
        description:
            - The state to check the event manager service
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
            evmstate=dict(default="evmstatus", aliases=['evm'])
        ),
        supports_check_mode=True
    )
    grid_home = module.params["grid_home"]
    evmstate = module.params["evmstate"]


    if evmstate == 'evmstatus':
        proc = subprocess.Popen(["$GRID_HOME/bin/crsctl check evm"], stdout=subprocess.PIPE, shell=True)
        (evmstatus, err) = proc.communicate()
    output = []
    output.append(evmstatus)
    STATUS = str(output)
    print("evm_status:", STATUS)
    EVM = 'is online'
    if EVM in STATUS:
        MSG = 'Event Manager %s' % (EVM)
        module.exit_json(MSG=MSG, changed=False)
    else:
        MSG = 'Event Manager is not online'
        module.exit_json(MSG=MSG, changed=False)
