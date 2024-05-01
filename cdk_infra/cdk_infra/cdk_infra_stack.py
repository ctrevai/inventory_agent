from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_ecr_assets as ecr_assets
)
from constructs import Construct


class CdkInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.build_lambda_func()

    def build_lambda_func(self):
        self.docker_lambda = _lambda.DockerImageFunction(
            self, id="inventoryapi",
            function_name="inventoryapi",
            code=_lambda.DockerImageCode.from_image_asset(
                "../image",
                # add when build docker image on Mac M1
                platform=ecr_assets.Platform.LINUX_ARM64),
            memory_size=1024,
            timeout=Duration.seconds(300),
            # add when build docker image on Mac M1
            architecture=_lambda.Architecture.ARM_64,
        )
