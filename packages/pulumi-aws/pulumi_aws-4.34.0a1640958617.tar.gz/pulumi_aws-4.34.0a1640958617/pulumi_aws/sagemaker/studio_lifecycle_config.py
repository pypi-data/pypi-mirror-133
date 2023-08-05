# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['StudioLifecycleConfigArgs', 'StudioLifecycleConfig']

@pulumi.input_type
class StudioLifecycleConfigArgs:
    def __init__(__self__, *,
                 studio_lifecycle_config_app_type: pulumi.Input[str],
                 studio_lifecycle_config_content: pulumi.Input[str],
                 studio_lifecycle_config_name: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a StudioLifecycleConfig resource.
        :param pulumi.Input[str] studio_lifecycle_config_app_type: The App type that the Lifecycle Configuration is attached to. Valid values are `JupyterServer` and `KernelGateway`.
        :param pulumi.Input[str] studio_lifecycle_config_content: The content of your Studio Lifecycle Configuration script. This content must be base64 encoded.
        :param pulumi.Input[str] studio_lifecycle_config_name: The name of the Studio Lifecycle Configuration to create.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "studio_lifecycle_config_app_type", studio_lifecycle_config_app_type)
        pulumi.set(__self__, "studio_lifecycle_config_content", studio_lifecycle_config_content)
        pulumi.set(__self__, "studio_lifecycle_config_name", studio_lifecycle_config_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="studioLifecycleConfigAppType")
    def studio_lifecycle_config_app_type(self) -> pulumi.Input[str]:
        """
        The App type that the Lifecycle Configuration is attached to. Valid values are `JupyterServer` and `KernelGateway`.
        """
        return pulumi.get(self, "studio_lifecycle_config_app_type")

    @studio_lifecycle_config_app_type.setter
    def studio_lifecycle_config_app_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "studio_lifecycle_config_app_type", value)

    @property
    @pulumi.getter(name="studioLifecycleConfigContent")
    def studio_lifecycle_config_content(self) -> pulumi.Input[str]:
        """
        The content of your Studio Lifecycle Configuration script. This content must be base64 encoded.
        """
        return pulumi.get(self, "studio_lifecycle_config_content")

    @studio_lifecycle_config_content.setter
    def studio_lifecycle_config_content(self, value: pulumi.Input[str]):
        pulumi.set(self, "studio_lifecycle_config_content", value)

    @property
    @pulumi.getter(name="studioLifecycleConfigName")
    def studio_lifecycle_config_name(self) -> pulumi.Input[str]:
        """
        The name of the Studio Lifecycle Configuration to create.
        """
        return pulumi.get(self, "studio_lifecycle_config_name")

    @studio_lifecycle_config_name.setter
    def studio_lifecycle_config_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "studio_lifecycle_config_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _StudioLifecycleConfigState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 studio_lifecycle_config_app_type: Optional[pulumi.Input[str]] = None,
                 studio_lifecycle_config_content: Optional[pulumi.Input[str]] = None,
                 studio_lifecycle_config_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering StudioLifecycleConfig resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Studio Lifecycle Config.
        :param pulumi.Input[str] studio_lifecycle_config_app_type: The App type that the Lifecycle Configuration is attached to. Valid values are `JupyterServer` and `KernelGateway`.
        :param pulumi.Input[str] studio_lifecycle_config_content: The content of your Studio Lifecycle Configuration script. This content must be base64 encoded.
        :param pulumi.Input[str] studio_lifecycle_config_name: The name of the Studio Lifecycle Configuration to create.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if studio_lifecycle_config_app_type is not None:
            pulumi.set(__self__, "studio_lifecycle_config_app_type", studio_lifecycle_config_app_type)
        if studio_lifecycle_config_content is not None:
            pulumi.set(__self__, "studio_lifecycle_config_content", studio_lifecycle_config_content)
        if studio_lifecycle_config_name is not None:
            pulumi.set(__self__, "studio_lifecycle_config_name", studio_lifecycle_config_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Studio Lifecycle Config.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="studioLifecycleConfigAppType")
    def studio_lifecycle_config_app_type(self) -> Optional[pulumi.Input[str]]:
        """
        The App type that the Lifecycle Configuration is attached to. Valid values are `JupyterServer` and `KernelGateway`.
        """
        return pulumi.get(self, "studio_lifecycle_config_app_type")

    @studio_lifecycle_config_app_type.setter
    def studio_lifecycle_config_app_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "studio_lifecycle_config_app_type", value)

    @property
    @pulumi.getter(name="studioLifecycleConfigContent")
    def studio_lifecycle_config_content(self) -> Optional[pulumi.Input[str]]:
        """
        The content of your Studio Lifecycle Configuration script. This content must be base64 encoded.
        """
        return pulumi.get(self, "studio_lifecycle_config_content")

    @studio_lifecycle_config_content.setter
    def studio_lifecycle_config_content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "studio_lifecycle_config_content", value)

    @property
    @pulumi.getter(name="studioLifecycleConfigName")
    def studio_lifecycle_config_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Studio Lifecycle Configuration to create.
        """
        return pulumi.get(self, "studio_lifecycle_config_name")

    @studio_lifecycle_config_name.setter
    def studio_lifecycle_config_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "studio_lifecycle_config_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class StudioLifecycleConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 studio_lifecycle_config_app_type: Optional[pulumi.Input[str]] = None,
                 studio_lifecycle_config_content: Optional[pulumi.Input[str]] = None,
                 studio_lifecycle_config_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Sagemaker Studio Lifecycle Config resource.

        ## Example Usage

        ## Import

        Sagemaker Code Studio Lifecycle Configs can be imported using the `studio_lifecycle_config_name`, e.g.,

        ```sh
         $ pulumi import aws:sagemaker/studioLifecycleConfig:StudioLifecycleConfig example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] studio_lifecycle_config_app_type: The App type that the Lifecycle Configuration is attached to. Valid values are `JupyterServer` and `KernelGateway`.
        :param pulumi.Input[str] studio_lifecycle_config_content: The content of your Studio Lifecycle Configuration script. This content must be base64 encoded.
        :param pulumi.Input[str] studio_lifecycle_config_name: The name of the Studio Lifecycle Configuration to create.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StudioLifecycleConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Sagemaker Studio Lifecycle Config resource.

        ## Example Usage

        ## Import

        Sagemaker Code Studio Lifecycle Configs can be imported using the `studio_lifecycle_config_name`, e.g.,

        ```sh
         $ pulumi import aws:sagemaker/studioLifecycleConfig:StudioLifecycleConfig example example
        ```

        :param str resource_name: The name of the resource.
        :param StudioLifecycleConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StudioLifecycleConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 studio_lifecycle_config_app_type: Optional[pulumi.Input[str]] = None,
                 studio_lifecycle_config_content: Optional[pulumi.Input[str]] = None,
                 studio_lifecycle_config_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = StudioLifecycleConfigArgs.__new__(StudioLifecycleConfigArgs)

            if studio_lifecycle_config_app_type is None and not opts.urn:
                raise TypeError("Missing required property 'studio_lifecycle_config_app_type'")
            __props__.__dict__["studio_lifecycle_config_app_type"] = studio_lifecycle_config_app_type
            if studio_lifecycle_config_content is None and not opts.urn:
                raise TypeError("Missing required property 'studio_lifecycle_config_content'")
            __props__.__dict__["studio_lifecycle_config_content"] = studio_lifecycle_config_content
            if studio_lifecycle_config_name is None and not opts.urn:
                raise TypeError("Missing required property 'studio_lifecycle_config_name'")
            __props__.__dict__["studio_lifecycle_config_name"] = studio_lifecycle_config_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(StudioLifecycleConfig, __self__).__init__(
            'aws:sagemaker/studioLifecycleConfig:StudioLifecycleConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            studio_lifecycle_config_app_type: Optional[pulumi.Input[str]] = None,
            studio_lifecycle_config_content: Optional[pulumi.Input[str]] = None,
            studio_lifecycle_config_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'StudioLifecycleConfig':
        """
        Get an existing StudioLifecycleConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Studio Lifecycle Config.
        :param pulumi.Input[str] studio_lifecycle_config_app_type: The App type that the Lifecycle Configuration is attached to. Valid values are `JupyterServer` and `KernelGateway`.
        :param pulumi.Input[str] studio_lifecycle_config_content: The content of your Studio Lifecycle Configuration script. This content must be base64 encoded.
        :param pulumi.Input[str] studio_lifecycle_config_name: The name of the Studio Lifecycle Configuration to create.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StudioLifecycleConfigState.__new__(_StudioLifecycleConfigState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["studio_lifecycle_config_app_type"] = studio_lifecycle_config_app_type
        __props__.__dict__["studio_lifecycle_config_content"] = studio_lifecycle_config_content
        __props__.__dict__["studio_lifecycle_config_name"] = studio_lifecycle_config_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return StudioLifecycleConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Studio Lifecycle Config.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="studioLifecycleConfigAppType")
    def studio_lifecycle_config_app_type(self) -> pulumi.Output[str]:
        """
        The App type that the Lifecycle Configuration is attached to. Valid values are `JupyterServer` and `KernelGateway`.
        """
        return pulumi.get(self, "studio_lifecycle_config_app_type")

    @property
    @pulumi.getter(name="studioLifecycleConfigContent")
    def studio_lifecycle_config_content(self) -> pulumi.Output[str]:
        """
        The content of your Studio Lifecycle Configuration script. This content must be base64 encoded.
        """
        return pulumi.get(self, "studio_lifecycle_config_content")

    @property
    @pulumi.getter(name="studioLifecycleConfigName")
    def studio_lifecycle_config_name(self) -> pulumi.Output[str]:
        """
        The name of the Studio Lifecycle Configuration to create.
        """
        return pulumi.get(self, "studio_lifecycle_config_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

