#!/usr/bin/python

import sys
import time
import pexpect

# Generate executable with pyinstaller --onefile connect.py. Install pyinstaller with sudo pip install pyinstaller

# Hosts data
HOSTS_DATA = {
    'ssh_name_1': {'port': 22, 'user': 'test', 'home': '/home/test', 'password': 'test'},
    'ssh_name_2': {'port': 22, 'user': 'test', 'home': '/home/test', 'password': 'test'}
}

# Check arguments. Remember that script name is in sys.argv
MIN_ARGS = 2
MAX_ARGS = 3

if len(sys.argv) < MIN_ARGS or len(sys.argv) > MAX_ARGS:
    print 'Invalid arguments. Please set server for ssh, or server and file for scp. '
    print 'Usage: connect server --> Connect to ssh server'
    print '       connect server file --> Recover file from server in its home folder'
    print '       connect file server --> Send file to home folder server'
    exit(1)

mode = ''
if len(sys.argv) == MIN_ARGS:
    mode = 'ssh'
elif len(sys.argv) == MAX_ARGS:
    mode = 'scp'
else:
    print 'Undefined error'
    exit(3)


# Get host and set command
cmd = ''
host = ''
if mode == 'ssh':
    host = sys.argv[1]
    if host not in HOSTS_DATA.keys():
        print 'Host not supported. Please contact with admin for adding'
        exit(2)
    cmd = 'ssh -p {} {}@{}'.format(HOSTS_DATA[host]['port'], HOSTS_DATA[host]['user'], host)
elif mode == 'scp':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    if arg1 in HOSTS_DATA.keys():
        host = arg1
        filename = arg2
        cmd = 'scp -p {} {}@{}:{}/{} .'.format(HOSTS_DATA[host]['port'], HOSTS_DATA[host]['user'], host,
                                               HOSTS_DATA[host]['home'], filename)
    elif arg2 in HOSTS_DATA.keys():
        host = arg2
        filename = arg1
        cmd = 'scp -p {} {} {}@{}:{}'.format(HOSTS_DATA[host]['port'], filename, HOSTS_DATA[host]['user'], host,
                                             HOSTS_DATA[host]['home'])
    else:
        print 'Host not supported. Please contact with admin for adding'
        exit(2)

else:
    print 'Undefined error'
    exit(3)

# Try to connect
try:
    ssh = pexpect.spawn(cmd)
    ssh.expect('assword:')
    time.sleep(0.1)
    ssh.sendline(HOSTS_DATA[host]['password'])
    time.sleep(0.5)
    ssh.interact()

except Exception as e:
    print(str(e))
