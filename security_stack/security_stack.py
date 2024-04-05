from aws_cdk import aws_ec2 as ec2, Stack
from constructs import Construct

class SecurityStack(Stack):
    def __init__(
            self,
            scope: Construct,
            id: str,
            vpc_name: str,
            **kwargs,
        ) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        self.vpc = ec2.Vpc(
            self,
            vpc_name,
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(
                name=vpc_name,
                subnet_type=ec2.SubnetType.PUBLIC
                )
            ]
        )