import sys

from aws_cdk import aws_lambda, Duration, aws_iam as iam

from constructs import Construct


LAMBDA_TIMEOUT = 900

BASE_LAMBDA_CONFIG = dict(
    timeout=Duration.seconds(LAMBDA_TIMEOUT),
    memory_size=512,
    tracing=aws_lambda.Tracing.ACTIVE,
    architecture=aws_lambda.Architecture.ARM_64
)

PYTHON_LAMBDA_CONFIG = dict(
    runtime=aws_lambda.Runtime.PYTHON_3_11, **BASE_LAMBDA_CONFIG
)

from layers import Layers


class Lambdas(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        COMMON_LAMBDA_CONF = dict(environment={}, **PYTHON_LAMBDA_CONFIG)
        Lay = Layers(self, 'Lay')


        self.data_source_creator = aws_lambda.Function(
            self,
            "CR_datasource",
            handler="lambda_function.lambda_handler",description ="To create Amazon kendra data source from amazon s3 bucket" ,
            layers=[Lay.bs4_requests],
            code=aws_lambda.Code.from_asset("./lambdas/code/data_source_creator"),
            **COMMON_LAMBDA_CONF
        )

        

        self.dynamodb_put_item_batch = aws_lambda.Function(
            self,
            "dynamodb_put_item_batch",
            handler="lambda_function.lambda_handler",description ="To create Dynamodb Table Re:invent Agenda 2023" ,
            code=aws_lambda.Code.from_asset("./lambdas/code/dynamodb_put_item_batch"),
            **COMMON_LAMBDA_CONF
        )

        self.dynamodb_query = aws_lambda.Function(
            self,
            "dynamodb_query",
            handler="lambda_function.lambda_handler",description ="To query Dynamodb Table Re:invent Agenda 2023" ,
            code=aws_lambda.Code.from_asset("./lambdas/code/dynamodb_query"),
            **COMMON_LAMBDA_CONF
        )

        self.agent = aws_lambda.Function(
            self,
            "agent",
            handler="lambda_function.lambda_handler",description ="Re:invent 2023 agent" ,
            layers=[Lay.bedrock,Lay.langchain],
            code=aws_lambda.Code.from_asset("./lambdas/code/agent"),
            **COMMON_LAMBDA_CONF
        )

