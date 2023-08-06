from __future__ import annotations

from functools import lru_cache

import b_aws_cf_response
from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack, Duration
from b_cfn_lambda_layer.package_version import PackageVersion
from b_twilio_sdk_layer.layer import Layer as TwilioLayer

import b_cfn_twilio


class TwilioTaskQueueSingletonFunction(SingletonFunction):
    """
    Custom resource Singleton Lambda function.

    Creates Task Queue on stack creation.
    Updates Task Queue when parameters change.
    Deletes Task Queue on stack deletion.
    """

    def __init__(
            self,
            scope: Stack,
            name: str
    ) -> None:
        self.__name = name

        super().__init__(
            scope=scope,
            id=name,
            uuid='4b5bfe56-7cb0-4442-bbec-9ba1ed440927',
            function_name=name,
            code=self.__code(),
            layers=[
                TwilioLayer(
                    scope=scope,
                    name=f'TwilioLayerFor{name}',
                    dependencies={
                        'b-aws-cf-response': PackageVersion.latest()
                    }
                )
            ],
            timeout=Duration.minutes(1),
            handler='main.index.handler',
            runtime=Runtime.PYTHON_3_8
        )

    @lru_cache
    def __code(self) -> Code:
        from .source import root
        return Code.from_asset(root)

    @property
    def function_name(self):
        return self.__name
