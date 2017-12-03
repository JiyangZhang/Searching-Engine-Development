import  boto.ec2
import time
import os
import paramiko

#get access
f = open('config.txt')    # people have to type their key_id at the first line and secret at the second line
l = []
for i in f:
    if i[-1] == '\n':
        l.append(i[:-2])
    else:
        l.append(i)
f.close()
# get the key
key_id = l[0]
secret_access_key = l[1]

# connection
conn = boto.ec2.connect_to_region('us-east-1', aws_access_key_id = str(key_id), aws_secret_access_key = str(secret_access_key))

# create key pair
keypair = conn.create_key_pair('csc')
keypair.save(".")
key_name = 'csc.pem'
os.system("chmod 400 " + key_name)
"""
# create security groups
web = conn.create_security_group('csc326_group11', 'Our CS Group')
web.authorize('ICMP', -1, -1, '0.0.0.0/0')
web.authorize('TCP', 22, 22, '0.0.0.0/0')
web.authorize('TCP', 80, 80, '0.0.0.0/0')
"""

# launch instance
reservation_obj = conn.run_instances('ami-8caa1ce4', instance_type='t1.micro', security_groups= ['csc326_group11'], key_name= 'csc' )# have to change key
instance = reservation_obj.instances[0]
# get the instance ip address
while instance.update() != "running":
    time.sleep(30)  # Run this in a green thread, ideally
instance_address = instance.ip_address  # get the address of instance
instance_ID = instance.id   # get the instance id 
print(instance_address)

# all what to do on the server

os.system("scp -i " + key_name + "  Backend_lab4_new.py ubuntu@" + instance_address + ":~/.")   # upload the files to the server
os.system("scp -i " + key_name + "  FrontEnd_lab4.py ubuntu@" + instance_address + ":~/.")
os.system("scp -i " + key_name + "  getdata.py ubuntu@" + instance_address + ":~/.")
os.system("scp -i " + key_name + "  storage.py ubuntu@" + instance_address + ":~/.")
os.system("scp -i " + key_name + "  urls.txt ubuntu@" + instance_address + ":~/.")
os.system("scp -i " + key_name + "  pagerank.py ubuntu@" + instance_address + ":~/.")
os.system("scp -i " + key_name + "  Backend_lab4_new.py ubuntu@" + instance_address + ":~/.")

k = paramiko.RSAKey.from_private_key_file(key_name) # must be in your current dir
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

c.connect( hostname = instance_address, username = "ubuntu", pkey = k )

# install mongod
commands_db = [ "sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6",\
'echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list',\
"sudo apt-get update", "sudo apt-get install -y mongodb-org",\
"sudo service mongod start" ]
# install libraries of backend
commands_bd = [ "sudo apt-get install -y python-pip", 
"sudo pip install beautifulsoup",\
"sudo pip install pymongo", "sudo apt-get install -y python-numpy"]
# install libraries for frontend
commands_fd = ["sudo pip install bottle", "sudo pip install httplib2",\
"sudo apt install -y python-oauth2client ",
 "sudo pip install --upgrade google-api-python-client",\
"sudo apt-get install python-beaker"]
# run backend and frontend
commands_run_bd = ["sudo python Backend_lab4_new.py"]
commands_run_fd = ['sudo python FrontEnd_lab4.py']
commands_all = commands_db + commands_bd + commands_fd + commands_run_bd + commands_run_fd

def line_buffered(f):
    line_buf = ""
    while not f.channel.exit_status_ready():
        line_buf += f.read(1)
        if line_buf.endswith('\n'):
            yield line_buf
            line_buf = ''

for command in commands_all:
    print ("Executing {}".format( command ))
    stdin , stdout, stderr = c.exec_command(command) # this command is executed on the *remote* server
    for l in line_buffered(stdout):
        print l
    print stdout.read()
    print stderr.read()

c.close()
"""
# create load balancer
elb = boto.ec2.elb.connect_to_region( 'us-east-1', aws_access_key_id =str(key_id), aws_secret_access_key = str(secret_access_key))
hc = HealthCheck(
        interval=30,
        healthy_threshold=10,
        unhealthy_threshold=2,
        target='TCP:80')
subnet = ['subnet-44d40519','subnet-9d0891d6']
ports = [(80, 80, 'TCP')]
lb = elb.create_load_balancer('my-csc-326', None, ports, subnet ,["sg-65149510"], 'internet-facing', None)
lb.configure_health_check(hc)
load_balancer_dns = lb.dns_name #get the load_balancer_dns
#lb.register_instances(instance_ids)
"""