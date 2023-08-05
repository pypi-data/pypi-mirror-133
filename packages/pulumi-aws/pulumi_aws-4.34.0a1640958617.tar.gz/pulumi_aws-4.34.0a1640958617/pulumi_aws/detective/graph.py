# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['GraphArgs', 'Graph']

@pulumi.input_type
class GraphArgs:
    def __init__(__self__, *,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Graph resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the instance. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the instance. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


@pulumi.input_type
class _GraphState:
    def __init__(__self__, *,
                 created_time: Optional[pulumi.Input[str]] = None,
                 graph_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Graph resources.
        :param pulumi.Input[str] created_time: Date and time, in UTC and extended RFC 3339 format, when the Amazon Detective Graph was created.
        :param pulumi.Input[str] graph_arn: ARN of the Detective Graph.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the instance. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if created_time is not None:
            pulumi.set(__self__, "created_time", created_time)
        if graph_arn is not None:
            pulumi.set(__self__, "graph_arn", graph_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[pulumi.Input[str]]:
        """
        Date and time, in UTC and extended RFC 3339 format, when the Amazon Detective Graph was created.
        """
        return pulumi.get(self, "created_time")

    @created_time.setter
    def created_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_time", value)

    @property
    @pulumi.getter(name="graphArn")
    def graph_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Detective Graph.
        """
        return pulumi.get(self, "graph_arn")

    @graph_arn.setter
    def graph_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "graph_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the instance. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class Graph(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a resource to manage an [AWS Detective Graph](https://docs.aws.amazon.com/detective/latest/APIReference/API_CreateGraph.html). As an AWS account may own only one Detective graph per region, provisioning multiple Detective graphs requires a separate provider configuration for each graph.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.detective.Graph("example", tags={
            "Name": "example-detective-graph",
        })
        ```

        ## Import

        `aws_detective_graph` can be imported using the arn, e.g.

        ```sh
         $ pulumi import aws:detective/graph:Graph example arn:aws:detective:us-east-1:123456789101:graph:231684d34gh74g4bae1dbc7bd807d02d
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the instance. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[GraphArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage an [AWS Detective Graph](https://docs.aws.amazon.com/detective/latest/APIReference/API_CreateGraph.html). As an AWS account may own only one Detective graph per region, provisioning multiple Detective graphs requires a separate provider configuration for each graph.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.detective.Graph("example", tags={
            "Name": "example-detective-graph",
        })
        ```

        ## Import

        `aws_detective_graph` can be imported using the arn, e.g.

        ```sh
         $ pulumi import aws:detective/graph:Graph example arn:aws:detective:us-east-1:123456789101:graph:231684d34gh74g4bae1dbc7bd807d02d
        ```

        :param str resource_name: The name of the resource.
        :param GraphArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GraphArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = GraphArgs.__new__(GraphArgs)

            __props__.__dict__["tags"] = tags
            __props__.__dict__["tags_all"] = tags_all
            __props__.__dict__["created_time"] = None
            __props__.__dict__["graph_arn"] = None
        super(Graph, __self__).__init__(
            'aws:detective/graph:Graph',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_time: Optional[pulumi.Input[str]] = None,
            graph_arn: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Graph':
        """
        Get an existing Graph resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_time: Date and time, in UTC and extended RFC 3339 format, when the Amazon Detective Graph was created.
        :param pulumi.Input[str] graph_arn: ARN of the Detective Graph.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the instance. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GraphState.__new__(_GraphState)

        __props__.__dict__["created_time"] = created_time
        __props__.__dict__["graph_arn"] = graph_arn
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Graph(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> pulumi.Output[str]:
        """
        Date and time, in UTC and extended RFC 3339 format, when the Amazon Detective Graph was created.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="graphArn")
    def graph_arn(self) -> pulumi.Output[str]:
        """
        ARN of the Detective Graph.
        """
        return pulumi.get(self, "graph_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the instance. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "tags_all")

