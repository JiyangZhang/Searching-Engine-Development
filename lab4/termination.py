import  boto.ec2
import sys
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

conn = boto.ec2.connect_to_region('us-east-1', aws_access_key_id = str(key_id), aws_secret_access_key = str(secret_access_key))
instance_id = raw_input("Please enter instance_id: ")  # Python 2
lst = conn.terminate_instances(instance_ids=[instance_id])
for i in lst:
    print("%s has been terminated" % str(i))
