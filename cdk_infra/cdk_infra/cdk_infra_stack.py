from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct


class CdkInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.build_lambda_func()
        self.build_api_gateway()

    def build_lambda_func(self):
        self.docker_lambda = _lambda.DockerImageFunction(
            self, id="inventoryapi",
            function_name="inventoryapi", code=_lambda.DockerImageCode.from_image_asset("../image"),
            memory_size=1024,
            timeout=Duration.seconds(300)
        )

    # add api gateway
    def build_api_gateway(self):
        self.api_gateway = apigateway.LambdaRestApi(
            self, "InventoryApi",
            handler=self.docker_lambda,
            proxy=False
        )
        self.api_gateway.root.add_method(
            "GET", apigateway.LambdaIntegration(self.docker_lambda))
