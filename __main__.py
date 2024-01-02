"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3, ec2

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)


sg = ec2.SecurityGroup('web-sg',ingress=[ec2.SecurityGroupIngressArgs(protocol='tcp',
                                                                      from_port=80,
                                                                      to_port=80,
                                                                      cidr_blocks=['0.0.0.0/0']
                                                                      ),
                                                                      ],
                                                                      egress=[ec2.SecurityGroupEgressArgs(protocol='-1',
                                                                                                           from_port=0,
                                                                                                           to_port=0,
                                                                                                           cidr_blocks=['0.0.0.0/0']
                                                                                                           )
                                                                                                           ],
)


instance_names =['web-server', 'db-server', 'cache-server']
output_public_ip = []
output_public_dns = []

for i in instance_names:
    instance = ec2.Instance(i,
                 ami="ami-0bfb14e483c08be7d",
                 instance_type="t2.micro",
                 tags={"Name": i},
                 vpc_security_group_ids=[sg.id],
                 )
    output_public_ip.append(instance.public_ip)
    output_public_dns.append(instance.public_dns)


pulumi.export('public_ip', output_public_ip)
pulumi.export('public_dns', output_public_dns)

#get dns
# pulumi.export('public_dns', ec2.instance.public_dns)
# pulumi.export('intance_url',pulumi.Output.concat("http://",ec2_instance.public_dns)