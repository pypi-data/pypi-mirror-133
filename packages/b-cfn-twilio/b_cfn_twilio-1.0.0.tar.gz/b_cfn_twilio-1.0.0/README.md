# B.CfnTwilio

A collection of AWS CDK based Twilio resources.

### Description

This library is intended to simplify Twilio Resource management. It helps manage resources such as Activities, TaskQueues, Workflows and Workspaces in an AWS
Architecture.

**NOTE!** In order to use this layer, a `docker` command must be available on your machine. It is because the CDK runs a bundling command on a docker container
to create the Twilio dependency.

### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science industry by sharing its IT knowledge with other companies and the community. This is an open
source library intended to be used by anyone. Improvements and pull requests are welcome.

### Related technology

- Python 3
- AWS CDK
- Twilio

### Assumptions

The project assumes the following:

- You have basic-good knowledge in python programming.
- You have basic-good knowledge in AWS and AWS CDK.
- You have basic knowledge in Twilio.

### Useful sources

- Read more about Twilio SDK:<br>
  https://www.twilio.com/docs/libraries/python

### Install

The project is built and uploaded to PyPi. Install it by using pip.

```
pip install b_cfn_twilio
```

Or directly install it through source.

```
pip install .
```

### Usage & Examples

Create a Twilio Workspace:

```python
from b_cfn_twilio.cfn_workspace.resource import TwilioWorkspaceResource

workspace = TwilioWorkspaceResource(
    scope=stack,
    name='WorkspaceResource',
    workspace_name='WorkspaceName',
    twilio_account_sid='TWILIO_ACCOUNT_SID',
    twilio_auth_token='TWILIO_AUTH_TOKEN'
)

print(workspace.workspace_sid)

```

Create a Twilio Workflow:

```python
from b_cfn_twilio.cfn_task_queue.resource import TwilioTaskQueueResource

task_queue = TwilioTaskQueueResource(
    scope=stack,
    name='TaskQueueResource',
    task_queue_name='TaskQueueName',
    twilio_account_sid='TWILIO_ACCOUNT_SID',
    twilio_auth_token='TWILIO_AUTH_TOKEN',
    twilio_workspace_sid=workspace.workspace_sid
)

print(task_queue.task_queue_sid)

```

Create a Twilio TaskQueue:

```python
from b_cfn_twilio.cfn_workflow.resource import TwilioWorkflowResource

workflow = TwilioWorkflowResource(
    scope=stack,
    name='WorkflowResource',
    workflow_name='Workflow',
    task_queue_sid=task_queue.task_queue_sid,
    twilio_account_sid='TWILIO_ACCOUNT_SID',
    twilio_auth_token='TWILIO_AUTH_TOKEN',
    twilio_workspace_sid=workspace.workspace_sid
)

print(workflow.workflow_sid)

```

Create Twilio Activities:

```python
from b_cfn_twilio.cfn_activity.resource import TwilioActivityResource
from b_cfn_twilio.cfn_activity.twilio_activity import TwilioActivity

activities = TwilioActivityResource(
    scope=stack,
    name='ActivityResource',
    activities=[
        TwilioActivity('Available', True, False),
        TwilioActivity('Unavailable', False, True)
    ],
    twilio_account_sid='TWILIO_ACCOUNT_SID',
    twilio_auth_token='TWILIO_AUTH_TOKEN',
    twilio_workspace_sid=workspace.workspace_sid
)

print(activities.get_activity_sid('Available'))
print(activities.get_activity_sid('Unavailable'))

```

### Testing

This package has integration tests based on pytest. To run tests simply run:

```
pytest b_cfn_twilio_test/integration/tests
```

### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us directly, create a pull-request or an issue in github platform. Lets modernize the world
together.