
import subprocess
import os
import time
import requests
import pexpect
import socket
import threading
from flask import request

class AutomationScript:

    image = 'automation'
    def execute_Docker(self):

        print(f"Creating Docker Image {self.image}")
        subprocess.run('docker build -t {} .'.format(self.image), shell=True)
        print('\n')

        print("Checking if Docker Image Exits")
        op = subprocess.check_output('docker images', shell=True) # check_output method used to store the output in variable.
        op=op.decode('utf-8') #Usually op is stored in bytes string. So we need to decode to string. So we need decode
        if self.image in op:
            print("{} Docker Image exists".format(self.image))
            print('\n')
        else:
            return "{} Docker Image not exists".format(self.image)

        for ports in range(3000,3007):
            cmd = 'docker run -d -p {}:3000 {}'.format(str(ports),self.image)
            print(cmd,'\n')
            subprocess.run(cmd, shell=True)
            time.sleep(5)
            print("trying to get data")
            output = self.get_Data(ports)
            print(output)
            print("\n")
        return ''

    def get_Data(self,ports):
        url = "http://localhost:{}/".format(str(ports))
        resp = requests.get(url)
        print("Getting data from {}".format(url))
        return resp.text

    def create_Server(self):
        cmd = 'docker run -dit --name master-server {}'.format(self.image)
        print(cmd,'\n')
        cntr_id = subprocess.check_output(cmd, shell=True)
        cntr_id=cntr_id.decode('utf-8')
        if cntr_id is None:
            return "master-server is not created!"
        else:
            return f"master-server is created and container-id is: {cntr_id}"


    def create_Clients(self):
        flag = False
        for id in range(1,6):
            print(f"Creating client-{str(id)}\n")
            cmd = 'docker run -dit --name client-{} --link master-server {}'.format(str(id),self.image)
            cntr_id = subprocess.check_output(cmd, shell=True)
            cntr_id = cntr_id.decode('utf-8')
            print(f"client-{str(id)} is created and container-id is: {cntr_id}")

            ssh = pexpect.spawn('docker exec -it client-{} bash'.format(str(id)))
            ssh.expect('# ')
            ssh.sendline('ping master-server -c 5')
            time.sleep(5)
            ssh.expect('# ')
            ssh.expect([pexpect.TIMEOUT, '#', pexpect.EOF])
            op=ssh.before
            op=op.decode('utf-8')
            if 'Name or service not known' in op:
                print(op,'\n')
                return "Ping is not successful from client-{} to master-server".format(str(id))
            else:
                print("Ping is successful from client-{} to master-server".format(str(id)))
                print(op,'\n')

        return "Ping to master-server is reachable on all clients"

if __name__ == "__main__":
    obj = AutomationScript()
    print(obj.execute_Docker())
    print(obj.create_Server())
    print(obj.create_Clients())
