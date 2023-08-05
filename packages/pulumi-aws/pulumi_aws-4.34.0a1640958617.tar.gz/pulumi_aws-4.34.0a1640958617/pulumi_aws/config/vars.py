# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

import types

__config__ = pulumi.Config('aws')


class _ExportableConfig(types.ModuleType):
    @property
    def access_key(self) -> Optional[str]:
        """
        The access key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console.
        """
        return __config__.get('accessKey')

    @property
    def allowed_account_ids(self) -> Optional[str]:
        return __config__.get('allowedAccountIds')

    @property
    def assume_role(self) -> Optional[str]:
        return __config__.get('assumeRole')

    @property
    def default_tags(self) -> Optional[str]:
        """
        Configuration block with settings to default resource tags across all resources.
        """
        return __config__.get('defaultTags')

    @property
    def endpoints(self) -> Optional[str]:
        return __config__.get('endpoints')

    @property
    def forbidden_account_ids(self) -> Optional[str]:
        return __config__.get('forbiddenAccountIds')

    @property
    def http_proxy(self) -> Optional[str]:
        """
        The address of an HTTP proxy to use when accessing the AWS API. Can also be configured using the `HTTP_PROXY` or
        `HTTPS_PROXY` environment variables.
        """
        return __config__.get('httpProxy')

    @property
    def ignore_tags(self) -> Optional[str]:
        """
        Configuration block with settings to ignore resource tags across all resources.
        """
        return __config__.get('ignoreTags')

    @property
    def insecure(self) -> Optional[bool]:
        """
        Explicitly allow the provider to perform "insecure" SSL requests. If omitted, default value is `false`
        """
        return __config__.get_bool('insecure')

    @property
    def max_retries(self) -> Optional[int]:
        """
        The maximum number of times an AWS API request is being executed. If the API request still fails, an error is thrown.
        """
        return __config__.get_int('maxRetries')

    @property
    def profile(self) -> Optional[str]:
        """
        The profile for API operations. If not set, the default profile created with `aws configure` will be used.
        """
        return __config__.get('profile') or _utilities.get_env('AWS_PROFILE')

    @property
    def region(self) -> Optional[str]:
        """
        The region where AWS operations will take place. Examples are us-east-1, us-west-2, etc.
        """
        return __config__.get('region') or _utilities.get_env('AWS_REGION', 'AWS_DEFAULT_REGION')

    @property
    def s3_force_path_style(self) -> Optional[bool]:
        """
        Set this to true to force the request to use path-style addressing, i.e., http://s3.amazonaws.com/BUCKET/KEY. By
        default, the S3 client will use virtual hosted bucket addressing when possible (http://BUCKET.s3.amazonaws.com/KEY).
        Specific to the Amazon S3 service.
        """
        return __config__.get_bool('s3ForcePathStyle')

    @property
    def secret_key(self) -> Optional[str]:
        """
        The secret key for API operations. You can retrieve this from the 'Security & Credentials' section of the AWS console.
        """
        return __config__.get('secretKey')

    @property
    def shared_credentials_file(self) -> Optional[str]:
        """
        The path to the shared credentials file. If not set this defaults to ~/.aws/credentials.
        """
        return __config__.get('sharedCredentialsFile')

    @property
    def skip_credentials_validation(self) -> bool:
        """
        Skip the credentials validation via STS API. Used for AWS API implementations that do not have STS
        available/implemented.
        """
        return __config__.get_bool('skipCredentialsValidation') or True

    @property
    def skip_get_ec2_platforms(self) -> bool:
        """
        Skip getting the supported EC2 platforms. Used by users that don't have ec2:DescribeAccountAttributes permissions.
        """
        return __config__.get_bool('skipGetEc2Platforms') or True

    @property
    def skip_metadata_api_check(self) -> bool:
        return __config__.get_bool('skipMetadataApiCheck') or True

    @property
    def skip_region_validation(self) -> bool:
        """
        Skip static validation of region name. Used by users of alternative AWS-like APIs or users w/ access to regions that are
        not public (yet).
        """
        return __config__.get_bool('skipRegionValidation') or True

    @property
    def skip_requesting_account_id(self) -> Optional[bool]:
        """
        Skip requesting the account ID. Used for AWS API implementations that do not have IAM/STS API and/or metadata API.
        """
        return __config__.get_bool('skipRequestingAccountId')

    @property
    def token(self) -> Optional[str]:
        """
        session token. A session token is only required if you are using temporary security credentials.
        """
        return __config__.get('token')

