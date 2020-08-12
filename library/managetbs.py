import os
from ansible.module_utils.basic import AnsibleModule

try:
    import cx_Oracle
except ImportError:
    CX_ORACLE_EXISTS = False
else:
    CX_ORACLE_EXISTS = True

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
        status = None
        tsname = None
        for tsname, status in result:
            status = status
            tsname = tsname

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

def readonly_tablespace(msg, cursor, tablespace):

    sql = 'alter tablespace %s read only' % tablespace

    try:
        cursor.execute(sql)
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = 'Something went wrong while changing  the tablespace to read only mode - %s sql: %s' % (error.message, sql)
        module.fail_json(msg=msg, changed=False)

    return True

def readwrite_tablespace(msg, cursor, tablespace):

    sql = 'alter tablespace %s read write' % tablespace

    try:
        cursor.execute(sql)
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = 'Something went wrong while changing  the tablespace to read write mode - %s sql: %s' % (error.message, sql)
        module.fail_json(msg=msg, changed=False)

    return True


def tbs_offline_mode(msg, cursor, tablespace):

    sql = 'alter tablespace %s offline' % tablespace

    try:
        cursor.execute(sql)
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = 'Something went wrong while changing  the tablespace to offline mode - %s sql: %s' % (error.message, sql)
        module.fail_json(msg=msg, changed=False)

    return True


def tbs_online_mode(msg, cursor, tablespace):

    sql = 'alter tablespace %s online' % tablespace

    try:
        cursor.execute(sql)
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = 'Something went wrong while changing  the tablespace to online mode - %s sql: %s' % (error.message, sql)
        module.fail_json(msg=msg, changed=False)

    return True



def main():
    msg = ['']
    module = AnsibleModule(
        argument_spec=dict(
            tablespace=dict(required=False),
            hostname=dict(default='localhost'),
            oracle_home=dict(required=False, aliases=['oh']),
            port=dict(default=1521),
            service_name=dict(required=True, aliases=['tns']),
            user=dict(required=False),
            password=dict(required=False, no_log=True),
            mode=dict(default='normal', choices=["normal", "sysdba"]),
            state=dict(default="absent", choices=["present", "absent", "read_only", "read_write", "offline", "online"])

        ),
        supports_check_mode=True
    )
    tablespace = module.params["tablespace"]
    hostname = module.params["hostname"]
    oracle_home = module.params["oracle_home"]
    port = module.params["port"]
    service_name = module.params["service_name"]
    user = module.params["user"]
    password = module.params["password"]
    mode = module.params["mode"]
    state = module.params["state"]

    if not CX_ORACLE_EXISTS:
        module.fail_json(msg="The cx_Oracle module is required. 'pip install cx_Oracle' should do the trick. If cx_Oracle is installed")


    if oracle_home is not None:
        os.environ['ORACLE_HOME'] = oracle_home.rstrip('/')
                #os.environ['LD_LIBRARY_PATH'] = ld_library_path
    elif 'ORACLE_HOME' in os.environ:
        oracle_home = os.environ['ORACLE_HOME']

    try:
        dsn = cx_Oracle.makedsn(host=hostname, port=port, service_name=service_name)
        connect = dsn
        conn = cx_Oracle.connect(user, password, dsn)


    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = 'Could not connect to database - %s, connect descriptor: %s' % (error.message, connect)
        module.fail_json(msg=msg, changed=False)

    cursor = conn.cursor()


    if state == 'read_only':
        if check_tablespace_exists(module, msg, cursor, tablespace):
            if readonly_tablespace(msg, cursor, tablespace):
                msg = 'The tablespace %s has been put in read only mode' % tablespace
                module.exit_json(msg=msg, changed=True)
            else:
                msg = 'The tablespace %s has already put in read only mode' % tablespace
                module.exit_json(msg=msg, changed=True)
        else:
            module.exit_json(msg='The tablespace %s doesn\'t exist' % tablespace, changed=False)

    if state == 'read_write':
        if check_tablespace_exists(module, msg, cursor, tablespace):
            if readwrite_tablespace(msg, cursor, tablespace):
                msg = 'The tablespace %s has been put in read write mode' % tablespace
                module.exit_json(msg=msg, changed=True)
        else:
            module.exit_json(msg='The tablespace %s doesn\'t exist' % tablespace, changed=False)

    if state == 'offline':
        if check_tablespace_exists(module, msg, cursor, tablespace):
            if tbs_offline_mode(msg, cursor, tablespace):
                msg = 'The tablespace %s has been put in offline mode' % tablespace
                module.exit_json(msg=msg, changed=True)
        else:
            module.exit_json(msg='The tablespace %s doesn\'t exist' % tablespace, changed=False)


    if state == 'online':
        if check_tablespace_exists(module, msg, cursor, tablespace):
            if tbs_online_mode(msg, cursor, tablespace):
                msg = 'The tablespace %s has been put in online mode' % tablespace
                module.exit_json(msg=msg, changed=True)
        else:
            module.exit_json(msg='The tablespace %s doesn\'t exist' % tablespace, changed=False)


if __name__ == '__main__':
    main()
