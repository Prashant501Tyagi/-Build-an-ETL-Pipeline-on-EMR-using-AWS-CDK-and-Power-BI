from aws_cdk import aws_ec2 as ec2, aws_iam as iam, App, Aws, Stack, aws_emr as emr
from constructs import Construct

MASTER_INSTANCE_TYPE = "m5.xlarge"
CORE_INSTANCE_TYPE = "m5.xlarge"
CORE_INSTANCE_COUNT = 2
MARKET = "ON_DEMAND"
CLUSTER_NAME = "emr-pipeline-cluster"
EMR_RELEASE="emr-6.10.0"
SUBNET_ID ="subnet-0d0f61ccb5bd3ca19"

class EMRClusterStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        s3_log_bucket: str,
        s3_script_bucket: str,
        vpc_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        scripts_location = f"{s3_script_bucket}/emr_pipeline/scripts"

        # enable reading scripts from s3 bucket
        read_scripts_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["s3:GetObject",],
            resources=[f"arn:aws:s3:::{scripts_location}/*"],
        )
        read_scripts_document = iam.PolicyDocument()
        read_scripts_document.add_statements(read_scripts_policy)

        # emr service role
        emr_service_role = iam.Role(
            self,
            "emr_service_role",
            assumed_by=iam.ServicePrincipal("elasticmapreduce.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonElasticMapReduceRole"
                )
            ],
            inline_policies={
                "read_scripts_document": read_scripts_document
            },
        )

        # emr job flow role
        emr_job_flow_role = iam.Role(
            self,
            "emr_job_flow_role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonElasticMapReduceforEC2Role"
                )
            ],
        )
        # emr job flow profile
        emr_job_flow_profile = iam.CfnInstanceProfile(
            self,
            "emr_job_flow_profile",
            roles=["EMR_EC2_DefaultRole"],
            instance_profile_name="emrJobFlowProfile_",
        )

        # create emr cluster
        emr_cluster = emr.CfnCluster(
            self,
            "emr_cluster",
            instances=emr.CfnCluster.JobFlowInstancesConfigProperty(
                core_instance_group=emr.CfnCluster.InstanceGroupConfigProperty(
                    instance_count=CORE_INSTANCE_COUNT,
                    instance_type=CORE_INSTANCE_TYPE,
                    market=MARKET
                ),
                ec2_subnet_id=SUBNET_ID,
                ec2_key_name="ProjectProAlexClark",
                keep_job_flow_alive_when_no_steps=True,
                master_instance_group=emr.CfnCluster.InstanceGroupConfigProperty(
                    instance_count=1,
                    instance_type=MASTER_INSTANCE_TYPE,
                    market=MARKET
                ),
            ),
            steps=[
                {
                    "actionOnFailure": "CANCEL_AND_WAIT",
                    "hadoopJarStep": {
                        "jar": "command-runner.jar",
                        "args": [
                            "hive",
                            "-f",
                            f"s3://{scripts_location}/create_tables.hql",
                        ],
                    },
                    "name": "create_tables",
                },
                {
                    "actionOnFailure": "CANCEL_AND_WAIT",
                    "hadoopJarStep": {
                        "jar": "command-runner.jar",
                        "args": [
                            "hive",
                            "-f",
                            f"s3://{scripts_location}/transform_data.hql",
                        ],
                    },
                    "name": "transform_data",
                }
            ],
            job_flow_role="EMR_EC2_DefaultRole",
            name=CLUSTER_NAME,
            applications=[emr.CfnCluster.ApplicationProperty(name="Hive")],
            service_role=emr_service_role.role_name,
            configurations=[],
            log_uri=f"s3://{s3_log_bucket}/{Aws.REGION}/elasticmapreduce/",
            release_label=EMR_RELEASE,
            visible_to_all_users=False,
        )
        