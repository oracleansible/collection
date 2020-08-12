import os
import subprocess
import re
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: pmon
short_description: To check the status of the database
description:
    - To check the status of the database in the server
options:
    db_name:
        description:
            - The database name
        required: true
    state:
        description:
            - The state to check the status of the database
        required: true
'''

os.environ['oracle_home'] = 'oracle_home'

os.environ['grid_home'] = 'grid_home'

MSG = ['']

if __name__ == '__main__':
    module = AnsibleModule(
        argument_spec=dict(
            db_name=dict(required=True, aliases=['db']),
            state=dict(default="pmon", choices=["pmon"])
        ),
        supports_check_mode=True
    )
    db_name = module.params["db_name"]
    state = module.params["state"]

    ORATABFILE = '/etc/oratab'
    ISEXISTS = os.path.exists(ORATABFILE)
    print("File exists:", ISEXISTS)
    LINE = None
    with open(ORATABFILE, 'r') as oratab:
        for LINE in oratab:
            x = re.search(db_name +':', LINE)
    if x:
        print(LINE)
    else:
        print("db is not running")

    if state == 'pmon':
        proc = subprocess.Popen(['ps -ef|grep pmon'], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        pmonoutput = []
        pmonoutput.append(out)
        PMON = str(pmonoutput)
        if db_name in PMON:
            MSG = 'Database " %s " is up ' % (db_name)
            module.exit_json(MSG=MSG, changed=False)
        else:
            MSG = 'Database " %s " is down ' % (db_name)
            module.exit_json(MSG=MSG, changed=False)
