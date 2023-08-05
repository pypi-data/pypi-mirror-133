# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_vite']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2', 'fastapi', 'pydantic[dotenv]>=1.9.0,<2.0.0', 'typer']

entry_points = \
{'console_scripts': ['fastapi-vite = fastapi_vite.cli:main']}

setup_kwargs = {
    'name': 'fastapi-vite',
    'version': '0.3.2',
    'description': 'Integration utilities for FastAPI and ViteJS.',
    'long_description': '# fastapi-vite\n\nIntegration for FastAPI and Vite JS\n\n## what?\n\nThis package is designed to make working with javascript assets easier.\n\nfastapi-vite enables the jinja filters required to render asset URLs to jinja templates\n\nInspired by `django-vite` @ [https://github.com/MrBin99/django-vite]\n\n## installation\n\nInstall using pip\n\n```shell\npip install fastapi-vite\n```\n\n## Usage\n\nConfigure Jinja templating for FastAPI\n\n```python\nimport fastapi_vite\n\ntemplates = Jinja2Templates(directory=\'templates\')\ntemplates.env.globals[\'vite_hmr_client\'] = fastapi_vite.vite_hmr_client\ntemplates.env.globals[\'vite_asset\'] = fastapi_vite.vite_asset\n\n```\n\n### Configure Vite\n\nHere is an example used to test this plugin\n\n```javascript\nimport { defineConfig } from \'vite\'\nimport reactRefresh from \'@vitejs/plugin-react-refresh\'\nconst Dotenv = require("dotenv");\nimport path from "path";\nDotenv.config({ path: path.join(__dirname, ".env") });\n\nconst STATIC_URL = process.env.STATIC_URL;\n// https://vitejs.dev/config/\nexport default defineConfig({\n  base: `${STATIC_URL}`,\n  clearScreen: false,\n  plugins: [\n    reactRefresh(),\n\n  ],\n  build: {\n    target: "esnext",\n    outDir: "./static/",\n    emptyOutDir: true,\n    assetsDir: "",\n    manifest: true,\n    rollupOptions: {\n      input:  "./assets/javascript/main.tsx"\n    },\n  },\n\n  root: ".", // You can change the root path as you wish\n\n})\n\n```\n\n### Configure Static Assets\n\n### Configure Templates\n\n\\*render_vite_hmr no-op when in production.\n\n```html\n{{ render_vite_hmr_client() }}\n\n<script\n  type="text/javascript"\n  defer\n  src="{{ asset_url(\'javascript/main.tsx\') }}"\n></script>\n```\n',
    'author': 'Cody Fincher',
    'author_email': 'cody.fincher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cofin/fastapi-vite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
