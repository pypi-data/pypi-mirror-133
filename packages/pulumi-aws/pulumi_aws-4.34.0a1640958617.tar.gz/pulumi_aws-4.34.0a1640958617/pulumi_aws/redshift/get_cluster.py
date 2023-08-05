# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetClusterResult',
    'AwaitableGetClusterResult',
    'get_cluster',
    'get_cluster_output',
]

@pulumi.output_type
class GetClusterResult:
    """
    A collection of values returned by getCluster.
    """
    def __init__(__self__, allow_version_upgrade=None, automated_snapshot_retention_period=None, availability_zone=None, bucket_name=None, cluster_identifier=None, cluster_parameter_group_name=None, cluster_public_key=None, cluster_revision_number=None, cluster_security_groups=None, cluster_subnet_group_name=None, cluster_type=None, cluster_version=None, database_name=None, elastic_ip=None, enable_logging=None, encrypted=None, endpoint=None, enhanced_vpc_routing=None, iam_roles=None, id=None, kms_key_id=None, master_username=None, node_type=None, number_of_nodes=None, port=None, preferred_maintenance_window=None, publicly_accessible=None, s3_key_prefix=None, tags=None, vpc_id=None, vpc_security_group_ids=None):
        if allow_version_upgrade and not isinstance(allow_version_upgrade, bool):
            raise TypeError("Expected argument 'allow_version_upgrade' to be a bool")
        pulumi.set(__self__, "allow_version_upgrade", allow_version_upgrade)
        if automated_snapshot_retention_period and not isinstance(automated_snapshot_retention_period, int):
            raise TypeError("Expected argument 'automated_snapshot_retention_period' to be a int")
        pulumi.set(__self__, "automated_snapshot_retention_period", automated_snapshot_retention_period)
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        pulumi.set(__self__, "availability_zone", availability_zone)
        if bucket_name and not isinstance(bucket_name, str):
            raise TypeError("Expected argument 'bucket_name' to be a str")
        pulumi.set(__self__, "bucket_name", bucket_name)
        if cluster_identifier and not isinstance(cluster_identifier, str):
            raise TypeError("Expected argument 'cluster_identifier' to be a str")
        pulumi.set(__self__, "cluster_identifier", cluster_identifier)
        if cluster_parameter_group_name and not isinstance(cluster_parameter_group_name, str):
            raise TypeError("Expected argument 'cluster_parameter_group_name' to be a str")
        pulumi.set(__self__, "cluster_parameter_group_name", cluster_parameter_group_name)
        if cluster_public_key and not isinstance(cluster_public_key, str):
            raise TypeError("Expected argument 'cluster_public_key' to be a str")
        pulumi.set(__self__, "cluster_public_key", cluster_public_key)
        if cluster_revision_number and not isinstance(cluster_revision_number, str):
            raise TypeError("Expected argument 'cluster_revision_number' to be a str")
        pulumi.set(__self__, "cluster_revision_number", cluster_revision_number)
        if cluster_security_groups and not isinstance(cluster_security_groups, list):
            raise TypeError("Expected argument 'cluster_security_groups' to be a list")
        pulumi.set(__self__, "cluster_security_groups", cluster_security_groups)
        if cluster_subnet_group_name and not isinstance(cluster_subnet_group_name, str):
            raise TypeError("Expected argument 'cluster_subnet_group_name' to be a str")
        pulumi.set(__self__, "cluster_subnet_group_name", cluster_subnet_group_name)
        if cluster_type and not isinstance(cluster_type, str):
            raise TypeError("Expected argument 'cluster_type' to be a str")
        pulumi.set(__self__, "cluster_type", cluster_type)
        if cluster_version and not isinstance(cluster_version, str):
            raise TypeError("Expected argument 'cluster_version' to be a str")
        pulumi.set(__self__, "cluster_version", cluster_version)
        if database_name and not isinstance(database_name, str):
            raise TypeError("Expected argument 'database_name' to be a str")
        pulumi.set(__self__, "database_name", database_name)
        if elastic_ip and not isinstance(elastic_ip, str):
            raise TypeError("Expected argument 'elastic_ip' to be a str")
        pulumi.set(__self__, "elastic_ip", elastic_ip)
        if enable_logging and not isinstance(enable_logging, bool):
            raise TypeError("Expected argument 'enable_logging' to be a bool")
        pulumi.set(__self__, "enable_logging", enable_logging)
        if encrypted and not isinstance(encrypted, bool):
            raise TypeError("Expected argument 'encrypted' to be a bool")
        pulumi.set(__self__, "encrypted", encrypted)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if enhanced_vpc_routing and not isinstance(enhanced_vpc_routing, bool):
            raise TypeError("Expected argument 'enhanced_vpc_routing' to be a bool")
        pulumi.set(__self__, "enhanced_vpc_routing", enhanced_vpc_routing)
        if iam_roles and not isinstance(iam_roles, list):
            raise TypeError("Expected argument 'iam_roles' to be a list")
        pulumi.set(__self__, "iam_roles", iam_roles)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if master_username and not isinstance(master_username, str):
            raise TypeError("Expected argument 'master_username' to be a str")
        pulumi.set(__self__, "master_username", master_username)
        if node_type and not isinstance(node_type, str):
            raise TypeError("Expected argument 'node_type' to be a str")
        pulumi.set(__self__, "node_type", node_type)
        if number_of_nodes and not isinstance(number_of_nodes, int):
            raise TypeError("Expected argument 'number_of_nodes' to be a int")
        pulumi.set(__self__, "number_of_nodes", number_of_nodes)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if preferred_maintenance_window and not isinstance(preferred_maintenance_window, str):
            raise TypeError("Expected argument 'preferred_maintenance_window' to be a str")
        pulumi.set(__self__, "preferred_maintenance_window", preferred_maintenance_window)
        if publicly_accessible and not isinstance(publicly_accessible, bool):
            raise TypeError("Expected argument 'publicly_accessible' to be a bool")
        pulumi.set(__self__, "publicly_accessible", publicly_accessible)
        if s3_key_prefix and not isinstance(s3_key_prefix, str):
            raise TypeError("Expected argument 's3_key_prefix' to be a str")
        pulumi.set(__self__, "s3_key_prefix", s3_key_prefix)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)
        if vpc_security_group_ids and not isinstance(vpc_security_group_ids, list):
            raise TypeError("Expected argument 'vpc_security_group_ids' to be a list")
        pulumi.set(__self__, "vpc_security_group_ids", vpc_security_group_ids)

    @property
    @pulumi.getter(name="allowVersionUpgrade")
    def allow_version_upgrade(self) -> bool:
        """
        Whether major version upgrades can be applied during maintenance period
        """
        return pulumi.get(self, "allow_version_upgrade")

    @property
    @pulumi.getter(name="automatedSnapshotRetentionPeriod")
    def automated_snapshot_retention_period(self) -> int:
        """
        The backup retention period
        """
        return pulumi.get(self, "automated_snapshot_retention_period")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> str:
        """
        The availability zone of the cluster
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> str:
        """
        The name of the S3 bucket where the log files are to be stored
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """
        The cluster identifier
        """
        return pulumi.get(self, "cluster_identifier")

    @property
    @pulumi.getter(name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> str:
        """
        The name of the parameter group to be associated with this cluster
        """
        return pulumi.get(self, "cluster_parameter_group_name")

    @property
    @pulumi.getter(name="clusterPublicKey")
    def cluster_public_key(self) -> str:
        """
        The public key for the cluster
        """
        return pulumi.get(self, "cluster_public_key")

    @property
    @pulumi.getter(name="clusterRevisionNumber")
    def cluster_revision_number(self) -> str:
        """
        The cluster revision number
        """
        return pulumi.get(self, "cluster_revision_number")

    @property
    @pulumi.getter(name="clusterSecurityGroups")
    def cluster_security_groups(self) -> Sequence[str]:
        """
        The security groups associated with the cluster
        """
        return pulumi.get(self, "cluster_security_groups")

    @property
    @pulumi.getter(name="clusterSubnetGroupName")
    def cluster_subnet_group_name(self) -> str:
        """
        The name of a cluster subnet group to be associated with this cluster
        """
        return pulumi.get(self, "cluster_subnet_group_name")

    @property
    @pulumi.getter(name="clusterType")
    def cluster_type(self) -> str:
        """
        The cluster type
        """
        return pulumi.get(self, "cluster_type")

    @property
    @pulumi.getter(name="clusterVersion")
    def cluster_version(self) -> str:
        return pulumi.get(self, "cluster_version")

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> str:
        """
        The name of the default database in the cluster
        """
        return pulumi.get(self, "database_name")

    @property
    @pulumi.getter(name="elasticIp")
    def elastic_ip(self) -> str:
        """
        The Elastic IP of the cluster
        """
        return pulumi.get(self, "elastic_ip")

    @property
    @pulumi.getter(name="enableLogging")
    def enable_logging(self) -> bool:
        """
        Whether cluster logging is enabled
        """
        return pulumi.get(self, "enable_logging")

    @property
    @pulumi.getter
    def encrypted(self) -> bool:
        """
        Whether the cluster data is encrypted
        """
        return pulumi.get(self, "encrypted")

    @property
    @pulumi.getter
    def endpoint(self) -> str:
        """
        The cluster endpoint
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="enhancedVpcRouting")
    def enhanced_vpc_routing(self) -> bool:
        """
        Whether enhanced VPC routing is enabled
        """
        return pulumi.get(self, "enhanced_vpc_routing")

    @property
    @pulumi.getter(name="iamRoles")
    def iam_roles(self) -> Sequence[str]:
        """
        The IAM roles associated to the cluster
        """
        return pulumi.get(self, "iam_roles")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> str:
        """
        The KMS encryption key associated to the cluster
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="masterUsername")
    def master_username(self) -> str:
        """
        Username for the master DB user
        """
        return pulumi.get(self, "master_username")

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> str:
        """
        The cluster node type
        """
        return pulumi.get(self, "node_type")

    @property
    @pulumi.getter(name="numberOfNodes")
    def number_of_nodes(self) -> int:
        """
        The number of nodes in the cluster
        """
        return pulumi.get(self, "number_of_nodes")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port the cluster responds on
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> str:
        """
        The maintenance window
        """
        return pulumi.get(self, "preferred_maintenance_window")

    @property
    @pulumi.getter(name="publiclyAccessible")
    def publicly_accessible(self) -> bool:
        """
        Whether the cluster is publicly accessible
        """
        return pulumi.get(self, "publicly_accessible")

    @property
    @pulumi.getter(name="s3KeyPrefix")
    def s3_key_prefix(self) -> str:
        """
        The folder inside the S3 bucket where the log files are stored
        """
        return pulumi.get(self, "s3_key_prefix")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags associated to the cluster
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The VPC Id associated with the cluster
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> Sequence[str]:
        """
        The VPC security group Ids associated with the cluster
        """
        return pulumi.get(self, "vpc_security_group_ids")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            allow_version_upgrade=self.allow_version_upgrade,
            automated_snapshot_retention_period=self.automated_snapshot_retention_period,
            availability_zone=self.availability_zone,
            bucket_name=self.bucket_name,
            cluster_identifier=self.cluster_identifier,
            cluster_parameter_group_name=self.cluster_parameter_group_name,
            cluster_public_key=self.cluster_public_key,
            cluster_revision_number=self.cluster_revision_number,
            cluster_security_groups=self.cluster_security_groups,
            cluster_subnet_group_name=self.cluster_subnet_group_name,
            cluster_type=self.cluster_type,
            cluster_version=self.cluster_version,
            database_name=self.database_name,
            elastic_ip=self.elastic_ip,
            enable_logging=self.enable_logging,
            encrypted=self.encrypted,
            endpoint=self.endpoint,
            enhanced_vpc_routing=self.enhanced_vpc_routing,
            iam_roles=self.iam_roles,
            id=self.id,
            kms_key_id=self.kms_key_id,
            master_username=self.master_username,
            node_type=self.node_type,
            number_of_nodes=self.number_of_nodes,
            port=self.port,
            preferred_maintenance_window=self.preferred_maintenance_window,
            publicly_accessible=self.publicly_accessible,
            s3_key_prefix=self.s3_key_prefix,
            tags=self.tags,
            vpc_id=self.vpc_id,
            vpc_security_group_ids=self.vpc_security_group_ids)


def get_cluster(cluster_identifier: Optional[str] = None,
                tags: Optional[Mapping[str, str]] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    Provides details about a specific redshift cluster.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test_cluster = aws.redshift.get_cluster(cluster_identifier="test-cluster")
    test_stream = aws.kinesis.FirehoseDeliveryStream("testStream",
        destination="redshift",
        s3_configuration=aws.kinesis.FirehoseDeliveryStreamS3ConfigurationArgs(
            role_arn=aws_iam_role["firehose_role"]["arn"],
            bucket_arn=aws_s3_bucket["bucket"]["arn"],
            buffer_size=10,
            buffer_interval=400,
            compression_format="GZIP",
        ),
        redshift_configuration=aws.kinesis.FirehoseDeliveryStreamRedshiftConfigurationArgs(
            role_arn=aws_iam_role["firehose_role"]["arn"],
            cluster_jdbcurl=f"jdbc:redshift://{test_cluster.endpoint}/{test_cluster.database_name}",
            username="testuser",
            password="T3stPass",
            data_table_name="test-table",
            copy_options="delimiter '|'",
            data_table_columns="test-col",
        ))
    ```


    :param str cluster_identifier: The cluster identifier
    :param Mapping[str, str] tags: The tags associated to the cluster
    """
    __args__ = dict()
    __args__['clusterIdentifier'] = cluster_identifier
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:redshift/getCluster:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        allow_version_upgrade=__ret__.allow_version_upgrade,
        automated_snapshot_retention_period=__ret__.automated_snapshot_retention_period,
        availability_zone=__ret__.availability_zone,
        bucket_name=__ret__.bucket_name,
        cluster_identifier=__ret__.cluster_identifier,
        cluster_parameter_group_name=__ret__.cluster_parameter_group_name,
        cluster_public_key=__ret__.cluster_public_key,
        cluster_revision_number=__ret__.cluster_revision_number,
        cluster_security_groups=__ret__.cluster_security_groups,
        cluster_subnet_group_name=__ret__.cluster_subnet_group_name,
        cluster_type=__ret__.cluster_type,
        cluster_version=__ret__.cluster_version,
        database_name=__ret__.database_name,
        elastic_ip=__ret__.elastic_ip,
        enable_logging=__ret__.enable_logging,
        encrypted=__ret__.encrypted,
        endpoint=__ret__.endpoint,
        enhanced_vpc_routing=__ret__.enhanced_vpc_routing,
        iam_roles=__ret__.iam_roles,
        id=__ret__.id,
        kms_key_id=__ret__.kms_key_id,
        master_username=__ret__.master_username,
        node_type=__ret__.node_type,
        number_of_nodes=__ret__.number_of_nodes,
        port=__ret__.port,
        preferred_maintenance_window=__ret__.preferred_maintenance_window,
        publicly_accessible=__ret__.publicly_accessible,
        s3_key_prefix=__ret__.s3_key_prefix,
        tags=__ret__.tags,
        vpc_id=__ret__.vpc_id,
        vpc_security_group_ids=__ret__.vpc_security_group_ids)


@_utilities.lift_output_func(get_cluster)
def get_cluster_output(cluster_identifier: Optional[pulumi.Input[str]] = None,
                       tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClusterResult]:
    """
    Provides details about a specific redshift cluster.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test_cluster = aws.redshift.get_cluster(cluster_identifier="test-cluster")
    test_stream = aws.kinesis.FirehoseDeliveryStream("testStream",
        destination="redshift",
        s3_configuration=aws.kinesis.FirehoseDeliveryStreamS3ConfigurationArgs(
            role_arn=aws_iam_role["firehose_role"]["arn"],
            bucket_arn=aws_s3_bucket["bucket"]["arn"],
            buffer_size=10,
            buffer_interval=400,
            compression_format="GZIP",
        ),
        redshift_configuration=aws.kinesis.FirehoseDeliveryStreamRedshiftConfigurationArgs(
            role_arn=aws_iam_role["firehose_role"]["arn"],
            cluster_jdbcurl=f"jdbc:redshift://{test_cluster.endpoint}/{test_cluster.database_name}",
            username="testuser",
            password="T3stPass",
            data_table_name="test-table",
            copy_options="delimiter '|'",
            data_table_columns="test-col",
        ))
    ```


    :param str cluster_identifier: The cluster identifier
    :param Mapping[str, str] tags: The tags associated to the cluster
    """
    ...
