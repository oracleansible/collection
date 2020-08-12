import os
import subprocess
from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = '''
---
module: tnscheck
short_description: Listener status at OS level
description:
    - To check the status of the listener
options:
    state:
        description:
            - The state to check the status of the listener at OS level
        required: true
'''

os.environ['oracle_home'] = 'oracle_home'

os.environ['grid_home'] = 'grid_home'

MSG = ['']

if __name__ == '__main__':
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default="tnscheck", choices=["tnscheck"])
        ),
        supports_check_mode=True
    )
    state = module.params["state"]

    if state == 'tnscheck':
        proc = subprocess.Popen(['ps -ef|grep tns'], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        tnsoutput = []
        tnsoutput.append(out)
        TNS = str(tnsoutput)
        RESULT = 'tnslsnr'
        if RESULT in TNS:
            MSG = "Listener is up and running fine"
            module.exit_json(MSG=MSG, changed=False)
        else:
            MSG = "listener down"
            module.exit_json(MSG=MSG, changed=False)
