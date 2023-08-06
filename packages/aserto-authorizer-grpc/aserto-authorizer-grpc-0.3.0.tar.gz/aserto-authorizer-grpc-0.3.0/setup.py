# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aserto_authorizer_grpc',
 'aserto_authorizer_grpc.aserto',
 'aserto_authorizer_grpc.aserto.api',
 'aserto_authorizer_grpc.aserto.api.v1',
 'aserto_authorizer_grpc.aserto.authorizer',
 'aserto_authorizer_grpc.aserto.authorizer.authorizer',
 'aserto_authorizer_grpc.aserto.authorizer.authorizer.v1',
 'aserto_authorizer_grpc.aserto.options',
 'aserto_authorizer_grpc.aserto.options.v1',
 'aserto_authorizer_grpc.google',
 'aserto_authorizer_grpc.google.api',
 'aserto_authorizer_grpc.grpc',
 'aserto_authorizer_grpc.grpc.gateway',
 'aserto_authorizer_grpc.grpc.gateway.protoc_gen_openapiv2',
 'aserto_authorizer_grpc.grpc.gateway.protoc_gen_openapiv2.options']

package_data = \
{'': ['*']}

install_requires = \
['betterproto==v2.0.0b4',
 'certifi>=2021.5.30,<2022.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'aserto-authorizer-grpc',
    'version': '0.3.0',
    'description': 'gRPC client for Aserto Authorizer service instances',
    'long_description': '# Aserto Authorizer gRPC client\nThis is an automatically generated client for interacting with Aserto\'s [Authorizer service](https://docs.aserto.com/docs/authorizer-guide/overview) using the gRPC protocol.\n\n## Installation\n### Using Pip\n```sh\npip install aserto-authorizer-grpc\n```\n### Using Poetry\n```sh\npoetry add aserto-authorizer-grpc\n```\n## Usage\n```py\nfrom aserto_authorizer_grpc.aserto.api.v1 import (\n    IdentityContext,\n    IdentityType,\n    PolicyContext,\n)\nfrom aserto_authorizer_grpc.aserto.authorizer.authorizer.v1 import (\n    AuthorizerStub,\n    DecisionTreeOptions,\n    DecisionTreeResponse,\n    PathSeparator,\n    Proto,\n)\nfrom grpclib.client import Channel\n\n\nasync with Channel(host=host, port=port, ssl=True) as channel:\n    headers = {\n        "aserto-tenant-id": TENANT_ID,\n        "authorization": f"basic {ASERTO_API_KEY}"\n    }\n\n    client = AuthorizerStub(channel, metadata=headers)\n\n    response = await client.decision_tree(\n        policy_context=PolicyContext(\n            id=ASERTO_POLICY_ID,\n            path=ASERTO_POLICY_PATH_ROOT,\n            decisions=["visible", "enabled", "allowed"],\n        ),\n        identity_context=IdentityContext(type=IdentityType.IDENTITY_TYPE_NONE),\n        resource_context=Proto.Struct(),\n        options=DecisionTreeOptions(\n            path_separator=PathSeparator.PATH_SEPARATOR_DOT,\n        ),\n    )\n\n    assert response == DecisionTreeResponse(\n        path_root=ASERTO_POLICY_PATH_ROOT,\n        path=Proto.Struct(\n            fields={\n                "GET.your.policy.path": Proto.Value(\n                    struct_value=Proto.Struct(\n                        fields={\n                            "visible": Proto.Value(bool_value=True),\n                            "enabled": Proto.Value(bool_value=True),\n                            "allowed": Proto.Value(bool_value=False),\n                        },\n                    ),\n                ),\n            },\n        ),\n    )\n```',
    'author': 'Aserto, Inc.',
    'author_email': 'pypi@aserto.com',
    'maintainer': 'authereal',
    'maintainer_email': 'authereal@aserto.com',
    'url': 'https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/aserto-authorizer-grpc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
