from aws_cdk import (
    Duration,
    CfnOutput,
    Stack,
    aws_lambda as _lambda,
    aws_apigatewayv2 as apigwv2,
    aws_ecr_assets as ecr_assets,
    aws_apigatewayv2_integrations as apigwv2_integrations,
)
from constructs import Construct


class CdkInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.build_lambda_func()
        self.build_apigwv2()
        CfnOutput(self, "APIGWURL", value=self.apigwv2.api_endpoint)

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

    def build_apigwv2(self):
        self.apigwv2 = apigwv2.HttpApi(
            self, id="inventoryapi_gw", api_name="inventoryapi")
        self.apigwv2.add_routes(
            path="/",
            methods=[apigwv2.HttpMethod.GET],
            integration=apigwv2_integrations.HttpLambdaIntegration(
                "inventoryapi_lambda_integration", self.docker_lambda)
        )
        self.apigwv2.add_routes(
            path="/list-products",
            methods=[apigwv2.HttpMethod.GET],
            integration=apigwv2_integrations.HttpLambdaIntegration(
                "inventoryapi_lambda_integration", self.docker_lambda)
        )

        self.apigwv2.add_routes(
            path="/product-by-index/{index}",
            methods=[apigwv2.HttpMethod.GET],
            integration=apigwv2_integrations.HttpLambdaIntegration(
                "inventoryapi_lambda_integration", self.docker_lambda)
        )

        self.apigwv2.add_routes(
            path="/add-product",
            methods=[apigwv2.HttpMethod.POST],
            integration=apigwv2_integrations.HttpLambdaIntegration(
                "inventoryapi_lambda_integration", self.docker_lambda)
        )

        self.apigwv2.add_routes(
            path="/get-random-product",
            methods=[apigwv2.HttpMethod.GET],
            integration=apigwv2_integrations.HttpLambdaIntegration(
                "inventoryapi_lambda_integration", self.docker_lambda)
        )

        self.apigwv2.add_routes(
            path="/get-product/{product_id}",
            methods=[apigwv2.HttpMethod.GET],
            integration=apigwv2_integrations.HttpLambdaIntegration(
                "inventoryapi_lambda_integration", self.docker_lambda)
        )

        self.apigwv2.add_routes(
            path="/docs",
            methods=[apigwv2.HttpMethod.ANY],
            integration=apigwv2_integrations.HttpLambdaIntegration(
                "inventoryapi_lambda_integration", self.docker_lambda)
        )

        self.apigwv2.add_routes(
            path="/openapi.json",
            methods=[apigwv2.HttpMethod.GET],
            integration=apigwv2_integrations.HttpLambdaIntegration(
                "inventoryapi_lambda_integration", self.docker_lambda)
        )

        self.apigwv2.add_stage(
            id="dev",
            stage_name="dev",
            auto_deploy=True,
        )
