# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['VpcIpamPoolCidrArgs', 'VpcIpamPoolCidr']

@pulumi.input_type
class VpcIpamPoolCidrArgs:
    def __init__(__self__, *,
                 ipam_pool_id: pulumi.Input[str],
                 cidr: Optional[pulumi.Input[str]] = None,
                 cidr_authorization_context: Optional[pulumi.Input['VpcIpamPoolCidrCidrAuthorizationContextArgs']] = None):
        """
        The set of arguments for constructing a VpcIpamPoolCidr resource.
        :param pulumi.Input[str] ipam_pool_id: The ID of the pool to which you want to assign a CIDR.
        :param pulumi.Input[str] cidr: The CIDR you want to assign to the pool.
        :param pulumi.Input['VpcIpamPoolCidrCidrAuthorizationContextArgs'] cidr_authorization_context: A signed document that proves that you are authorized to bring the specified IP address range to Amazon using BYOIP. This is not stored in the state file. See cidr_authorization_context for more information.
        """
        pulumi.set(__self__, "ipam_pool_id", ipam_pool_id)
        if cidr is not None:
            pulumi.set(__self__, "cidr", cidr)
        if cidr_authorization_context is not None:
            pulumi.set(__self__, "cidr_authorization_context", cidr_authorization_context)

    @property
    @pulumi.getter(name="ipamPoolId")
    def ipam_pool_id(self) -> pulumi.Input[str]:
        """
        The ID of the pool to which you want to assign a CIDR.
        """
        return pulumi.get(self, "ipam_pool_id")

    @ipam_pool_id.setter
    def ipam_pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "ipam_pool_id", value)

    @property
    @pulumi.getter
    def cidr(self) -> Optional[pulumi.Input[str]]:
        """
        The CIDR you want to assign to the pool.
        """
        return pulumi.get(self, "cidr")

    @cidr.setter
    def cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr", value)

    @property
    @pulumi.getter(name="cidrAuthorizationContext")
    def cidr_authorization_context(self) -> Optional[pulumi.Input['VpcIpamPoolCidrCidrAuthorizationContextArgs']]:
        """
        A signed document that proves that you are authorized to bring the specified IP address range to Amazon using BYOIP. This is not stored in the state file. See cidr_authorization_context for more information.
        """
        return pulumi.get(self, "cidr_authorization_context")

    @cidr_authorization_context.setter
    def cidr_authorization_context(self, value: Optional[pulumi.Input['VpcIpamPoolCidrCidrAuthorizationContextArgs']]):
        pulumi.set(self, "cidr_authorization_context", value)


@pulumi.input_type
class _VpcIpamPoolCidrState:
    def __init__(__self__, *,
                 cidr: Optional[pulumi.Input[str]] = None,
                 cidr_authorization_context: Optional[pulumi.Input['VpcIpamPoolCidrCidrAuthorizationContextArgs']] = None,
                 ipam_pool_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering VpcIpamPoolCidr resources.
        :param pulumi.Input[str] cidr: The CIDR you want to assign to the pool.
        :param pulumi.Input['VpcIpamPoolCidrCidrAuthorizationContextArgs'] cidr_authorization_context: A signed document that proves that you are authorized to bring the specified IP address range to Amazon using BYOIP. This is not stored in the state file. See cidr_authorization_context for more information.
        :param pulumi.Input[str] ipam_pool_id: The ID of the pool to which you want to assign a CIDR.
        """
        if cidr is not None:
            pulumi.set(__self__, "cidr", cidr)
        if cidr_authorization_context is not None:
            pulumi.set(__self__, "cidr_authorization_context", cidr_authorization_context)
        if ipam_pool_id is not None:
            pulumi.set(__self__, "ipam_pool_id", ipam_pool_id)

    @property
    @pulumi.getter
    def cidr(self) -> Optional[pulumi.Input[str]]:
        """
        The CIDR you want to assign to the pool.
        """
        return pulumi.get(self, "cidr")

    @cidr.setter
    def cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr", value)

    @property
    @pulumi.getter(name="cidrAuthorizationContext")
    def cidr_authorization_context(self) -> Optional[pulumi.Input['VpcIpamPoolCidrCidrAuthorizationContextArgs']]:
        """
        A signed document that proves that you are authorized to bring the specified IP address range to Amazon using BYOIP. This is not stored in the state file. See cidr_authorization_context for more information.
        """
        return pulumi.get(self, "cidr_authorization_context")

    @cidr_authorization_context.setter
    def cidr_authorization_context(self, value: Optional[pulumi.Input['VpcIpamPoolCidrCidrAuthorizationContextArgs']]):
        pulumi.set(self, "cidr_authorization_context", value)

    @property
    @pulumi.getter(name="ipamPoolId")
    def ipam_pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the pool to which you want to assign a CIDR.
        """
        return pulumi.get(self, "ipam_pool_id")

    @ipam_pool_id.setter
    def ipam_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipam_pool_id", value)


class VpcIpamPoolCidr(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr: Optional[pulumi.Input[str]] = None,
                 cidr_authorization_context: Optional[pulumi.Input[pulumi.InputType['VpcIpamPoolCidrCidrAuthorizationContextArgs']]] = None,
                 ipam_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provisions a CIDR from an IPAM address pool.

        > **NOTE:** Provisioning Public IPv4 or Public IPv6 require [steps outside the scope of this resource](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-byoip.html#prepare-for-byoip). The resource accepts `message` and `signature` as part of the `cidr_authorization_context` attribute but those must be generated ahead of time. Public IPv6 CIDRs that are provisioned into a Pool with `publicly_advertisable = true` and all public IPv4 CIDRs also require creating a Route Origin Authorization (ROA) object in your Regional Internet Registry (RIR).

        ## Import

        IPAMs can be imported using the `<cidr>_<ipam-pool-id>`, e.g.

        ```sh
         $ pulumi import aws:ec2/vpcIpamPoolCidr:VpcIpamPoolCidr example 172.2.0.0/24_ipam-pool-0e634f5a1517cccdc
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr: The CIDR you want to assign to the pool.
        :param pulumi.Input[pulumi.InputType['VpcIpamPoolCidrCidrAuthorizationContextArgs']] cidr_authorization_context: A signed document that proves that you are authorized to bring the specified IP address range to Amazon using BYOIP. This is not stored in the state file. See cidr_authorization_context for more information.
        :param pulumi.Input[str] ipam_pool_id: The ID of the pool to which you want to assign a CIDR.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VpcIpamPoolCidrArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provisions a CIDR from an IPAM address pool.

        > **NOTE:** Provisioning Public IPv4 or Public IPv6 require [steps outside the scope of this resource](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-byoip.html#prepare-for-byoip). The resource accepts `message` and `signature` as part of the `cidr_authorization_context` attribute but those must be generated ahead of time. Public IPv6 CIDRs that are provisioned into a Pool with `publicly_advertisable = true` and all public IPv4 CIDRs also require creating a Route Origin Authorization (ROA) object in your Regional Internet Registry (RIR).

        ## Import

        IPAMs can be imported using the `<cidr>_<ipam-pool-id>`, e.g.

        ```sh
         $ pulumi import aws:ec2/vpcIpamPoolCidr:VpcIpamPoolCidr example 172.2.0.0/24_ipam-pool-0e634f5a1517cccdc
        ```

        :param str resource_name: The name of the resource.
        :param VpcIpamPoolCidrArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VpcIpamPoolCidrArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr: Optional[pulumi.Input[str]] = None,
                 cidr_authorization_context: Optional[pulumi.Input[pulumi.InputType['VpcIpamPoolCidrCidrAuthorizationContextArgs']]] = None,
                 ipam_pool_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = VpcIpamPoolCidrArgs.__new__(VpcIpamPoolCidrArgs)

            __props__.__dict__["cidr"] = cidr
            __props__.__dict__["cidr_authorization_context"] = cidr_authorization_context
            if ipam_pool_id is None and not opts.urn:
                raise TypeError("Missing required property 'ipam_pool_id'")
            __props__.__dict__["ipam_pool_id"] = ipam_pool_id
        super(VpcIpamPoolCidr, __self__).__init__(
            'aws:ec2/vpcIpamPoolCidr:VpcIpamPoolCidr',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cidr: Optional[pulumi.Input[str]] = None,
            cidr_authorization_context: Optional[pulumi.Input[pulumi.InputType['VpcIpamPoolCidrCidrAuthorizationContextArgs']]] = None,
            ipam_pool_id: Optional[pulumi.Input[str]] = None) -> 'VpcIpamPoolCidr':
        """
        Get an existing VpcIpamPoolCidr resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr: The CIDR you want to assign to the pool.
        :param pulumi.Input[pulumi.InputType['VpcIpamPoolCidrCidrAuthorizationContextArgs']] cidr_authorization_context: A signed document that proves that you are authorized to bring the specified IP address range to Amazon using BYOIP. This is not stored in the state file. See cidr_authorization_context for more information.
        :param pulumi.Input[str] ipam_pool_id: The ID of the pool to which you want to assign a CIDR.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VpcIpamPoolCidrState.__new__(_VpcIpamPoolCidrState)

        __props__.__dict__["cidr"] = cidr
        __props__.__dict__["cidr_authorization_context"] = cidr_authorization_context
        __props__.__dict__["ipam_pool_id"] = ipam_pool_id
        return VpcIpamPoolCidr(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cidr(self) -> pulumi.Output[str]:
        """
        The CIDR you want to assign to the pool.
        """
        return pulumi.get(self, "cidr")

    @property
    @pulumi.getter(name="cidrAuthorizationContext")
    def cidr_authorization_context(self) -> pulumi.Output[Optional['outputs.VpcIpamPoolCidrCidrAuthorizationContext']]:
        """
        A signed document that proves that you are authorized to bring the specified IP address range to Amazon using BYOIP. This is not stored in the state file. See cidr_authorization_context for more information.
        """
        return pulumi.get(self, "cidr_authorization_context")

    @property
    @pulumi.getter(name="ipamPoolId")
    def ipam_pool_id(self) -> pulumi.Output[str]:
        """
        The ID of the pool to which you want to assign a CIDR.
        """
        return pulumi.get(self, "ipam_pool_id")

