# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['StudioSessionMappingArgs', 'StudioSessionMapping']

@pulumi.input_type
class StudioSessionMappingArgs:
    def __init__(__self__, *,
                 identity_type: pulumi.Input[str],
                 session_policy_arn: pulumi.Input[str],
                 studio_id: pulumi.Input[str],
                 identity_id: Optional[pulumi.Input[str]] = None,
                 identity_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a StudioSessionMapping resource.
        :param pulumi.Input[str] identity_type: Specifies whether the identity to map to the Amazon EMR Studio is a `USER` or a `GROUP`.
        :param pulumi.Input[str] session_policy_arn: The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group. You should specify the ARN for the session policy that you want to apply, not the ARN of your user role.
        :param pulumi.Input[str] studio_id: The ID of the Amazon EMR Studio to which the user or group will be mapped.
        :param pulumi.Input[str] identity_id: The globally unique identifier (GUID) of the user or group from the Amazon Web Services SSO Identity Store.
        :param pulumi.Input[str] identity_name: The name of the user or group from the Amazon Web Services SSO Identity Store.
        """
        pulumi.set(__self__, "identity_type", identity_type)
        pulumi.set(__self__, "session_policy_arn", session_policy_arn)
        pulumi.set(__self__, "studio_id", studio_id)
        if identity_id is not None:
            pulumi.set(__self__, "identity_id", identity_id)
        if identity_name is not None:
            pulumi.set(__self__, "identity_name", identity_name)

    @property
    @pulumi.getter(name="identityType")
    def identity_type(self) -> pulumi.Input[str]:
        """
        Specifies whether the identity to map to the Amazon EMR Studio is a `USER` or a `GROUP`.
        """
        return pulumi.get(self, "identity_type")

    @identity_type.setter
    def identity_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "identity_type", value)

    @property
    @pulumi.getter(name="sessionPolicyArn")
    def session_policy_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group. You should specify the ARN for the session policy that you want to apply, not the ARN of your user role.
        """
        return pulumi.get(self, "session_policy_arn")

    @session_policy_arn.setter
    def session_policy_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "session_policy_arn", value)

    @property
    @pulumi.getter(name="studioId")
    def studio_id(self) -> pulumi.Input[str]:
        """
        The ID of the Amazon EMR Studio to which the user or group will be mapped.
        """
        return pulumi.get(self, "studio_id")

    @studio_id.setter
    def studio_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "studio_id", value)

    @property
    @pulumi.getter(name="identityId")
    def identity_id(self) -> Optional[pulumi.Input[str]]:
        """
        The globally unique identifier (GUID) of the user or group from the Amazon Web Services SSO Identity Store.
        """
        return pulumi.get(self, "identity_id")

    @identity_id.setter
    def identity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_id", value)

    @property
    @pulumi.getter(name="identityName")
    def identity_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user or group from the Amazon Web Services SSO Identity Store.
        """
        return pulumi.get(self, "identity_name")

    @identity_name.setter
    def identity_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_name", value)


@pulumi.input_type
class _StudioSessionMappingState:
    def __init__(__self__, *,
                 identity_id: Optional[pulumi.Input[str]] = None,
                 identity_name: Optional[pulumi.Input[str]] = None,
                 identity_type: Optional[pulumi.Input[str]] = None,
                 session_policy_arn: Optional[pulumi.Input[str]] = None,
                 studio_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering StudioSessionMapping resources.
        :param pulumi.Input[str] identity_id: The globally unique identifier (GUID) of the user or group from the Amazon Web Services SSO Identity Store.
        :param pulumi.Input[str] identity_name: The name of the user or group from the Amazon Web Services SSO Identity Store.
        :param pulumi.Input[str] identity_type: Specifies whether the identity to map to the Amazon EMR Studio is a `USER` or a `GROUP`.
        :param pulumi.Input[str] session_policy_arn: The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group. You should specify the ARN for the session policy that you want to apply, not the ARN of your user role.
        :param pulumi.Input[str] studio_id: The ID of the Amazon EMR Studio to which the user or group will be mapped.
        """
        if identity_id is not None:
            pulumi.set(__self__, "identity_id", identity_id)
        if identity_name is not None:
            pulumi.set(__self__, "identity_name", identity_name)
        if identity_type is not None:
            pulumi.set(__self__, "identity_type", identity_type)
        if session_policy_arn is not None:
            pulumi.set(__self__, "session_policy_arn", session_policy_arn)
        if studio_id is not None:
            pulumi.set(__self__, "studio_id", studio_id)

    @property
    @pulumi.getter(name="identityId")
    def identity_id(self) -> Optional[pulumi.Input[str]]:
        """
        The globally unique identifier (GUID) of the user or group from the Amazon Web Services SSO Identity Store.
        """
        return pulumi.get(self, "identity_id")

    @identity_id.setter
    def identity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_id", value)

    @property
    @pulumi.getter(name="identityName")
    def identity_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user or group from the Amazon Web Services SSO Identity Store.
        """
        return pulumi.get(self, "identity_name")

    @identity_name.setter
    def identity_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_name", value)

    @property
    @pulumi.getter(name="identityType")
    def identity_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether the identity to map to the Amazon EMR Studio is a `USER` or a `GROUP`.
        """
        return pulumi.get(self, "identity_type")

    @identity_type.setter
    def identity_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_type", value)

    @property
    @pulumi.getter(name="sessionPolicyArn")
    def session_policy_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group. You should specify the ARN for the session policy that you want to apply, not the ARN of your user role.
        """
        return pulumi.get(self, "session_policy_arn")

    @session_policy_arn.setter
    def session_policy_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "session_policy_arn", value)

    @property
    @pulumi.getter(name="studioId")
    def studio_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Amazon EMR Studio to which the user or group will be mapped.
        """
        return pulumi.get(self, "studio_id")

    @studio_id.setter
    def studio_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "studio_id", value)


class StudioSessionMapping(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity_id: Optional[pulumi.Input[str]] = None,
                 identity_name: Optional[pulumi.Input[str]] = None,
                 identity_type: Optional[pulumi.Input[str]] = None,
                 session_policy_arn: Optional[pulumi.Input[str]] = None,
                 studio_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Elastic MapReduce Studio Session Mapping.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.StudioSessionMapping("example",
            studio_id=aws_emr_studio["example"]["id"],
            identity_type="USER",
            identity_id="example",
            session_policy_arn=aws_iam_policy["example"]["arn"])
        ```

        ## Import

        EMR studio session mappings can be imported using the `id`, e.g., `studio-id:identity-type:identity-id`

        ```sh
         $ pulumi import aws:emr/studioSessionMapping:StudioSessionMapping example es-xxxxx:USER:xxxxx-xxx-xxx
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identity_id: The globally unique identifier (GUID) of the user or group from the Amazon Web Services SSO Identity Store.
        :param pulumi.Input[str] identity_name: The name of the user or group from the Amazon Web Services SSO Identity Store.
        :param pulumi.Input[str] identity_type: Specifies whether the identity to map to the Amazon EMR Studio is a `USER` or a `GROUP`.
        :param pulumi.Input[str] session_policy_arn: The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group. You should specify the ARN for the session policy that you want to apply, not the ARN of your user role.
        :param pulumi.Input[str] studio_id: The ID of the Amazon EMR Studio to which the user or group will be mapped.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StudioSessionMappingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Elastic MapReduce Studio Session Mapping.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.StudioSessionMapping("example",
            studio_id=aws_emr_studio["example"]["id"],
            identity_type="USER",
            identity_id="example",
            session_policy_arn=aws_iam_policy["example"]["arn"])
        ```

        ## Import

        EMR studio session mappings can be imported using the `id`, e.g., `studio-id:identity-type:identity-id`

        ```sh
         $ pulumi import aws:emr/studioSessionMapping:StudioSessionMapping example es-xxxxx:USER:xxxxx-xxx-xxx
        ```

        :param str resource_name: The name of the resource.
        :param StudioSessionMappingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StudioSessionMappingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity_id: Optional[pulumi.Input[str]] = None,
                 identity_name: Optional[pulumi.Input[str]] = None,
                 identity_type: Optional[pulumi.Input[str]] = None,
                 session_policy_arn: Optional[pulumi.Input[str]] = None,
                 studio_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = StudioSessionMappingArgs.__new__(StudioSessionMappingArgs)

            __props__.__dict__["identity_id"] = identity_id
            __props__.__dict__["identity_name"] = identity_name
            if identity_type is None and not opts.urn:
                raise TypeError("Missing required property 'identity_type'")
            __props__.__dict__["identity_type"] = identity_type
            if session_policy_arn is None and not opts.urn:
                raise TypeError("Missing required property 'session_policy_arn'")
            __props__.__dict__["session_policy_arn"] = session_policy_arn
            if studio_id is None and not opts.urn:
                raise TypeError("Missing required property 'studio_id'")
            __props__.__dict__["studio_id"] = studio_id
        super(StudioSessionMapping, __self__).__init__(
            'aws:emr/studioSessionMapping:StudioSessionMapping',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            identity_id: Optional[pulumi.Input[str]] = None,
            identity_name: Optional[pulumi.Input[str]] = None,
            identity_type: Optional[pulumi.Input[str]] = None,
            session_policy_arn: Optional[pulumi.Input[str]] = None,
            studio_id: Optional[pulumi.Input[str]] = None) -> 'StudioSessionMapping':
        """
        Get an existing StudioSessionMapping resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identity_id: The globally unique identifier (GUID) of the user or group from the Amazon Web Services SSO Identity Store.
        :param pulumi.Input[str] identity_name: The name of the user or group from the Amazon Web Services SSO Identity Store.
        :param pulumi.Input[str] identity_type: Specifies whether the identity to map to the Amazon EMR Studio is a `USER` or a `GROUP`.
        :param pulumi.Input[str] session_policy_arn: The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group. You should specify the ARN for the session policy that you want to apply, not the ARN of your user role.
        :param pulumi.Input[str] studio_id: The ID of the Amazon EMR Studio to which the user or group will be mapped.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StudioSessionMappingState.__new__(_StudioSessionMappingState)

        __props__.__dict__["identity_id"] = identity_id
        __props__.__dict__["identity_name"] = identity_name
        __props__.__dict__["identity_type"] = identity_type
        __props__.__dict__["session_policy_arn"] = session_policy_arn
        __props__.__dict__["studio_id"] = studio_id
        return StudioSessionMapping(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="identityId")
    def identity_id(self) -> pulumi.Output[str]:
        """
        The globally unique identifier (GUID) of the user or group from the Amazon Web Services SSO Identity Store.
        """
        return pulumi.get(self, "identity_id")

    @property
    @pulumi.getter(name="identityName")
    def identity_name(self) -> pulumi.Output[str]:
        """
        The name of the user or group from the Amazon Web Services SSO Identity Store.
        """
        return pulumi.get(self, "identity_name")

    @property
    @pulumi.getter(name="identityType")
    def identity_type(self) -> pulumi.Output[str]:
        """
        Specifies whether the identity to map to the Amazon EMR Studio is a `USER` or a `GROUP`.
        """
        return pulumi.get(self, "identity_type")

    @property
    @pulumi.getter(name="sessionPolicyArn")
    def session_policy_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) for the session policy that will be applied to the user or group. You should specify the ARN for the session policy that you want to apply, not the ARN of your user role.
        """
        return pulumi.get(self, "session_policy_arn")

    @property
    @pulumi.getter(name="studioId")
    def studio_id(self) -> pulumi.Output[str]:
        """
        The ID of the Amazon EMR Studio to which the user or group will be mapped.
        """
        return pulumi.get(self, "studio_id")

