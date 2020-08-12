import os
import re
import subprocess

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: dblist
short_description: To check the existance of the database
description:
    - To check the presence of the database in the server using srvctl utility
options:
    db_name:
        description:
            - The database name to check
        required: true
    state:
        description:
            - The state to check the presence of the database in the server
        required: true
'''

os.environ['oracle_home'] = 'oracle_home'

os.environ['grid_home'] = 'grid_home'

MSG = ['']

if __name__ == '__main__':
    module = AnsibleModule(
        argument_spec=dict(
            nodename=dict(required=False),
            oracle_home=dict(required=False, aliases=['oh']),
            db_name=dict(required=True, aliases=['db']),
            dbstate=dict(default="dblist", choices=["dblist"])
        ),
        supports_check_mode=True
    )

    db_name = module.params["db_name"]
    dbstate = module.params["dbstate"]

    ORATABFILE = '/etc/oratab'
    ISEXIST = os.path.exists(ORATABFILE)
    LINE = None
    print("File exists:", ISEXIST)
    with open(ORATABFILE, 'r') as oratab:
        for LINE in oratab:
            x = re.search(db_name +':', LINE)
    if x:
        print(LINE)
    else:
        print("db is not running")


    if dbstate == 'dblist':
        proc = subprocess.Popen(["$ORACLE_HOME/bin/srvctl config database"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
    a = []
    a.append(out)
    STATUS = str(a)
    print("db_list:", STATUS)

    if db_name in STATUS:
        MSG = 'Found " %s " in dblist ' % (db_name)
        module.exit_json(MSG=MSG, changed=False)
    else:
        MSG = 'dblist: db %s not found' % (db_name)
        module.exit_json(MSG=MSG, changed=False)
