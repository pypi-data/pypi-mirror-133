from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio.cfn_task_queue.function import TwilioTaskQueueSingletonFunction


class TwilioTaskQueueResource(CustomResource):
    """
    Custom resource used for managing a Twilio Task Queue for a deployment.

    Creates Task Queue on stack creation.
    Updates Task Queue when parameters change.
    Deletes Task Queue on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str,
            twilio_account_sid: str,
            twilio_auth_token: str,
            twilio_workspace_sid: str,
            task_queue_name: str
    ) -> None:
        """
        Constructor.

        :param scope: CloudFormation template stack in which this resource will belong.
        :param name: Custom resource name.
        :param twilio_account_sid: Twilio Account SID.
        :param twilio_auth_token: Twilio Auth SID.
        :param twilio_workspace_sid: Twilio Workspace SID.
        :param task_queue_name: Name that will be provided to the created TaskQueue.
        """

        task_queue_function = TwilioTaskQueueSingletonFunction(
            scope=scope,
            name=f'{name}Function'
        )

        super().__init__(
            scope=scope,
            id=f'CustomResource{name}',
            service_token=task_queue_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'TwilioTaskQueueName': task_queue_name,
                'TwilioAccountSid': twilio_account_sid,
                'TwilioAuthToken': twilio_auth_token,
                'TwilioWorkspaceSid': twilio_workspace_sid
            }
        )

    @property
    def task_queue_sid(self) -> str:
        """
        Get the Task Queue SID output from the custom resource.

        :return: Task Queue SID string.
        """

        return self.get_att_string('TaskQueueSid')
