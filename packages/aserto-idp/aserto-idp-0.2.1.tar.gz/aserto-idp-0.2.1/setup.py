# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aserto_idp']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'python-jose[cryptography]>=3.3.0,<4.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'aserto-idp',
    'version': '0.2.1',
    'description': 'Common identity providers for use with Aserto client libraries',
    'long_description': '# Aserto Identity Providers\nCommon identity providers for use with Aserto client libraries\n\n## Installation\n### Using Pip\n```sh\npip install aserto-idp\n```\n### Using Poetry\n```sh\npoetry add aserto-idp\n```\n## Current Identity Providers\n### Auth0\n```py\nfrom aserto_idp.auth0 import generate_oauth_subject_from_auth_header\n```\n### Stay tuned for more!\n## Usage\n### With [`aserto-authorizer-grpc`](https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/aserto-authorizer-grpc)\n```py\nfrom aserto_authorizer_grpc.aserto.api.v1 import IdentityContext, IdentityType\nfrom aserto_idp.auth0 import AccessTokenError, generate_oauth_subject_from_auth_header\n\n\ntry:\n    subject = await generate_oauth_subject_from_auth_header(\n        authorization_header=request.headers["Authorization"],\n        domain=AUTH0_DOMAIN,\n        client_id=AUTH0_CLIENT_ID,\n        audience=AUTH0_AUDIENCE,\n    )\n\n    identity_context = IdentityContext(\n        type=IdentityType.IDENTITY_TYPE_SUB,\n        identity=subject,\n    )\nexcept AccessTokenError:\n    identity_context = IdentityContext(type=IdentityType.IDENTITY_TYPE_NONE)\n\n```\n### With [`aserto`](https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/aserto)\n```py\nfrom aserto import Identity\nfrom aserto_idp.auth0 import AccessTokenError, generate_oauth_subject_from_auth_header\n\n\ntry:\n    subject = await generate_oauth_subject_from_auth_header(\n        authorization_header=request.headers["Authorization"],\n        domain=AUTH0_DOMAIN,\n        client_id=AUTH0_CLIENT_ID,\n        audience=AUTH0_AUDIENCE,\n    )\n\n    identity = Identity(type="SUBJECT", subject=subject)\nexcept AccessTokenError:\n    identity = Identity(type="NONE")\n```',
    'author': 'Aserto, Inc.',
    'author_email': 'pypi@aserto.com',
    'maintainer': 'authereal',
    'maintainer_email': 'authereal@aserto.com',
    'url': 'https://github.com/aserto-dev/aserto-python/tree/HEAD/packages/aserto-idp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
