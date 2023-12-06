from aws_cdk import (
    # Duration,
    Stack,
    Fn as CFn,
    # aws_sqs as sqs,
    aws_s3_notifications,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct
from kendra_constructs import (
    KendraIndex, CRKendraS3Datasource
)
from s3_cloudfront import S3Deploy
from lambdas import Lambdas
from databases import Tables

ENV_KEY_NAME = "thirdpartyid"
bedrock_model_id = "anthropic.claude-instant-v1"


class ReInventAgentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stk = Stack.of(self)
        account_id = stk.account
        region_name = self.region

        # Amazon Kendra 
        index = KendraIndex(self, "I")

        #Create Amazon S3 Bucket and upload the data into the folder agenda_reinvent_2023

        s3_deploy = S3Deploy(self, "re-invent-agenda", "agenda_reinvent","agenda_reinvent")

        s3_deploy_json = S3Deploy(self, "bucket-agenda", "agenda_reinvent_2023_json","agenda_reinvent_2023_json")

        #Create Amazon DynamoDB Tables
        Tbl = Tables(self, 'Tbl')

        #Create Amazon Lamda Functions

        Fn  = Lambdas(self,'Fn')

        Fn.data_source_creator.add_to_role_policy(iam.PolicyStatement(actions=["kendra:*"], resources=["*"]))

        Fn.data_source_creator.add_to_role_policy(iam.PolicyStatement(actions=["iam:PassRole"], resources=["*"]))

        # index_id = CFn.import_value("REINVENT-INDEX-ID")

        index_id = index.index_id

        Tbl.session_table.grant_full_access(Fn.agent)
        Tbl.reinvent_table.grant_full_access(Fn.agent)
        Fn.agent.add_environment(key='TABLE_NAME', value= Tbl.reinvent_table.table_name)
        Fn.agent.add_environment(key='TABLE_SESSION', value= Tbl.session_table.table_name)
        Fn.agent.add_environment(key='KENDRA_INDEX', value= index_id)
        Fn.agent.add_environment(key='LAMBDA_QUERY_NAME', value= Fn.dynamodb_query.function_name)
        Fn.agent.add_environment(key='MODEL_ID', value= bedrock_model_id)

        Fn.agent.add_to_role_policy(iam.PolicyStatement( actions=["lambda:InvokeFunction"], resources=[Fn.dynamodb_query.function_arn]))

        Fn.agent.add_to_role_policy(iam.PolicyStatement( actions=["kendra:Retrieve"], resources=[f"arn:aws:kendra:{region_name}:{account_id}:index/{index_id}"]))

        Fn.agent.add_to_role_policy(iam.PolicyStatement( actions=["kendra:Query"], resources=[f"arn:aws:kendra:{region_name}:{account_id}:index/{index_id}"]))

        Fn.agent.add_to_role_policy(iam.PolicyStatement( actions=["bedrock:*"], resources=['*']))


        Tbl.reinvent_table.grant_full_access(Fn.dynamodb_put_item_batch)
        Tbl.reinvent_table.grant_full_access(Fn.dynamodb_query)
        

        # TODO: Nota puedes crear un CustomResource para cargar la Tabla sin necesidad de un bucket con trigger. 
    
        s3_deploy_json.bucket.add_event_notification(s3.EventType.OBJECT_CREATED,
                                              aws_s3_notifications.LambdaDestination(Fn.dynamodb_put_item_batch))
        
        s3_deploy_json.bucket.grant_read(Fn.dynamodb_put_item_batch)



        Fn.dynamodb_put_item_batch.add_environment(key='TABLE_NAME', value= Tbl.reinvent_table.table_name)
        Fn.dynamodb_query.add_environment(key='TABLE_NAME', value= Tbl.reinvent_table.table_name)
        Fn.dynamodb_query.add_environment(key='ENV_KEY_NAME', value= ENV_KEY_NAME)

        #Data to Amazon Kendra Index
        
        
        
        s3_files_es_ds = CRKendraS3Datasource(
            self, "S3_txt_reinvent",
            service_token=Fn.data_source_creator.function_arn,
            index_id= index.index_id,
            role_arn=index.role.arn,
            name = "files-reinvent-v4",
            description = "",
            bucket_name=s3_deploy.bucket.bucket_name,
            language_code = 'en',
            inclusion_prefixes=["agenda_reinvent/agenda/"],
            #metadata_files_prefix = "files_es/metadata/",
            inclusion_patterns = []
        )
        
        
    