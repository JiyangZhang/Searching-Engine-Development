import  boto.ec2
import time
import os

# connection
conn = boto.ec2.connect_to_region('us-east-1', aws_access_key_id = 'AKIAJHGLFCEL3SCBBSAA', aws_secret_access_key = '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\
')

# create key pair
"""
keypair = conn.create_key_pair('zhan')
keypair.save(".")
"""

# create groups
"""

web = conn.create_security_group('csc326_group11', 'Our CS Group')
web.authorize('ICMP', -1, -1, '0.0.0.0/0')
web.authorize('TCP', 22, 22, '0.0.0.0/0')
web.authorize('TCP', 80, 80, '0.0.0.0/0')
"""
# launch instance

reservation_obj = conn.run_instances('ami-8caa1ce4', instance_type='t1.micro', security_groups= ['csc326_group11'], key_name='zhan')
instance = reservation_obj.instances[0]

# get the instance ip address

while instance.update() != "running":
    time.sleep(5)  # Run this in a green thread, ideally

address = instance.ip_address
instance_ID = instance.id
print(address)
print(instance_ID)
# Setup static IP address
"""
address = conn.allocate_address()
address.associate(instance_id = 'i-044907bea3635e8ac')

"""

# connect to the server
"""
os.system("scp -i key_pair.pem <FILE-PATH> ubuntu@<PUBLIC-IP-ADDRESS>:~/<REMOTE-PATH>")
os.system("ssh -i key_pair.pem ubuntu@<PUBLIC-IP-ADDRESS>")
os.system("install the necessary package")
os.system("run the frontend")
"""

