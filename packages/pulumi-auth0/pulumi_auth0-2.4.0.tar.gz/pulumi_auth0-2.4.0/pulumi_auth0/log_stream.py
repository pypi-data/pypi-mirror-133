# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['LogStreamArgs', 'LogStream']

@pulumi.input_type
class LogStreamArgs:
    def __init__(__self__, *,
                 sink: pulumi.Input['LogStreamSinkArgs'],
                 type: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a LogStream resource.
        :param pulumi.Input['LogStreamSinkArgs'] sink: List(Resource) The sink configuration for the log stream. For details, see Sink Configuration.
        :param pulumi.Input[str] type: The type of log stream. Options are "eventbridge", "eventgrid", "http", "datadog", "splunk", "sumo"
        :param pulumi.Input[str] name: Name of the log stream
        :param pulumi.Input[str] status: The current status of the log stream. Options are "active", "paused", "suspended"
        """
        pulumi.set(__self__, "sink", sink)
        pulumi.set(__self__, "type", type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def sink(self) -> pulumi.Input['LogStreamSinkArgs']:
        """
        List(Resource) The sink configuration for the log stream. For details, see Sink Configuration.
        """
        return pulumi.get(self, "sink")

    @sink.setter
    def sink(self, value: pulumi.Input['LogStreamSinkArgs']):
        pulumi.set(self, "sink", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of log stream. Options are "eventbridge", "eventgrid", "http", "datadog", "splunk", "sumo"
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the log stream
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The current status of the log stream. Options are "active", "paused", "suspended"
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _LogStreamState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 sink: Optional[pulumi.Input['LogStreamSinkArgs']] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LogStream resources.
        :param pulumi.Input[str] name: Name of the log stream
        :param pulumi.Input['LogStreamSinkArgs'] sink: List(Resource) The sink configuration for the log stream. For details, see Sink Configuration.
        :param pulumi.Input[str] status: The current status of the log stream. Options are "active", "paused", "suspended"
        :param pulumi.Input[str] type: The type of log stream. Options are "eventbridge", "eventgrid", "http", "datadog", "splunk", "sumo"
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if sink is not None:
            pulumi.set(__self__, "sink", sink)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the log stream
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def sink(self) -> Optional[pulumi.Input['LogStreamSinkArgs']]:
        """
        List(Resource) The sink configuration for the log stream. For details, see Sink Configuration.
        """
        return pulumi.get(self, "sink")

    @sink.setter
    def sink(self, value: Optional[pulumi.Input['LogStreamSinkArgs']]):
        pulumi.set(self, "sink", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The current status of the log stream. Options are "active", "paused", "suspended"
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of log stream. Options are "eventbridge", "eventgrid", "http", "datadog", "splunk", "sumo"
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class LogStream(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sink: Optional[pulumi.Input[pulumi.InputType['LogStreamSinkArgs']]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        With this resource, you can manage your Auth0 log streams.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        example = auth0.LogStream("example",
            sink=auth0.LogStreamSinkArgs(
                aws_account_id="my_account_id",
                aws_region="us-east-2",
            ),
            status="active",
            type="eventbridge")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the log stream
        :param pulumi.Input[pulumi.InputType['LogStreamSinkArgs']] sink: List(Resource) The sink configuration for the log stream. For details, see Sink Configuration.
        :param pulumi.Input[str] status: The current status of the log stream. Options are "active", "paused", "suspended"
        :param pulumi.Input[str] type: The type of log stream. Options are "eventbridge", "eventgrid", "http", "datadog", "splunk", "sumo"
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LogStreamArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        With this resource, you can manage your Auth0 log streams.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        example = auth0.LogStream("example",
            sink=auth0.LogStreamSinkArgs(
                aws_account_id="my_account_id",
                aws_region="us-east-2",
            ),
            status="active",
            type="eventbridge")
        ```

        :param str resource_name: The name of the resource.
        :param LogStreamArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LogStreamArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sink: Optional[pulumi.Input[pulumi.InputType['LogStreamSinkArgs']]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LogStreamArgs.__new__(LogStreamArgs)

            __props__.__dict__["name"] = name
            if sink is None and not opts.urn:
                raise TypeError("Missing required property 'sink'")
            __props__.__dict__["sink"] = sink
            __props__.__dict__["status"] = status
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
        super(LogStream, __self__).__init__(
            'auth0:index/logStream:LogStream',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            sink: Optional[pulumi.Input[pulumi.InputType['LogStreamSinkArgs']]] = None,
            status: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'LogStream':
        """
        Get an existing LogStream resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the log stream
        :param pulumi.Input[pulumi.InputType['LogStreamSinkArgs']] sink: List(Resource) The sink configuration for the log stream. For details, see Sink Configuration.
        :param pulumi.Input[str] status: The current status of the log stream. Options are "active", "paused", "suspended"
        :param pulumi.Input[str] type: The type of log stream. Options are "eventbridge", "eventgrid", "http", "datadog", "splunk", "sumo"
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LogStreamState.__new__(_LogStreamState)

        __props__.__dict__["name"] = name
        __props__.__dict__["sink"] = sink
        __props__.__dict__["status"] = status
        __props__.__dict__["type"] = type
        return LogStream(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the log stream
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sink(self) -> pulumi.Output['outputs.LogStreamSink']:
        """
        List(Resource) The sink configuration for the log stream. For details, see Sink Configuration.
        """
        return pulumi.get(self, "sink")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The current status of the log stream. Options are "active", "paused", "suspended"
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of log stream. Options are "eventbridge", "eventgrid", "http", "datadog", "splunk", "sumo"
        """
        return pulumi.get(self, "type")

