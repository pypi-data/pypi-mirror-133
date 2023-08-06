from __future__ import annotations

from functools import lru_cache

from aws_cdk.aws_lambda import Code, SingletonFunction, Runtime
from aws_cdk.core import Stack, Duration
from b_cfn_lambda_layer.package_version import PackageVersion
from b_twilio_sdk_layer.layer import Layer as TwilioLayer


class TwilioActivitySingletonFunction(SingletonFunction):
    """
    Custom activity resource Singleton Lambda function.

    Creates activities on stack creation.
    Updates activities, sets new defaults, renames, etc.
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
            uuid='c854810d-19d3-4cbb-beae-20c5f12cf992',
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
