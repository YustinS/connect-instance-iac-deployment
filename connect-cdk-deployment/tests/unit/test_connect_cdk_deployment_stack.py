import aws_cdk as core
import aws_cdk.assertions as assertions

from connect_cdk_deployment.connect_cdk_deployment_stack import (
    ConnectCdkDeploymentStack,
)


def test_connect_instance_config():
    """
    Tests validating the Connect configuration as generated in
    the template
    """
    app = core.App()
    stack = ConnectCdkDeploymentStack(app, "connect-cdk-deployment")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::Connect::Instance", 1)
    template.resource_count_is("AWS::Connect::InstanceStorageConfig", 3)

    template.has_resource_properties(
        "AWS::Connect::Instance", {"Attributes": {"ContactLens": False}}
    )
