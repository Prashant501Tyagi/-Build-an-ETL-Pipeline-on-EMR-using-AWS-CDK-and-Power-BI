from aws_cdk import (
    Stack,
    aws_s3_deployment as s3deploy,
    aws_s3 as s3,
)
from constructs import Construct
from decouple import config

# Deploys data to S3 which triggers the lambda
class BucketDeploymentStack(Stack):

    def __init__(self,
                 scope: Construct, 
                 construct_id: str,
                 primary_bucket_name: str,
                 log_bucket_name: str,
                 **kwargs
                ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        primary_bucket = s3.Bucket(
            self,
            id=primary_bucket_name,
            bucket_name=log_bucket_name
        )
 
        log_bucket = s3.Bucket(
            self,
            id=log_bucket_name,
            bucket_name=log_bucket_name
        )
    
        data_deployment = s3deploy.BucketDeployment(self, "DeployData",
                sources=[s3deploy.Source.asset("./emr_pipeline/")],
                destination_bucket=primary_bucket,
                destination_key_prefix="emr_pipeline/",
                prune=False
            )
        