import  boto.ec2
import time

conn = boto.ec2.connect_to_region('us-east-1', aws_access_key_id = '#', aws_secret_access_key = '#\')
my_id = raw_input("input the instance ID:")
lst = conn.terminate_instances(instance_ids=[my_id])
for i in lst:
    print("%s has been terminated" % str(i))
