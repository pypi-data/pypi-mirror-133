# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ApiCorsConfigurationArgs',
    'AuthorizerJwtConfigurationArgs',
    'DomainNameDomainNameConfigurationArgs',
    'DomainNameMutualTlsAuthenticationArgs',
    'IntegrationResponseParameterArgs',
    'IntegrationTlsConfigArgs',
    'RouteRequestParameterArgs',
    'StageAccessLogSettingsArgs',
    'StageDefaultRouteSettingsArgs',
    'StageRouteSettingArgs',
]

@pulumi.input_type
class ApiCorsConfigurationArgs:
    def __init__(__self__, *,
                 allow_credentials: Optional[pulumi.Input[bool]] = None,
                 allow_headers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 allow_methods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 allow_origins: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 expose_headers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 max_age: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[bool] allow_credentials: Whether credentials are included in the CORS request.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allow_headers: The set of allowed HTTP headers.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allow_methods: The set of allowed HTTP methods.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allow_origins: The set of allowed origins.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] expose_headers: The set of exposed HTTP headers.
        :param pulumi.Input[int] max_age: The number of seconds that the browser should cache preflight request results.
        """
        if allow_credentials is not None:
            pulumi.set(__self__, "allow_credentials", allow_credentials)
        if allow_headers is not None:
            pulumi.set(__self__, "allow_headers", allow_headers)
        if allow_methods is not None:
            pulumi.set(__self__, "allow_methods", allow_methods)
        if allow_origins is not None:
            pulumi.set(__self__, "allow_origins", allow_origins)
        if expose_headers is not None:
            pulumi.set(__self__, "expose_headers", expose_headers)
        if max_age is not None:
            pulumi.set(__self__, "max_age", max_age)

    @property
    @pulumi.getter(name="allowCredentials")
    def allow_credentials(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether credentials are included in the CORS request.
        """
        return pulumi.get(self, "allow_credentials")

    @allow_credentials.setter
    def allow_credentials(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_credentials", value)

    @property
    @pulumi.getter(name="allowHeaders")
    def allow_headers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The set of allowed HTTP headers.
        """
        return pulumi.get(self, "allow_headers")

    @allow_headers.setter
    def allow_headers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allow_headers", value)

    @property
    @pulumi.getter(name="allowMethods")
    def allow_methods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The set of allowed HTTP methods.
        """
        return pulumi.get(self, "allow_methods")

    @allow_methods.setter
    def allow_methods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allow_methods", value)

    @property
    @pulumi.getter(name="allowOrigins")
    def allow_origins(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The set of allowed origins.
        """
        return pulumi.get(self, "allow_origins")

    @allow_origins.setter
    def allow_origins(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allow_origins", value)

    @property
    @pulumi.getter(name="exposeHeaders")
    def expose_headers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The set of exposed HTTP headers.
        """
        return pulumi.get(self, "expose_headers")

    @expose_headers.setter
    def expose_headers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "expose_headers", value)

    @property
    @pulumi.getter(name="maxAge")
    def max_age(self) -> Optional[pulumi.Input[int]]:
        """
        The number of seconds that the browser should cache preflight request results.
        """
        return pulumi.get(self, "max_age")

    @max_age.setter
    def max_age(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_age", value)


@pulumi.input_type
class AuthorizerJwtConfigurationArgs:
    def __init__(__self__, *,
                 audiences: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 issuer: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] audiences: A list of the intended recipients of the JWT. A valid JWT must provide an aud that matches at least one entry in this list.
        :param pulumi.Input[str] issuer: The base domain of the identity provider that issues JSON Web Tokens, such as the `endpoint` attribute of the `cognito.UserPool` resource.
        """
        if audiences is not None:
            pulumi.set(__self__, "audiences", audiences)
        if issuer is not None:
            pulumi.set(__self__, "issuer", issuer)

    @property
    @pulumi.getter
    def audiences(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of the intended recipients of the JWT. A valid JWT must provide an aud that matches at least one entry in this list.
        """
        return pulumi.get(self, "audiences")

    @audiences.setter
    def audiences(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "audiences", value)

    @property
    @pulumi.getter
    def issuer(self) -> Optional[pulumi.Input[str]]:
        """
        The base domain of the identity provider that issues JSON Web Tokens, such as the `endpoint` attribute of the `cognito.UserPool` resource.
        """
        return pulumi.get(self, "issuer")

    @issuer.setter
    def issuer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer", value)


@pulumi.input_type
class DomainNameDomainNameConfigurationArgs:
    def __init__(__self__, *,
                 certificate_arn: pulumi.Input[str],
                 endpoint_type: pulumi.Input[str],
                 security_policy: pulumi.Input[str],
                 hosted_zone_id: Optional[pulumi.Input[str]] = None,
                 target_domain_name: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] certificate_arn: The ARN of an AWS-managed certificate that will be used by the endpoint for the domain name. AWS Certificate Manager is the only supported source.
               Use the `acm.Certificate` resource to configure an ACM certificate.
        :param pulumi.Input[str] endpoint_type: The endpoint type. Valid values: `REGIONAL`.
        :param pulumi.Input[str] security_policy: The Transport Layer Security (TLS) version of the [security policy](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-custom-domain-tls-version.html) for the domain name. Valid values: `TLS_1_2`.
        :param pulumi.Input[str] hosted_zone_id: The Amazon Route 53 Hosted Zone ID of the endpoint.
        :param pulumi.Input[str] target_domain_name: The target domain name.
        """
        pulumi.set(__self__, "certificate_arn", certificate_arn)
        pulumi.set(__self__, "endpoint_type", endpoint_type)
        pulumi.set(__self__, "security_policy", security_policy)
        if hosted_zone_id is not None:
            pulumi.set(__self__, "hosted_zone_id", hosted_zone_id)
        if target_domain_name is not None:
            pulumi.set(__self__, "target_domain_name", target_domain_name)

    @property
    @pulumi.getter(name="certificateArn")
    def certificate_arn(self) -> pulumi.Input[str]:
        """
        The ARN of an AWS-managed certificate that will be used by the endpoint for the domain name. AWS Certificate Manager is the only supported source.
        Use the `acm.Certificate` resource to configure an ACM certificate.
        """
        return pulumi.get(self, "certificate_arn")

    @certificate_arn.setter
    def certificate_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_arn", value)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> pulumi.Input[str]:
        """
        The endpoint type. Valid values: `REGIONAL`.
        """
        return pulumi.get(self, "endpoint_type")

    @endpoint_type.setter
    def endpoint_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_type", value)

    @property
    @pulumi.getter(name="securityPolicy")
    def security_policy(self) -> pulumi.Input[str]:
        """
        The Transport Layer Security (TLS) version of the [security policy](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-custom-domain-tls-version.html) for the domain name. Valid values: `TLS_1_2`.
        """
        return pulumi.get(self, "security_policy")

    @security_policy.setter
    def security_policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "security_policy", value)

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Route 53 Hosted Zone ID of the endpoint.
        """
        return pulumi.get(self, "hosted_zone_id")

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hosted_zone_id", value)

    @property
    @pulumi.getter(name="targetDomainName")
    def target_domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The target domain name.
        """
        return pulumi.get(self, "target_domain_name")

    @target_domain_name.setter
    def target_domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_domain_name", value)


@pulumi.input_type
class DomainNameMutualTlsAuthenticationArgs:
    def __init__(__self__, *,
                 truststore_uri: pulumi.Input[str],
                 truststore_version: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] truststore_uri: An Amazon S3 URL that specifies the truststore for mutual TLS authentication, for example, `s3://bucket-name/key-name`.
               The truststore can contain certificates from public or private certificate authorities. To update the truststore, upload a new version to S3, and then update your custom domain name to use the new version.
        :param pulumi.Input[str] truststore_version: The version of the S3 object that contains the truststore. To specify a version, you must have versioning enabled for the S3 bucket.
        """
        pulumi.set(__self__, "truststore_uri", truststore_uri)
        if truststore_version is not None:
            pulumi.set(__self__, "truststore_version", truststore_version)

    @property
    @pulumi.getter(name="truststoreUri")
    def truststore_uri(self) -> pulumi.Input[str]:
        """
        An Amazon S3 URL that specifies the truststore for mutual TLS authentication, for example, `s3://bucket-name/key-name`.
        The truststore can contain certificates from public or private certificate authorities. To update the truststore, upload a new version to S3, and then update your custom domain name to use the new version.
        """
        return pulumi.get(self, "truststore_uri")

    @truststore_uri.setter
    def truststore_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "truststore_uri", value)

    @property
    @pulumi.getter(name="truststoreVersion")
    def truststore_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the S3 object that contains the truststore. To specify a version, you must have versioning enabled for the S3 bucket.
        """
        return pulumi.get(self, "truststore_version")

    @truststore_version.setter
    def truststore_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "truststore_version", value)


@pulumi.input_type
class IntegrationResponseParameterArgs:
    def __init__(__self__, *,
                 mappings: pulumi.Input[Mapping[str, pulumi.Input[str]]],
                 status_code: pulumi.Input[str]):
        """
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] mappings: A key-value map. The key of ths map identifies the location of the request parameter to change, and how to change it. The corresponding value specifies the new data for the parameter.
               See the [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html) for details.
        :param pulumi.Input[str] status_code: The HTTP status code in the range 200-599.
        """
        pulumi.set(__self__, "mappings", mappings)
        pulumi.set(__self__, "status_code", status_code)

    @property
    @pulumi.getter
    def mappings(self) -> pulumi.Input[Mapping[str, pulumi.Input[str]]]:
        """
        A key-value map. The key of ths map identifies the location of the request parameter to change, and how to change it. The corresponding value specifies the new data for the parameter.
        See the [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html) for details.
        """
        return pulumi.get(self, "mappings")

    @mappings.setter
    def mappings(self, value: pulumi.Input[Mapping[str, pulumi.Input[str]]]):
        pulumi.set(self, "mappings", value)

    @property
    @pulumi.getter(name="statusCode")
    def status_code(self) -> pulumi.Input[str]:
        """
        The HTTP status code in the range 200-599.
        """
        return pulumi.get(self, "status_code")

    @status_code.setter
    def status_code(self, value: pulumi.Input[str]):
        pulumi.set(self, "status_code", value)


@pulumi.input_type
class IntegrationTlsConfigArgs:
    def __init__(__self__, *,
                 server_name_to_verify: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] server_name_to_verify: If you specify a server name, API Gateway uses it to verify the hostname on the integration's certificate. The server name is also included in the TLS handshake to support Server Name Indication (SNI) or virtual hosting.
        """
        if server_name_to_verify is not None:
            pulumi.set(__self__, "server_name_to_verify", server_name_to_verify)

    @property
    @pulumi.getter(name="serverNameToVerify")
    def server_name_to_verify(self) -> Optional[pulumi.Input[str]]:
        """
        If you specify a server name, API Gateway uses it to verify the hostname on the integration's certificate. The server name is also included in the TLS handshake to support Server Name Indication (SNI) or virtual hosting.
        """
        return pulumi.get(self, "server_name_to_verify")

    @server_name_to_verify.setter
    def server_name_to_verify(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_name_to_verify", value)


@pulumi.input_type
class RouteRequestParameterArgs:
    def __init__(__self__, *,
                 request_parameter_key: pulumi.Input[str],
                 required: pulumi.Input[bool]):
        """
        :param pulumi.Input[str] request_parameter_key: Request parameter key. This is a [request data mapping parameter](https://docs.aws.amazon.com/apigateway/latest/developerguide/websocket-api-data-mapping.html#websocket-mapping-request-parameters).
        :param pulumi.Input[bool] required: Boolean whether or not the parameter is required.
        """
        pulumi.set(__self__, "request_parameter_key", request_parameter_key)
        pulumi.set(__self__, "required", required)

    @property
    @pulumi.getter(name="requestParameterKey")
    def request_parameter_key(self) -> pulumi.Input[str]:
        """
        Request parameter key. This is a [request data mapping parameter](https://docs.aws.amazon.com/apigateway/latest/developerguide/websocket-api-data-mapping.html#websocket-mapping-request-parameters).
        """
        return pulumi.get(self, "request_parameter_key")

    @request_parameter_key.setter
    def request_parameter_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "request_parameter_key", value)

    @property
    @pulumi.getter
    def required(self) -> pulumi.Input[bool]:
        """
        Boolean whether or not the parameter is required.
        """
        return pulumi.get(self, "required")

    @required.setter
    def required(self, value: pulumi.Input[bool]):
        pulumi.set(self, "required", value)


@pulumi.input_type
class StageAccessLogSettingsArgs:
    def __init__(__self__, *,
                 destination_arn: pulumi.Input[str],
                 format: pulumi.Input[str]):
        """
        :param pulumi.Input[str] destination_arn: The ARN of the CloudWatch Logs log group to receive access logs. Any trailing `:*` is trimmed from the ARN.
        :param pulumi.Input[str] format: A single line [format](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html#apigateway-cloudwatch-log-formats) of the access logs of data, as specified by [selected $context variables](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-logging.html).
        """
        pulumi.set(__self__, "destination_arn", destination_arn)
        pulumi.set(__self__, "format", format)

    @property
    @pulumi.getter(name="destinationArn")
    def destination_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the CloudWatch Logs log group to receive access logs. Any trailing `:*` is trimmed from the ARN.
        """
        return pulumi.get(self, "destination_arn")

    @destination_arn.setter
    def destination_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_arn", value)

    @property
    @pulumi.getter
    def format(self) -> pulumi.Input[str]:
        """
        A single line [format](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html#apigateway-cloudwatch-log-formats) of the access logs of data, as specified by [selected $context variables](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-logging.html).
        """
        return pulumi.get(self, "format")

    @format.setter
    def format(self, value: pulumi.Input[str]):
        pulumi.set(self, "format", value)


@pulumi.input_type
class StageDefaultRouteSettingsArgs:
    def __init__(__self__, *,
                 data_trace_enabled: Optional[pulumi.Input[bool]] = None,
                 detailed_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 logging_level: Optional[pulumi.Input[str]] = None,
                 throttling_burst_limit: Optional[pulumi.Input[int]] = None,
                 throttling_rate_limit: Optional[pulumi.Input[float]] = None):
        """
        :param pulumi.Input[bool] data_trace_enabled: Whether data trace logging is enabled for the default route. Affects the log entries pushed to Amazon CloudWatch Logs.
               Defaults to `false`. Supported only for WebSocket APIs.
        :param pulumi.Input[bool] detailed_metrics_enabled: Whether detailed metrics are enabled for the default route. Defaults to `false`.
        :param pulumi.Input[str] logging_level: The logging level for the default route. Affects the log entries pushed to Amazon CloudWatch Logs.
               Valid values: `ERROR`, `INFO`, `OFF`. Defaults to `OFF`. Supported only for WebSocket APIs. This provider will only perform drift detection of its value when present in a configuration.
        :param pulumi.Input[int] throttling_burst_limit: The throttling burst limit for the default route.
        :param pulumi.Input[float] throttling_rate_limit: The throttling rate limit for the default route.
        """
        if data_trace_enabled is not None:
            pulumi.set(__self__, "data_trace_enabled", data_trace_enabled)
        if detailed_metrics_enabled is not None:
            pulumi.set(__self__, "detailed_metrics_enabled", detailed_metrics_enabled)
        if logging_level is not None:
            pulumi.set(__self__, "logging_level", logging_level)
        if throttling_burst_limit is not None:
            pulumi.set(__self__, "throttling_burst_limit", throttling_burst_limit)
        if throttling_rate_limit is not None:
            pulumi.set(__self__, "throttling_rate_limit", throttling_rate_limit)

    @property
    @pulumi.getter(name="dataTraceEnabled")
    def data_trace_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether data trace logging is enabled for the default route. Affects the log entries pushed to Amazon CloudWatch Logs.
        Defaults to `false`. Supported only for WebSocket APIs.
        """
        return pulumi.get(self, "data_trace_enabled")

    @data_trace_enabled.setter
    def data_trace_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "data_trace_enabled", value)

    @property
    @pulumi.getter(name="detailedMetricsEnabled")
    def detailed_metrics_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether detailed metrics are enabled for the default route. Defaults to `false`.
        """
        return pulumi.get(self, "detailed_metrics_enabled")

    @detailed_metrics_enabled.setter
    def detailed_metrics_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "detailed_metrics_enabled", value)

    @property
    @pulumi.getter(name="loggingLevel")
    def logging_level(self) -> Optional[pulumi.Input[str]]:
        """
        The logging level for the default route. Affects the log entries pushed to Amazon CloudWatch Logs.
        Valid values: `ERROR`, `INFO`, `OFF`. Defaults to `OFF`. Supported only for WebSocket APIs. This provider will only perform drift detection of its value when present in a configuration.
        """
        return pulumi.get(self, "logging_level")

    @logging_level.setter
    def logging_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "logging_level", value)

    @property
    @pulumi.getter(name="throttlingBurstLimit")
    def throttling_burst_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The throttling burst limit for the default route.
        """
        return pulumi.get(self, "throttling_burst_limit")

    @throttling_burst_limit.setter
    def throttling_burst_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throttling_burst_limit", value)

    @property
    @pulumi.getter(name="throttlingRateLimit")
    def throttling_rate_limit(self) -> Optional[pulumi.Input[float]]:
        """
        The throttling rate limit for the default route.
        """
        return pulumi.get(self, "throttling_rate_limit")

    @throttling_rate_limit.setter
    def throttling_rate_limit(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "throttling_rate_limit", value)


@pulumi.input_type
class StageRouteSettingArgs:
    def __init__(__self__, *,
                 route_key: pulumi.Input[str],
                 data_trace_enabled: Optional[pulumi.Input[bool]] = None,
                 detailed_metrics_enabled: Optional[pulumi.Input[bool]] = None,
                 logging_level: Optional[pulumi.Input[str]] = None,
                 throttling_burst_limit: Optional[pulumi.Input[int]] = None,
                 throttling_rate_limit: Optional[pulumi.Input[float]] = None):
        """
        :param pulumi.Input[str] route_key: Route key.
        :param pulumi.Input[bool] data_trace_enabled: Whether data trace logging is enabled for the route. Affects the log entries pushed to Amazon CloudWatch Logs.
               Defaults to `false`. Supported only for WebSocket APIs.
        :param pulumi.Input[bool] detailed_metrics_enabled: Whether detailed metrics are enabled for the route. Defaults to `false`.
        :param pulumi.Input[str] logging_level: The logging level for the route. Affects the log entries pushed to Amazon CloudWatch Logs.
               Valid values: `ERROR`, `INFO`, `OFF`. Defaults to `OFF`. Supported only for WebSocket APIs. This provider will only perform drift detection of its value when present in a configuration.
        :param pulumi.Input[int] throttling_burst_limit: The throttling burst limit for the route.
        :param pulumi.Input[float] throttling_rate_limit: The throttling rate limit for the route.
        """
        pulumi.set(__self__, "route_key", route_key)
        if data_trace_enabled is not None:
            pulumi.set(__self__, "data_trace_enabled", data_trace_enabled)
        if detailed_metrics_enabled is not None:
            pulumi.set(__self__, "detailed_metrics_enabled", detailed_metrics_enabled)
        if logging_level is not None:
            pulumi.set(__self__, "logging_level", logging_level)
        if throttling_burst_limit is not None:
            pulumi.set(__self__, "throttling_burst_limit", throttling_burst_limit)
        if throttling_rate_limit is not None:
            pulumi.set(__self__, "throttling_rate_limit", throttling_rate_limit)

    @property
    @pulumi.getter(name="routeKey")
    def route_key(self) -> pulumi.Input[str]:
        """
        Route key.
        """
        return pulumi.get(self, "route_key")

    @route_key.setter
    def route_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "route_key", value)

    @property
    @pulumi.getter(name="dataTraceEnabled")
    def data_trace_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether data trace logging is enabled for the route. Affects the log entries pushed to Amazon CloudWatch Logs.
        Defaults to `false`. Supported only for WebSocket APIs.
        """
        return pulumi.get(self, "data_trace_enabled")

    @data_trace_enabled.setter
    def data_trace_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "data_trace_enabled", value)

    @property
    @pulumi.getter(name="detailedMetricsEnabled")
    def detailed_metrics_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether detailed metrics are enabled for the route. Defaults to `false`.
        """
        return pulumi.get(self, "detailed_metrics_enabled")

    @detailed_metrics_enabled.setter
    def detailed_metrics_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "detailed_metrics_enabled", value)

    @property
    @pulumi.getter(name="loggingLevel")
    def logging_level(self) -> Optional[pulumi.Input[str]]:
        """
        The logging level for the route. Affects the log entries pushed to Amazon CloudWatch Logs.
        Valid values: `ERROR`, `INFO`, `OFF`. Defaults to `OFF`. Supported only for WebSocket APIs. This provider will only perform drift detection of its value when present in a configuration.
        """
        return pulumi.get(self, "logging_level")

    @logging_level.setter
    def logging_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "logging_level", value)

    @property
    @pulumi.getter(name="throttlingBurstLimit")
    def throttling_burst_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The throttling burst limit for the route.
        """
        return pulumi.get(self, "throttling_burst_limit")

    @throttling_burst_limit.setter
    def throttling_burst_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throttling_burst_limit", value)

    @property
    @pulumi.getter(name="throttlingRateLimit")
    def throttling_rate_limit(self) -> Optional[pulumi.Input[float]]:
        """
        The throttling rate limit for the route.
        """
        return pulumi.get(self, "throttling_rate_limit")

    @throttling_rate_limit.setter
    def throttling_rate_limit(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "throttling_rate_limit", value)


