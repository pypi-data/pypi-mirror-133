import json
from typing import Optional

from aws_cdk.core import Stack, CustomResource, RemovalPolicy

from b_cfn_twilio.cfn_workflow.function import TwilioWorkflowSingletonFunction


class TwilioWorkflowResource(CustomResource):
    """
    Custom resource used for managing a Twilio Workflow for a deployment.

    Creates Workflow on stack creation.
    Updates Workflow when parameters change.
    Deletes Workflow on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str,
            twilio_account_sid: str,
            twilio_auth_token: str,
            twilio_workspace_sid: str,
            workflow_name: str,
            task_queue_sid: str,
            assignment_callback_url: Optional[str] = None,
            fallback_assignment_callback_url: Optional[str] = None,
            task_reservation_timeout: Optional[int] = None
    ) -> None:
        """

        :param scope: CloudFormation template stack in which this resource will belong.
        :param name: Custom resource name.
        :param twilio_account_sid: Twilio Account SID.
        :param twilio_auth_token: Twilio Auth SID.
        :param twilio_workspace_sid: Twilio Workspace SID.
        :param workflow_name: Name that will be provided to the created Workflow.
        :param task_queue_sid: TaskQueue that will be assigned as default queue for this Workflow.
        :param assignment_callback_url: Endpoint URL where Twilio will get instructions how to assign a call to a worker.
        :param fallback_assignment_callback_url: Secondary assignment endpoint URL.
        :param task_reservation_timeout: This is the value (in seconds), on how long a task should be reserved before going to the next matching worker.
        """

        workflow_function = TwilioWorkflowSingletonFunction(
            scope=scope,
            name=f'{name}Function'
        )

        super().__init__(
            scope=scope,
            id=f'CustomResource{name}',
            service_token=workflow_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'TwilioWorkflowName': workflow_name,
                'WorkflowConfiguration': json.dumps({
                    'task_routing': {
                        'filters': [],
                        'default_filter': {
                            'queue': task_queue_sid
                        }
                    }
                }),
                'AssignmentCallbackUrl': assignment_callback_url,
                'FallbackAssignmentCallbackUrl': fallback_assignment_callback_url,
                'TaskReservationTimeout': task_reservation_timeout,
                'TwilioAccountSid': twilio_account_sid,
                'TwilioAuthToken': twilio_auth_token,
                'TwilioWorkspaceSid': twilio_workspace_sid,
            }
        )

    @property
    def workflow_sid(self) -> str:
        """
        Get the Workflow SID output from the custom resource.

        :return: Workflow SID string.
        """

        return self.get_att_string("WorkflowSid")
