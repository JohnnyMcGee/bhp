import paramiko

def ssh_command(ip, port, user, password, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=password)
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()

    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())
    
if __name__ == '__main__':
    import sys
    from ssh_parse import ssh_parse

    ns = ssh_parse(program_name="ssh_cmd.py", args=sys.argv[1:])
    ssh_command(
        ip=ns.host,
        port=ns.port,
        user=ns.user,
        password=ns.password,
        cmd=ns.command
    )