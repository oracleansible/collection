import os
import subprocess
from ansible.module_utils.basic import AnsibleModule

os.environ['oracle_home'] = 'oracle_home'

os.environ['grid_home'] = 'grid_home'

os.environ['oracle_sid'] = 'oracle_sid'

MSG = ['']

if __name__ == '__main__':
    module = AnsibleModule(
        argument_spec=dict(
            nodename=dict(required=False),
            oracle_home=dict(default=None, aliases=['oh']),
            grid_home=dict(default=None, aliases=['gi']),
            listener_name=dict(required=True, aliases=['lsnr_name']),
            state=dict(default="lsnrctlstart"),
            username=dict(required=True, aliases=['user'])
        ),
        supports_check_mode=True
    )
    oracle_home = module.params["oracle_home"]
    grid_home = module.params["grid_home"]
    state = module.params["state"]
    listener_name = module.params["listener_name"]
    username = module.params["username"]


    if state == 'lsnrctlstart':
        proc = subprocess.Popen(["$ORACLE_HOME/bin/srvctl start listener"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
    MSG = 'Local listener started'
    module.exit_json(MSG=MSG, changed=False)
