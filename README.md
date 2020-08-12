# Ansible Collection - oracleansible.my_collection

Documentation for the collection.

* To check the status of the database  OS level and using srvctl utility
* To check the status of the listener OS level and using lsnrctl utility
* Ability to stop/start the local listener
* To check the cluster services in case of grid infrastructure 

                   * Cluster ready service ( CRS )
                   * Cluster synchronization service ( CSS )
                   * Event manager ( EVM )

Required Software:

              * Ansible 2.9.9
              * Python 3.6.3
                                       
Playbook:
=========

       Ansible playbook which use input from the ini file (user input) and includes the modules as per the requirement.The modules to be created in library.


Library files :
===============
       
       Created seperate python module for each checks which are listed below

               * pmoncheck.py                                             # DB availability
               * evmcheck.py                                              # EVM service status
               * csscheck.py                                              # CSS service status
               * ohascheck.py                                             # HAS service status
               * dblist.py                                                # Check the db using srvctl utility
               * tns.py                                                   # Listener check at OS level
               * listenerstop.py                                          # Stopping the listener
               * listenerstart.py                                         # Starting the listener
               * listenerstatus.py                                        # Listener status check


Required Input:
===============

Sample input:

[db_info]

nodename      =    orcl

oracle_sid    =    +ASM

oracle_home   =    /u01/app/oracle/product/12.2.0/dbhome_1

db_name       =    san

listener_name =    LISTENER_SAN

username      =    grid

grid_home     =    /u01/app/12.2.0.1/grid
