#!/usr/bin/python
# -*- coding: utf-8 -*-



try:
    import cx_Oracle
except ImportError:
    cx_oracle_exists = False
else:
    cx_oracle_exists = True

# Check if the tablespace exists
def check_tablespace_exists(module, msg, cursor, tablespace):

    sql = 'select tablespace_name, status from dba_tablespaces where tablespace_name = upper(\'%s\')' % tablespace

    try:
            cursor.execute(sql)
            result = cursor.fetchall()
            count = cursor.rowcount
    except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            msg = error.message+ 'sql: ' + sql
            return False

    if count > 0:
        list_of_dbfs = get_tablespace_files(module, msg, cursor, tablespace)
        for tsname,status in result:
            status  = status

        return True, status

def get_tablespace_files(module, msg, cursor, tablespace):
    sql = 'select FILE_NAME from dba_data_files where TABLESPACE_NAME = upper(\'%s\')' % tablespace
    try:
            cursor.execute(sql)
            result = cursor.fetchall()
    except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            msg = error.message+ ': sql: ' + sql
            module.fail_json(msg=msg)

    return result

def drop_tablespace(msg, cursor, tablespace):

    sql = 'drop tablespace %s including contents and datafiles' % tablespace

    try:
        cursor.execute(sql)
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = 'Something went wrong while dropping the tablespace - %s sql: %s' % (error.message, sql)
        module.fail_json(msg=msg, changed=False)

    return True

def main():
    msg = ['']
    module = AnsibleModule(
        argument_spec = dict(
            tablespace    = dict(required=False),
            hostname      = dict(default='localhost'),
            oracle_home   = dict(required=False, aliases=['oh']),
            port          = dict(default=1521),
            service_name  = dict(required=True, aliases = ['tns']),
            user          = dict(required=False),
            password      = dict(required=False, no_log=True),
            mode          = dict(default='normal', choices=["normal","sysdba"]),
            state         = dict(default="absent", choices=["present", "absent"])

        ),
        supports_check_mode=True
    )
    tablespace   = module.params["tablespace"]
    hostname     = module.params["hostname"]
    oracle_home  = module.params["oracle_home"]
    port         = module.params["port"]
    service_name = module.params["service_name"]
    user         = module.params["user"]
    password     = module.params["password"]
    mode         = module.params["mode"]
    state        = module.params["state"]
    

    if not cx_oracle_exists:
                module.fail_json(msg="The cx_Oracle module is required. 'pip install cx_Oracle' should do the trick. If cx_Oracle is installed")


    if oracle_home is not None:
                os.environ['ORACLE_HOME'] = oracle_home.rstrip('/')
                #os.environ['LD_LIBRARY_PATH'] = ld_library_path
    elif 'ORACLE_HOME' in os.environ:
                oracle_home     = os.environ['ORACLE_HOME']

    wallet_connect = '/@%s' % service_name
    try:
          if (not user and not password ): # If neither user or password is supplied, the use of an oracle wallet is assumed
                if mode == 'sysdba':
                     connect = wallet_connect
                     conn = cx_Oracle.connect(wallet_connect, mode=cx_Oracle.SYSDBA)
                else:
                     connect = wallet_connect
                     conn = cx_Oracle.connect(wallet_connect)

          elif (user and password ):
                if mode == 'sysdba':
                     dsn = cx_Oracle.makedsn(host=hostname, port=port, service_name=service_name)
                     connect = dsn
                     conn = cx_Oracle.connect(user, password, dsn, mode=cx_Oracle.SYSDBA)
                else:
                     dsn = cx_Oracle.makedsn(host=hostname, port=port, service_name=service_name)
                     connect = dsn
                     conn = cx_Oracle.connect(user, password, dsn)

          elif (not(user) or not(password)):
                     module.fail_json(msg='Missing username or password for cx_Oracle')

    except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                msg = 'Could not connect to database - %s, connect descriptor: %s' % (error.message, connect)
                module.fail_json(msg=msg, changed=False)

    cursor = conn.cursor()


    if state == 'absent':
        if check_tablespace_exists(module, msg, cursor, tablespace):
            if drop_tablespace(msg, cursor, tablespace):
                msg = 'The tablespace %s has been dropped successfully' % tablespace
                module.exit_json(msg=msg, changed=True)
        else:
            module.exit_json(msg='The tablespace %s doesn\'t exist' % tablespace, changed=False)



from ansible.module_utils.basic import *
if __name__ == '__main__':
       main()

