"""
Deploy VM Linode using Linode API v4, however, pexpect.spawn and pexpect.run() works only on Ubuntu.
"""
import tempfile

import pexpect


def scp(src, user2, host2, tgt, pwd, opts='', timeout=30):
    ''' Transfers file(s) from local host to remote host
    params = 
    {
    'src': '/home/src/*.txt',
    'user2': 'userName',
    'host2': 'x.x.x.x',
    'tgt': '/home/userName/',
    'pwd': myPwd(),
    'opts': '',
    }
    scp(**params) 

    '''
    cmd = f'''/bin/bash -c "scp {opts} {src} {user2}@{host2}:{tgt}"'''
    print("Executing the following cmd:", cmd, sep='\n')
    tmpFl = '/tmp/scp.log'
    fp = open(tmpFl, 'wb')
    childP = pexpect.spawn(cmd, timeout=timeout)
    try:
        childP.sendline(cmd)
        childP.expect([f"{user2}@{host2}'s password:"])
        childP.sendline(pwd)
        childP.logfile = fp
        childP.expect(pexpect.EOF)
        childP.close()
        fp.close()
        fp = open(tmpFl, 'r')
        stdout = fp.read()
        fp.close()
        if childP.exitstatus != 0:
            raise Exception(stdout)
    except KeyboardInterrupt:
        childP.close()
        fp.close()
        return
    print(stdout)


def scp1(host, user, password, from_dir, to_dir, timeout=300, recursive=False):
    fname = tempfile.mktemp()
    fout = open(fname, 'w')
    scp_cmd = 'scp'
    if recursive:
        scp_cmd += ' -r'
    scp_cmd += f' {user}@{host}:{from_dir} {to_dir}'
    child = pexpect.spawnu(scp_cmd, timeout=timeout)
    child.expect(['[pP]assword: '])
    child.sendline(str(password))
    child.logfile = fout
    child.expect(pexpect.EOF)
    child.close()
    fout.close()
    fin = open(fname, 'r')
    stdout = fin.read()
    fin.close()
    if 0 != child.exitstatus:
        raise Exception(stdout)
    return stdout


def ssh(host, cmd, user, password, timeout=300, bg_run=False):
    """SSH'es to a host using the supplied credentials and executes a command.
    Throws an exception if the command doesn't return 0.
    bgrun: run command in the background"""
    fname = tempfile.mktemp()
    fout = open(fname, 'w')
    options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'
    if bg_run:
        options += ' -f'
    ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)
    child = pexpect.spawn(ssh_cmd, timeout=timeout)
    child.expect(['[pP]assword: '])
    child.sendline(password)
    child.logfile = fout
    child.expect(pexpect.EOF)
    child.close()
    fout.close()
    fin = open(fname, 'r')
    stdout = fin.read()
    fin.close()
    if 0 != child.exitstatus:
        raise Exception(stdout)
    return stdout


if __name__ == "__main__":
    import os

    import linode_api4
    from dotenv import *
    load_dotenv()

    LINODE_API_TOKEN = os.environ["linode_api"]

    NS = 0
    S = 1

    client = linode_api4.LinodeClient(LINODE_API_TOKEN)
    my_linodes = client.linode.instances()
    print("Open Instances:")
    for current_linode in my_linodes:
        print(current_linode.label)
    available_regions = client.regions()
    print("Available regions:")
    for regions in available_regions:
        print(regions)
    available_images = client.images()
    print("Available Images:")
    for images in available_images:
        print(images)
    available_types = client.linode.types()
    print("Available Types:")
    for types in available_types:
        print(types)

    if NS:
        type = input("Select Type : \n")
        region = input("Select Region : \n")
        image = input("Select Image : \n ")
        label_image = input("Select Label_Image : \n")

    if S:
        type = 'g6-nanode-1'
        region = 'eu-central'
        image = 'linode/ubuntu20.04'
        label_image = "Hello"

    new_linode, password = client.linode.instance_create(
        type, region, image=image, label=label_image)
    print(new_linode.__dict__)
    print(f"ssh root@{new_linode.ipv4[0]}")
    print(f"Password: {password}")
    with open(f"{label_image}_{region}_{type}.txt", "w") as file:
        file.write(f"IP Address : {new_linode.ipv4[0]}")
        file.write("\n")
        file.write(f"Password : {password}")

    ssh(new_linode.ipv4[0], "ls", "root", password)
