'''
# cdk-library-aws-organization

This CDK library is a WIP and not ready for production use.

## Key challenges with Organizations

* Accounts aren't like AWS resources and the [removal process isn't a simple delete](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_remove.html). Therefore the constructs contained in this library do **not** have the goal to delete accounts.
* CloudFormation doesn't support Organizations directly so the constructs in this library use CloudFormation custom resources that utilize Python and [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html)

## Testing the custom provider code with SAM CLI

* Create a test project that utilizes this library
* Create a test stack
* Synthesize the test stack with `cdk synth --no-staging > template.yml`
* Get the function name from the template
* Run `sam local start-lambda -t template.yml`
* Run the `handler_tests` python files with `pytest` like follows:

```
LAMBDA_FUNCTION_NAME='<name you noted earlier>' pytest ./handler_tests/<handler>/test.py -rA --capture=sys
```

* The `test.py` also looks up the root org id to run tests so you'll need to have AWS creds set up to accomodate that behavior.
* You can run the provided tests against the real lambda function by getting the deployed function name from AWS and setting the `RUN_LOCALLY` env variable

```
RUN_LOCALLY='false' LAMBDA_FUNCTION_NAME='<name from AWS>' pytest ./handler_tests/<handler>/test.py -rA --capture=sys
```

## Why can't I move an OU?

Moving OUs isn't supported by Organizations and would cause significant issues with keeping track of OUs in the CDK. Imagine a scenario like below:

* You have an ou, `OUAdmin`, and it has 2 children, `OUChild1 and Account1`, that are also managed by the CDK stack.
* You change the parent of `OUAdmin` to `OUFoo`. The CDK would need to take the following actions:

  * Create a new `OU` under `OUFoo` with the name `OUAdmin`
  * Move all of the original `OUAdmin` OU's children to the new `OUAdmin`
  * Delete the old `OUAdmin`
  * Update all physical resource IDs

    * It would succeed at moving accounts because physical IDs should not change. Accounting moving between OUs is supported by Organizations
    * It would fail at moving any child OUs because they would also be recreated. Resulting in a change to physical resource ID. Because the custom resource can only managed the resource it's currently acting on, `OUAdmin`, any children OUs would be "lost" in this process and ugly to try and manage.

The best way to move OUs would be to add additional OUs to your org then move any accounts as needed then proceed to delete the OUs, like so:

* Add new OU resources
* Deploy the stack
* Change account parents
* Deploy the stack
* Remove old OU resources
* Deploy the stack
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk
import aws_cdk.aws_iam
import aws_cdk.custom_resources
import constructs


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-organization.AccountProps",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "name": "name"},
)
class AccountProps:
    def __init__(self, *, email: builtins.str, name: builtins.str) -> None:
        '''The properties of an Account.

        :param email: The email address of the account. Most be unique.
        :param name: The name of the account.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "email": email,
            "name": name,
        }

    @builtins.property
    def email(self) -> builtins.str:
        '''The email address of the account.

        Most be unique.
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the account.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-organization.OUProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_recreate_on_update": "allowRecreateOnUpdate",
        "import_on_duplicate": "importOnDuplicate",
    },
)
class OUProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_recreate_on_update: typing.Optional[builtins.bool] = None,
        import_on_duplicate: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''The properties of an OU.

        :param name: The name of the OU.
        :param allow_recreate_on_update: Whether or not a missing OU should be recreated during an update. If this is false and the OU does not exist an error will be thrown when you try to update it.
        :param import_on_duplicate: Whether or not to import an existing OU if the new OU is a duplicate. If this is false and the OU already exists an error will be thrown. Default: false
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if allow_recreate_on_update is not None:
            self._values["allow_recreate_on_update"] = allow_recreate_on_update
        if import_on_duplicate is not None:
            self._values["import_on_duplicate"] = import_on_duplicate

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the OU.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_recreate_on_update(self) -> typing.Optional[builtins.bool]:
        '''Whether or not a missing OU should be recreated during an update.

        If this is false and the OU does not exist an error will be thrown when you try to update it.
        '''
        result = self._values.get("allow_recreate_on_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def import_on_duplicate(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to import an existing OU if the new OU is a duplicate.

        If this is false and the OU already exists an error will be thrown.

        :default: false
        '''
        result = self._values.get("import_on_duplicate")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OUProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-organization.OUResourceProps",
    jsii_struct_bases=[OUProps],
    name_mapping={
        "name": "name",
        "allow_recreate_on_update": "allowRecreateOnUpdate",
        "import_on_duplicate": "importOnDuplicate",
        "parent": "parent",
        "provider": "provider",
    },
)
class OUResourceProps(OUProps):
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_recreate_on_update: typing.Optional[builtins.bool] = None,
        import_on_duplicate: typing.Optional[builtins.bool] = None,
        parent: typing.Union[builtins.str, "OrganizationOU"],
        provider: aws_cdk.custom_resources.Provider,
    ) -> None:
        '''The properties of an OrganizationOU custom resource.

        :param name: The name of the OU.
        :param allow_recreate_on_update: Whether or not a missing OU should be recreated during an update. If this is false and the OU does not exist an error will be thrown when you try to update it.
        :param import_on_duplicate: Whether or not to import an existing OU if the new OU is a duplicate. If this is false and the OU already exists an error will be thrown. Default: false
        :param parent: The parent OU id.
        :param provider: The provider to use for the custom resource that will create the OU. You can create a provider with the OrganizationOuProvider class
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "parent": parent,
            "provider": provider,
        }
        if allow_recreate_on_update is not None:
            self._values["allow_recreate_on_update"] = allow_recreate_on_update
        if import_on_duplicate is not None:
            self._values["import_on_duplicate"] = import_on_duplicate

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the OU.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_recreate_on_update(self) -> typing.Optional[builtins.bool]:
        '''Whether or not a missing OU should be recreated during an update.

        If this is false and the OU does not exist an error will be thrown when you try to update it.
        '''
        result = self._values.get("allow_recreate_on_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def import_on_duplicate(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to import an existing OU if the new OU is a duplicate.

        If this is false and the OU already exists an error will be thrown.

        :default: false
        '''
        result = self._values.get("import_on_duplicate")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parent(self) -> typing.Union[builtins.str, "OrganizationOU"]:
        '''The parent OU id.'''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(typing.Union[builtins.str, "OrganizationOU"], result)

    @builtins.property
    def provider(self) -> aws_cdk.custom_resources.Provider:
        '''The provider to use for the custom resource that will create the OU.

        You can create a provider with the OrganizationOuProvider class
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(aws_cdk.custom_resources.Provider, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OUResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrgObject",
    jsii_struct_bases=[],
    name_mapping={
        "children": "children",
        "properties": "properties",
        "type": "type",
        "id": "id",
    },
)
class OrgObject:
    def __init__(
        self,
        *,
        children: typing.Sequence["OrgObject"],
        properties: typing.Union[OUProps, AccountProps],
        type: "OrgObjectTypes",
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The structure of an OrgObject.

        :param children: Other org objects that are children of this org object.
        :param properties: The org object properties.
        :param type: The type of the org object.
        :param id: The unique id of the OrgObject. This is used as the unique identifier when instantiating a construct object. This is important for the CDK to be able to maintain a reference for the object when utilizing the processOrgObj function rather then using the name property of an object which could change. If the id changes the CDK treats this as a new construct and will create a new construct resource and destroy the old one. Not strictly required but useful when using the processOrgObj function. If the id is not provided the name property will be used as the id in processOrgObj. You can create a unique id however you like. A bash example is provided.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "children": children,
            "properties": properties,
            "type": type,
        }
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def children(self) -> typing.List["OrgObject"]:
        '''Other org objects that are children of this org object.'''
        result = self._values.get("children")
        assert result is not None, "Required property 'children' is missing"
        return typing.cast(typing.List["OrgObject"], result)

    @builtins.property
    def properties(self) -> typing.Union[OUProps, AccountProps]:
        '''The org object properties.'''
        result = self._values.get("properties")
        assert result is not None, "Required property 'properties' is missing"
        return typing.cast(typing.Union[OUProps, AccountProps], result)

    @builtins.property
    def type(self) -> "OrgObjectTypes":
        '''The type of the org object.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("OrgObjectTypes", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The unique id of the OrgObject.

        This is used as the unique identifier when instantiating a construct object.
        This is important for the CDK to be able to maintain a reference for the object when utilizing
        the processOrgObj function rather then using the name property of an object which could change.
        If the id changes the CDK treats this as a new construct and will create a new construct resource and
        destroy the old one.

        Not strictly required but useful when using the processOrgObj function. If the id is not provided
        the name property will be used as the id in processOrgObj.

        You can create a unique id however you like. A bash example is provided.

        Example::

            # Example automatically generated from non-compiling source. May contain errors.
            echo "ou-$( echo $RANDOM | md5sum | head -c 8 )"
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@renovosolutions/cdk-library-aws-organization.OrgObjectTypes")
class OrgObjectTypes(enum.Enum):
    '''The supported OrgObject types.'''

    OU = "OU"
    ACCOUNT = "ACCOUNT"


class OrganizationOU(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrganizationOU",
):
    '''The construct to create or update an Organization OU.

    This relies on the custom resource provider OrganizationOUProvider.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        parent: typing.Union[builtins.str, "OrganizationOU"],
        provider: aws_cdk.custom_resources.Provider,
        name: builtins.str,
        allow_recreate_on_update: typing.Optional[builtins.bool] = None,
        import_on_duplicate: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param parent: The parent OU id.
        :param provider: The provider to use for the custom resource that will create the OU. You can create a provider with the OrganizationOuProvider class
        :param name: The name of the OU.
        :param allow_recreate_on_update: Whether or not a missing OU should be recreated during an update. If this is false and the OU does not exist an error will be thrown when you try to update it.
        :param import_on_duplicate: Whether or not to import an existing OU if the new OU is a duplicate. If this is false and the OU already exists an error will be thrown. Default: false
        '''
        props = OUResourceProps(
            parent=parent,
            provider=provider,
            name=name,
            allow_recreate_on_update=allow_recreate_on_update,
            import_on_duplicate=import_on_duplicate,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.CustomResource:
        return typing.cast(aws_cdk.CustomResource, jsii.get(self, "resource"))


class OrganizationOUProvider(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrganizationOUProvider",
):
    '''The provider for OU custom resources.

    This creates a lambda function that handles custom resource requests for creating/updating/deleting OUs.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param role: The role the custom resource should use for taking actions on OUs if one is not provided one will be created automatically.
        '''
        props = OrganizationOUProviderProps(role=role)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="provider")
    def provider(self) -> aws_cdk.custom_resources.Provider:
        return typing.cast(aws_cdk.custom_resources.Provider, jsii.get(self, "provider"))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrganizationOUProviderProps",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class OrganizationOUProviderProps:
    def __init__(self, *, role: typing.Optional[aws_cdk.aws_iam.IRole] = None) -> None:
        '''The properties for the OU custom resource provider.

        :param role: The role the custom resource should use for taking actions on OUs if one is not provided one will be created automatically.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The role the custom resource should use for taking actions on OUs if one is not provided one will be created automatically.'''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationOUProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccountProps",
    "OUProps",
    "OUResourceProps",
    "OrgObject",
    "OrgObjectTypes",
    "OrganizationOU",
    "OrganizationOUProvider",
    "OrganizationOUProviderProps",
]

publication.publish()
