import aws_cdk as core
import aws_cdk.assertions as assertions

from re_invent_agent.re_invent_agent_stack import ReInventAgentStack

# example tests. To run these tests, uncomment this file along with the example
# resource in re_invent_agent/re_invent_agent_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ReInventAgentStack(app, "re-invent-agent")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
