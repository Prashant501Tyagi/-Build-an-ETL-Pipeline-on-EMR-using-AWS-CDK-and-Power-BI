#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags
from decouple import config

from bucket_deployment_stack.bucket_deployment_stack import BucketDeploymentStack
from emr_cluster_stack.emr_cluster_stack import EMRClusterStack
from security_stack.security_stack import SecurityStack

# Set global variables
ID = config('id')
PRIMARY_BUCKET = f"emr-pipeline-{ID}"
LOG_BUCKET = f"emr-logs-{ID}"
SCRIPT_LOCATION = f"{PRIMARY_BUCKET}/scripts/"
VPC_NAME = f"emr-pipeline-vpc-{ID}"

env_USA = cdk.Environment(account="196214221306", region="us-west-1")
app = cdk.App()

# Create Stacks
security_stack = SecurityStack(
    scope=app,
    id="SecurityStack",
    vpc_name=VPC_NAME,
    env=env_USA
)


bucket_deployment_stack = BucketDeploymentStack(
    scope=app,
    construct_id=f"BucketDeploymentStack-1",
    primary_bucket_name=PRIMARY_BUCKET,
    log_bucket_name=LOG_BUCKET,
    env=env_USA
)


emr_cluster_stack = EMRClusterStack(
    scope=app,
    id=f"EMRClusterStack",
    s3_log_bucket=LOG_BUCKET,
    s3_script_bucket=PRIMARY_BUCKET,
    vpc_name=f"SecurityStack/{VPC_NAME}",
    env=env_USA
)


# Add dependencies
emr_cluster_stack.add_dependency(bucket_deployment_stack)
emr_cluster_stack.add_dependency(security_stack)


# Add tags
Tags.of(app).add("ProjectOwner", "Prashant")
Tags.of(app).add("Project", "EMR-ETL-Pipeline")

app.synth()
