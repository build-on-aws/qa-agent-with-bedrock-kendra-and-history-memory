from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as ddb
)
from constructs import Construct


REMOVAL_POLICY = RemovalPolicy.DESTROY

TABLE_CONFIG = dict (removal_policy=REMOVAL_POLICY, billing_mode= ddb.BillingMode.PAY_PER_REQUEST)


class Tables(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.reinvent_table = ddb.Table(
            self, "ReInventAgenda", 
            partition_key=ddb.Attribute(name="thirdpartyid", type=ddb.AttributeType.STRING)
        )
                                      
        self.session_table = ddb.Table(
            self, "SessionTable", 
            partition_key=ddb.Attribute(name="SessionId", type=ddb.AttributeType.STRING),
            **TABLE_CONFIG)
        