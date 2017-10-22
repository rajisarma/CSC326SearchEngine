import boto.ec2
import os
import time
import string

AWS_ACCESS_KEY_ID = "AKIAJKJ4BBOQQC4UM3XA"
AWS_SECURITY_ACCESS_KEY = "Fpv+ty8pGm+Mr2liAxIVxGBF3lS02EXMVpIv3hyA"
KEY_NAME = "key_pair_bm"
KEY_PAIR_DIRECTORY_PATH = "~/Desktop/csc326/lab1_group_37/aws/"
SECURITY_GROUP_NAME = "csc326-groupnumber37_bm"
SECURITY_GROUP_DESCRIPTION = "security_group_for_group_37"

def establish_aws_connection():
	connection = boto.ec2.connect_to_region("us-east-1", aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECURITY_ACCESS_KEY)
	
	#delete_key_pair_and_security_groups(connection)

	key_pair_path = KEY_PAIR_DIRECTORY_PATH + KEY_NAME + ".pem"
	print key_pair_path
	if(os.path.exists(key_pair_path)):
		os.remove(key_pair_path)
	key_pair = connection.create_key_pair(KEY_NAME)
	key_pair.save(KEY_PAIR_DIRECTORY_PATH)


	security_group_instance = connection.create_security_group(SECURITY_GROUP_NAME, SECURITY_GROUP_DESCRIPTION)

	connection.authorize_security_group(group_name = security_group_instance.name, ip_protocol = "ICMP", from_port = "-1", to_port = "-1", cidr_ip = "0.0.0.0/0")
	connection.authorize_security_group(group_name = security_group_instance.name, ip_protocol = "TCP", from_port = "22", to_port = "22", cidr_ip = "0.0.0.0/0")
	connection.authorize_security_group(group_name = security_group_instance.name, ip_protocol = "TCP", from_port = "80", to_port = "80", cidr_ip = "0.0.0.0/0")

	instance_objects = connection.run_instances('ami-c5062ba0', instance_type = "t2.micro", security_groups = [security_group_instance.name], key_name = KEY_NAME)
	print instance_objects
	return connection, instance_objects.instances[0]

def verify_instance_running(connection,instance_id):
	instance_status = connection.get_all_instance_status(instance_ids = [instance.id])

	if not instance_status:
		return "None"
	else:
		return instance_status[0].system_status.status

def set_static_ip_address(connection, instance):
	static_ip_address = connection.allocate_address()
	static_ip_address.associate(instance_id = instance.id)
	return static_ip_address

def delete_key_pair_and_security_groups(connection):

	instances = [instance.id for instance in connection.get_only_instances()]
	connection.terminate_instances(instances)
	
	connection.delete_key_pair(KEY_NAME)

	security_groups = connection.get_all_security_groups()
	print security_groups
	if (SECURITY_GROUP_NAME in security_groups):
		security_group_ids = [security_group.id for security_group in security_groups]
		for sg_id in security_group_ids:
			connection.delete_security_group(SECURITY_GROUP_NAME, group_id = str(sg_id))
	else:
		pass

	
if __name__ == "__main__":
	connection, instance = establish_aws_connection()
	while(instance.state != "running"):
		instance.update()

	ip_address = set_static_ip_address(connection,instance)

	print ip_address.public_ip
	print instance.id
	print connection
