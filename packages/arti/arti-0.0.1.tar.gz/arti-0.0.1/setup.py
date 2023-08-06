# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['arti',
 'arti.annotations',
 'arti.artifacts',
 'arti.backends',
 'arti.executors',
 'arti.fingerprints',
 'arti.formats',
 'arti.graphs',
 'arti.internal',
 'arti.internal.vendored',
 'arti.io',
 'arti.partitions',
 'arti.producers',
 'arti.statistics',
 'arti.storage',
 'arti.thresholds',
 'arti.types',
 'arti.versions',
 'arti.views']

package_data = \
{'': ['*']}

install_requires = \
['frozendict>=2.1.0,<3.0.0',
 'multimethod>=1.6,<2.0',
 'parse>=1.19.0,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyfarmhash>=0.2.2,<0.4.0',
 'python-box>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'arti',
    'version': '0.0.1',
    'description': '',
    'long_description': '# artigraph\n\n[![pypi](https://img.shields.io/pypi/v/arti.svg)](https://pypi.python.org/pypi/arti)\n[![downloads](https://pepy.tech/badge/arti/month)](https://pepy.tech/project/arti)\n[![versions](https://img.shields.io/pypi/pyversions/arti.svg)](https://github.com/artigraph/artigraph)\n[![license](https://img.shields.io/github/license/artigraph/artigraph.svg)](https://github.com/artigraph/artigraph/blob/golden/LICENSE)\n[![CI](https://github.com/artigraph/artigraph/actions/workflows/ci.yaml/badge.svg)](https://github.com/artigraph/artigraph/actions/workflows/ci.yaml)\n[![codecov](https://codecov.io/gh/artigraph/artigraph/branch/golden/graph/badge.svg?token=6LUCpjcGdN)](https://codecov.io/gh/artigraph/artigraph)\n\nDeclarative Data Production\n\n## Installation\n\nArtigraph can be installed from PyPI on python 3.9+ with `pip install arti`.\n\n## Example\n\nThis [simple example](docs/examples/spend/demo.py) takes a series of purchase transactions and computes the total amount spent:\n\n```python\nfrom pathlib import Path\nfrom typing import Annotated\n\nfrom arti import Annotation, Artifact, Graph, producer\nfrom arti.formats.json import JSON\nfrom arti.storage.local import LocalFile\nfrom arti.types import Collection, Date, Float64, Int64, Struct\nfrom arti.versions import SemVer\n\nDIR = Path(__file__).parent\n\n\nclass Vendor(Annotation):\n    name: str\n\n\nclass Transactions(Artifact):\n    """Transactions partitioned by day."""\n\n    type = Collection(\n        element=Struct(fields={"id": Int64(), "date": Date(), "amount": Float64()}),\n        partition_by=("date",),\n    )\n\n\nclass TotalSpend(Artifact):\n    """Aggregate spend over all time."""\n\n    type = Float64()\n    format = JSON()\n    storage = LocalFile()\n\n\n@producer(version=SemVer(major=1, minor=0, patch=0))\ndef aggregate_transactions(\n    transactions: Annotated[list[dict], Transactions]\n) -> Annotated[float, TotalSpend]:\n    return sum(txn["amount"] for txn in transactions)\n\n\nwith Graph(name="test") as g:\n    g.artifacts.vendor.transactions = Transactions(\n        annotations=[Vendor(name="Acme")],\n        format=JSON(),\n        storage=LocalFile(path=str(DIR / "transactions" / "{date.iso}.json")),\n    )\n    g.artifacts.spend = aggregate_transactions(transactions=g.artifacts.vendor.transactions)\n```\n\nThis example can be run easily with `docker run --rm artigraph/example-spend`.\n',
    'author': 'Jacob Hayes',
    'author_email': 'jacob.r.hayes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/artigraph/artigraph',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
