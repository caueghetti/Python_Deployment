import paramiko
from scp import SCPClient
import json

#coleta parametros de arquivo externo
def get_parms():
    try:
        json_data = json.load(open('config.json'))
        return json_data
    except Exception as e:
        print("ERRO AO ABRIR ARQUIVO JSON : {}".format(e))
        exit(1)

#inicia conexão ssh com host remoto
def sshClient_(host_,user_,pass_):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_, username=user_, password=pass_)
        return ssh
    except Exception as e:
        print("ERRO AO INICIAR SSH CLIENT : {}".format(e))
        exit(1)

#utilizando o SSHCliente inicia serviço scp para transferencia de arquivos
def scpClient_(ssh):
    try:
        scp = SCPClient(ssh.get_transport())
        return scp
    except Exception as e:
        print("ERRO AO INICIAR SSH CLIENT : {}".format(e))
        exit(1)

#realiza transferencia de arquivos
def transfer_file(scp,dir_orig,dir_dest):
    try:
        scp.put(dir_orig,dir_dest)
        print('TRANSFERENCIA FINALIZADA : {} TO {}'.format(dir_orig,dir_dest))
    except Exception as e:
        print("ERRO AO REALIZAR TRANSFERENCIA : {}".format(e))
        exit(1)

#executa comando pos deploy
def execute_command(command):
    try:
        stdin, stdout, stderr = ssh.exec_command(configs['command_after_deployment'])
        print('\n --- OUTPUT --- \n')
        for result in stdout.readlines():
            print(result.strip())
        for result in stderr.readlines():
            print(result.strip())
    except Exception as e:
        print('ERRO AO EXECUTAR COMANDO : {}'.format(e))
        exit(1)

if __name__ == "__main__":
    hosts_configs = get_parms()
    for configs in list(hosts_configs):
        #realizando conexão com host remoto
        ssh = sshClient_(configs['host'],configs['user'],configs['pass'])
        scp = scpClient_(ssh)

        #realizando transferencia de arquivos
        for arq in list(configs['arquivos']):
            transfer_file(scp,str(arq['orig_path']).strip(),str(arq['remote_path']).strip())

        #realizando execucao de comando pos deploy (nao obrigatorio)        
        if 'command_after_deployment' in list(configs.keys()):
            if configs['command_after_deployment'].strip() != '':                  
                execute_command(configs['command_after_deployment'].strip())
