import  boto.ec2
import time

conn = boto.ec2.connect_to_region('us-east-1', aws_access_key_id = 'AKIAJHGLFCEL3SCBBSAA', aws_secret_access_key = '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\
')
my_id = raw_input("input the instance ID:")
lst = conn.terminate_instances(instance_ids=[my_id])
for i in lst:
    print("%s has been terminated" % str(i))
