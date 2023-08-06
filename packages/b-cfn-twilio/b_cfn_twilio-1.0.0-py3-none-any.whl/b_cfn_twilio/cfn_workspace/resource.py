from typing import Optional, List

from aws_cdk.core import Stack, CustomResource, RemovalPolicy
from twilio.rest.taskrouter.v1.workspace import WorkspaceInstance

from b_cfn_twilio.cfn_workspace.function import TwilioWorkspaceSingletonFunction


class TwilioWorkspaceResource(CustomResource):
    """
    Custom resource used for managing a Twilio Workspace for a deployment.

    Creates Workspace on stack creation.
    Updates Workspace on workspace name change.
    Deletes Workspace on stack deletion.


    """

    def __init__(
            self,
            scope: Stack,
            name: str,
            twilio_account_sid: str,
            twilio_auth_token: str,
            workspace_name: str,
            event_callback_url: Optional[str] = None,
            events_filter: Optional[List[str]] = None,
            multi_task_enabled: Optional[bool] = None,
            prioritize_queue_order: Optional[WorkspaceInstance.QueueOrder] = None
    ) -> None:
        """
        Constructor.

        :param scope: CloudFormation template stack in which this resource will belong.
        :param name: Custom resource name.
        :param twilio_account_sid: Twilio Account SID.
        :param twilio_auth_token: Twilio Auth SID.
        :param workspace_name: Name that will be provided to the created Workspace.
        :param event_callback_url: Endpoint URL where Twilio will send callback information.
        :param events_filter:The list of Workspace events for which to call event_callback_url
        :param multi_task_enabled: Whether multi-tasking is enabled.
        :param prioritize_queue_order: The type of TaskQueue to prioritize when Workers are receiving Tasks from both types of TaskQueues.
        """

        workspace_function = TwilioWorkspaceSingletonFunction(
            scope=scope,
            name=f'{name}Function'
        )

        super().__init__(
            scope=scope,
            id=f'CustomResource{name}',
            service_token=workspace_function.function_arn,
            pascal_case_properties=True,
            removal_policy=RemovalPolicy.DESTROY,
            properties={
                'WorkspaceName': workspace_name,
                'EventCallbackUrl': event_callback_url,
                'EventsFilter': events_filter,
                'MultiTaskEnabled': multi_task_enabled,
                'PrioritizeQueueOrder': prioritize_queue_order,
                'TwilioAccountSid': twilio_account_sid,
                'TwilioAuthToken': twilio_auth_token
            }
        )

    @property
    def workspace_sid(self) -> str:
        """
        Get the Workspace SID output from the custom resource.

        :return: Workspace SID string.
        """

        return self.get_att_string("WorkspaceSid")
