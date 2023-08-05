# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['EmailTemplateArgs', 'EmailTemplate']

@pulumi.input_type
class EmailTemplateArgs:
    def __init__(__self__, *,
                 body: pulumi.Input[str],
                 enabled: pulumi.Input[bool],
                 from_: pulumi.Input[str],
                 subject: pulumi.Input[str],
                 syntax: pulumi.Input[str],
                 template: pulumi.Input[str],
                 result_url: Optional[pulumi.Input[str]] = None,
                 url_lifetime_in_seconds: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a EmailTemplate resource.
        :param pulumi.Input[str] body: String. Body of the email template. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[bool] enabled: Boolean. Indicates whether or not the template is enabled.
        :param pulumi.Input[str] from_: String. Email address to use as the sender. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[str] subject: String. Subject line of the email. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[str] syntax: String. Syntax of the template body. You can use either text or HTML + Liquid syntax.
        :param pulumi.Input[str] template: String. Template name. Options include `verify_email`, `verify_email_by_code`, `reset_email`, `welcome_email`, `blocked_account`, `stolen_credentials`, `enrollment_email`, `mfa_oob_code`, `user_invitation`, `change_password` (legacy), or `password_reset` (legacy).
        :param pulumi.Input[str] result_url: String. URL to redirect the user to after a successful action. [Learn more](https://auth0.com/docs/email/templates#configuring-the-redirect-to-url).
        :param pulumi.Input[int] url_lifetime_in_seconds: Integer. Number of seconds during which the link within the email will be valid.
        """
        pulumi.set(__self__, "body", body)
        pulumi.set(__self__, "enabled", enabled)
        pulumi.set(__self__, "from_", from_)
        pulumi.set(__self__, "subject", subject)
        pulumi.set(__self__, "syntax", syntax)
        pulumi.set(__self__, "template", template)
        if result_url is not None:
            pulumi.set(__self__, "result_url", result_url)
        if url_lifetime_in_seconds is not None:
            pulumi.set(__self__, "url_lifetime_in_seconds", url_lifetime_in_seconds)

    @property
    @pulumi.getter
    def body(self) -> pulumi.Input[str]:
        """
        String. Body of the email template. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "body")

    @body.setter
    def body(self, value: pulumi.Input[str]):
        pulumi.set(self, "body", value)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        """
        Boolean. Indicates whether or not the template is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="from")
    def from_(self) -> pulumi.Input[str]:
        """
        String. Email address to use as the sender. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "from_")

    @from_.setter
    def from_(self, value: pulumi.Input[str]):
        pulumi.set(self, "from_", value)

    @property
    @pulumi.getter
    def subject(self) -> pulumi.Input[str]:
        """
        String. Subject line of the email. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "subject")

    @subject.setter
    def subject(self, value: pulumi.Input[str]):
        pulumi.set(self, "subject", value)

    @property
    @pulumi.getter
    def syntax(self) -> pulumi.Input[str]:
        """
        String. Syntax of the template body. You can use either text or HTML + Liquid syntax.
        """
        return pulumi.get(self, "syntax")

    @syntax.setter
    def syntax(self, value: pulumi.Input[str]):
        pulumi.set(self, "syntax", value)

    @property
    @pulumi.getter
    def template(self) -> pulumi.Input[str]:
        """
        String. Template name. Options include `verify_email`, `verify_email_by_code`, `reset_email`, `welcome_email`, `blocked_account`, `stolen_credentials`, `enrollment_email`, `mfa_oob_code`, `user_invitation`, `change_password` (legacy), or `password_reset` (legacy).
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: pulumi.Input[str]):
        pulumi.set(self, "template", value)

    @property
    @pulumi.getter(name="resultUrl")
    def result_url(self) -> Optional[pulumi.Input[str]]:
        """
        String. URL to redirect the user to after a successful action. [Learn more](https://auth0.com/docs/email/templates#configuring-the-redirect-to-url).
        """
        return pulumi.get(self, "result_url")

    @result_url.setter
    def result_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "result_url", value)

    @property
    @pulumi.getter(name="urlLifetimeInSeconds")
    def url_lifetime_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Integer. Number of seconds during which the link within the email will be valid.
        """
        return pulumi.get(self, "url_lifetime_in_seconds")

    @url_lifetime_in_seconds.setter
    def url_lifetime_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "url_lifetime_in_seconds", value)


@pulumi.input_type
class _EmailTemplateState:
    def __init__(__self__, *,
                 body: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 from_: Optional[pulumi.Input[str]] = None,
                 result_url: Optional[pulumi.Input[str]] = None,
                 subject: Optional[pulumi.Input[str]] = None,
                 syntax: Optional[pulumi.Input[str]] = None,
                 template: Optional[pulumi.Input[str]] = None,
                 url_lifetime_in_seconds: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering EmailTemplate resources.
        :param pulumi.Input[str] body: String. Body of the email template. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[bool] enabled: Boolean. Indicates whether or not the template is enabled.
        :param pulumi.Input[str] from_: String. Email address to use as the sender. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[str] result_url: String. URL to redirect the user to after a successful action. [Learn more](https://auth0.com/docs/email/templates#configuring-the-redirect-to-url).
        :param pulumi.Input[str] subject: String. Subject line of the email. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[str] syntax: String. Syntax of the template body. You can use either text or HTML + Liquid syntax.
        :param pulumi.Input[str] template: String. Template name. Options include `verify_email`, `verify_email_by_code`, `reset_email`, `welcome_email`, `blocked_account`, `stolen_credentials`, `enrollment_email`, `mfa_oob_code`, `user_invitation`, `change_password` (legacy), or `password_reset` (legacy).
        :param pulumi.Input[int] url_lifetime_in_seconds: Integer. Number of seconds during which the link within the email will be valid.
        """
        if body is not None:
            pulumi.set(__self__, "body", body)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if from_ is not None:
            pulumi.set(__self__, "from_", from_)
        if result_url is not None:
            pulumi.set(__self__, "result_url", result_url)
        if subject is not None:
            pulumi.set(__self__, "subject", subject)
        if syntax is not None:
            pulumi.set(__self__, "syntax", syntax)
        if template is not None:
            pulumi.set(__self__, "template", template)
        if url_lifetime_in_seconds is not None:
            pulumi.set(__self__, "url_lifetime_in_seconds", url_lifetime_in_seconds)

    @property
    @pulumi.getter
    def body(self) -> Optional[pulumi.Input[str]]:
        """
        String. Body of the email template. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "body")

    @body.setter
    def body(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "body", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean. Indicates whether or not the template is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="from")
    def from_(self) -> Optional[pulumi.Input[str]]:
        """
        String. Email address to use as the sender. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "from_")

    @from_.setter
    def from_(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "from_", value)

    @property
    @pulumi.getter(name="resultUrl")
    def result_url(self) -> Optional[pulumi.Input[str]]:
        """
        String. URL to redirect the user to after a successful action. [Learn more](https://auth0.com/docs/email/templates#configuring-the-redirect-to-url).
        """
        return pulumi.get(self, "result_url")

    @result_url.setter
    def result_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "result_url", value)

    @property
    @pulumi.getter
    def subject(self) -> Optional[pulumi.Input[str]]:
        """
        String. Subject line of the email. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "subject")

    @subject.setter
    def subject(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subject", value)

    @property
    @pulumi.getter
    def syntax(self) -> Optional[pulumi.Input[str]]:
        """
        String. Syntax of the template body. You can use either text or HTML + Liquid syntax.
        """
        return pulumi.get(self, "syntax")

    @syntax.setter
    def syntax(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "syntax", value)

    @property
    @pulumi.getter
    def template(self) -> Optional[pulumi.Input[str]]:
        """
        String. Template name. Options include `verify_email`, `verify_email_by_code`, `reset_email`, `welcome_email`, `blocked_account`, `stolen_credentials`, `enrollment_email`, `mfa_oob_code`, `user_invitation`, `change_password` (legacy), or `password_reset` (legacy).
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template", value)

    @property
    @pulumi.getter(name="urlLifetimeInSeconds")
    def url_lifetime_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Integer. Number of seconds during which the link within the email will be valid.
        """
        return pulumi.get(self, "url_lifetime_in_seconds")

    @url_lifetime_in_seconds.setter
    def url_lifetime_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "url_lifetime_in_seconds", value)


class EmailTemplate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 body: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 from_: Optional[pulumi.Input[str]] = None,
                 result_url: Optional[pulumi.Input[str]] = None,
                 subject: Optional[pulumi.Input[str]] = None,
                 syntax: Optional[pulumi.Input[str]] = None,
                 template: Optional[pulumi.Input[str]] = None,
                 url_lifetime_in_seconds: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        With Auth0, you can have standard welcome, password reset, and account verification email-based workflows built right into Auth0. This resource allows you to configure email templates to customize the look, feel, and sender identities of emails sent by Auth0. Used in conjunction with configured email providers.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        my_email_provider = auth0.Email("myEmailProvider",
            enabled=True,
            default_from_address="accounts@example.com",
            credentials=auth0.EmailCredentialsArgs(
                access_key_id="AKIAXXXXXXXXXXXXXXXX",
                secret_access_key="7e8c2148xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                region="us-east-1",
            ))
        my_email_template = auth0.EmailTemplate("myEmailTemplate",
            template="welcome_email",
            body="<html><body><h1>Welcome!</h1></body></html>",
            from_="welcome@example.com",
            result_url="https://example.com/welcome",
            subject="Welcome",
            syntax="liquid",
            url_lifetime_in_seconds=3600,
            enabled=True,
            opts=pulumi.ResourceOptions(depends_on=[my_email_provider]))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] body: String. Body of the email template. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[bool] enabled: Boolean. Indicates whether or not the template is enabled.
        :param pulumi.Input[str] from_: String. Email address to use as the sender. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[str] result_url: String. URL to redirect the user to after a successful action. [Learn more](https://auth0.com/docs/email/templates#configuring-the-redirect-to-url).
        :param pulumi.Input[str] subject: String. Subject line of the email. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[str] syntax: String. Syntax of the template body. You can use either text or HTML + Liquid syntax.
        :param pulumi.Input[str] template: String. Template name. Options include `verify_email`, `verify_email_by_code`, `reset_email`, `welcome_email`, `blocked_account`, `stolen_credentials`, `enrollment_email`, `mfa_oob_code`, `user_invitation`, `change_password` (legacy), or `password_reset` (legacy).
        :param pulumi.Input[int] url_lifetime_in_seconds: Integer. Number of seconds during which the link within the email will be valid.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EmailTemplateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        With Auth0, you can have standard welcome, password reset, and account verification email-based workflows built right into Auth0. This resource allows you to configure email templates to customize the look, feel, and sender identities of emails sent by Auth0. Used in conjunction with configured email providers.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        my_email_provider = auth0.Email("myEmailProvider",
            enabled=True,
            default_from_address="accounts@example.com",
            credentials=auth0.EmailCredentialsArgs(
                access_key_id="AKIAXXXXXXXXXXXXXXXX",
                secret_access_key="7e8c2148xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                region="us-east-1",
            ))
        my_email_template = auth0.EmailTemplate("myEmailTemplate",
            template="welcome_email",
            body="<html><body><h1>Welcome!</h1></body></html>",
            from_="welcome@example.com",
            result_url="https://example.com/welcome",
            subject="Welcome",
            syntax="liquid",
            url_lifetime_in_seconds=3600,
            enabled=True,
            opts=pulumi.ResourceOptions(depends_on=[my_email_provider]))
        ```

        :param str resource_name: The name of the resource.
        :param EmailTemplateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EmailTemplateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 body: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 from_: Optional[pulumi.Input[str]] = None,
                 result_url: Optional[pulumi.Input[str]] = None,
                 subject: Optional[pulumi.Input[str]] = None,
                 syntax: Optional[pulumi.Input[str]] = None,
                 template: Optional[pulumi.Input[str]] = None,
                 url_lifetime_in_seconds: Optional[pulumi.Input[int]] = None,
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
            __props__ = EmailTemplateArgs.__new__(EmailTemplateArgs)

            if body is None and not opts.urn:
                raise TypeError("Missing required property 'body'")
            __props__.__dict__["body"] = body
            if enabled is None and not opts.urn:
                raise TypeError("Missing required property 'enabled'")
            __props__.__dict__["enabled"] = enabled
            if from_ is None and not opts.urn:
                raise TypeError("Missing required property 'from_'")
            __props__.__dict__["from_"] = from_
            __props__.__dict__["result_url"] = result_url
            if subject is None and not opts.urn:
                raise TypeError("Missing required property 'subject'")
            __props__.__dict__["subject"] = subject
            if syntax is None and not opts.urn:
                raise TypeError("Missing required property 'syntax'")
            __props__.__dict__["syntax"] = syntax
            if template is None and not opts.urn:
                raise TypeError("Missing required property 'template'")
            __props__.__dict__["template"] = template
            __props__.__dict__["url_lifetime_in_seconds"] = url_lifetime_in_seconds
        super(EmailTemplate, __self__).__init__(
            'auth0:index/emailTemplate:EmailTemplate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            body: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            from_: Optional[pulumi.Input[str]] = None,
            result_url: Optional[pulumi.Input[str]] = None,
            subject: Optional[pulumi.Input[str]] = None,
            syntax: Optional[pulumi.Input[str]] = None,
            template: Optional[pulumi.Input[str]] = None,
            url_lifetime_in_seconds: Optional[pulumi.Input[int]] = None) -> 'EmailTemplate':
        """
        Get an existing EmailTemplate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] body: String. Body of the email template. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[bool] enabled: Boolean. Indicates whether or not the template is enabled.
        :param pulumi.Input[str] from_: String. Email address to use as the sender. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[str] result_url: String. URL to redirect the user to after a successful action. [Learn more](https://auth0.com/docs/email/templates#configuring-the-redirect-to-url).
        :param pulumi.Input[str] subject: String. Subject line of the email. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        :param pulumi.Input[str] syntax: String. Syntax of the template body. You can use either text or HTML + Liquid syntax.
        :param pulumi.Input[str] template: String. Template name. Options include `verify_email`, `verify_email_by_code`, `reset_email`, `welcome_email`, `blocked_account`, `stolen_credentials`, `enrollment_email`, `mfa_oob_code`, `user_invitation`, `change_password` (legacy), or `password_reset` (legacy).
        :param pulumi.Input[int] url_lifetime_in_seconds: Integer. Number of seconds during which the link within the email will be valid.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EmailTemplateState.__new__(_EmailTemplateState)

        __props__.__dict__["body"] = body
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["from_"] = from_
        __props__.__dict__["result_url"] = result_url
        __props__.__dict__["subject"] = subject
        __props__.__dict__["syntax"] = syntax
        __props__.__dict__["template"] = template
        __props__.__dict__["url_lifetime_in_seconds"] = url_lifetime_in_seconds
        return EmailTemplate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def body(self) -> pulumi.Output[str]:
        """
        String. Body of the email template. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "body")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        """
        Boolean. Indicates whether or not the template is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="from")
    def from_(self) -> pulumi.Output[str]:
        """
        String. Email address to use as the sender. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "from_")

    @property
    @pulumi.getter(name="resultUrl")
    def result_url(self) -> pulumi.Output[Optional[str]]:
        """
        String. URL to redirect the user to after a successful action. [Learn more](https://auth0.com/docs/email/templates#configuring-the-redirect-to-url).
        """
        return pulumi.get(self, "result_url")

    @property
    @pulumi.getter
    def subject(self) -> pulumi.Output[str]:
        """
        String. Subject line of the email. You can include [common variables](https://auth0.com/docs/email/templates#common-variables).
        """
        return pulumi.get(self, "subject")

    @property
    @pulumi.getter
    def syntax(self) -> pulumi.Output[str]:
        """
        String. Syntax of the template body. You can use either text or HTML + Liquid syntax.
        """
        return pulumi.get(self, "syntax")

    @property
    @pulumi.getter
    def template(self) -> pulumi.Output[str]:
        """
        String. Template name. Options include `verify_email`, `verify_email_by_code`, `reset_email`, `welcome_email`, `blocked_account`, `stolen_credentials`, `enrollment_email`, `mfa_oob_code`, `user_invitation`, `change_password` (legacy), or `password_reset` (legacy).
        """
        return pulumi.get(self, "template")

    @property
    @pulumi.getter(name="urlLifetimeInSeconds")
    def url_lifetime_in_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        Integer. Number of seconds during which the link within the email will be valid.
        """
        return pulumi.get(self, "url_lifetime_in_seconds")

