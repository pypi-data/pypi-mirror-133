# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_timer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-timer',
    'version': '0.0.2',
    'description': 'Benchmark your code while unit testing them',
    'long_description': '## Benchmark your code while unit testing them\n\n### Usecases\n1. Problem solving. To quickly check different implementations and compare versions to find which one performs better.\n2. Quick algorithm mockup. Again, to quickly check different approaches and implementations and compare versions to find which one performs better.\n\n### What it does not provide insights about\n1. Overall performance score of your application.\n2. Algorithmic complexity.\n\n\n```Python\nimport time\nimport test_timer\n\n\ndef function_a():\n    ...\n\n\ndef function_b():\n    time.sleep(1)\n\n\nclass TestSrc(test_timer.BenchTestCase):\n    def test_function_a(self):\n        function_a()\n\n    def test_function_b(self):\n        function_b()\n\nif __name__ == "__main__":\n    test_timer.main()\n```\n\n```Bash\ntest_function_a (__main__.TestSrc): 0:00:00.000052\n.\ntest_function_b (__main__.TestSrc): 0:00:01.001192\n.\n----------------------------------------------------------------------\nRan 2 tests in 1.002s\n\nOK\n```\n\n### How to install:\n```Bash\npip install test_timer\n```\n',
    'author': 'nazrul',
    'author_email': 'mnazrul.c@gmail.com',
    'maintainer': 'nazrul',
    'maintainer_email': 'mnazrul.c@gmail.com',
    'url': 'https://github.com/mnislam01/test_timer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
