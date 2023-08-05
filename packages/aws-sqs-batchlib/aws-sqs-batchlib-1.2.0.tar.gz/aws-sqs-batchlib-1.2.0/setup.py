# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_sqs_batchlib']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.26,<2.0.0']

setup_kwargs = {
    'name': 'aws-sqs-batchlib',
    'version': '1.2.0',
    'description': 'Library working with Amazon SQS',
    'long_description': '# aws-sqs-batchlib for Python\n\nConsume and process Amazon SQS queues in large batches.\n\n## Features\n\n* Consume arbitrary number of messages from an Amazon SQS queue.\n\n  * Define maximum batch size and batching window in seconds to consume a batch\n    of messages from Amazon SQS queue similar to Lambda Event Source Mapping.\n\n* Delete arbitrary number of messages from an Amazon SQS queue.\n\n\n## Installation\n\nInstall from PyPI with pip\n\n```\npip install aws-sqs-batchlib\n```\n\nor with the package manager of choice.\n\n## Usage\n\n### Consume\n\n```python\nimport aws_sqs_batchlib\n\n# Consume up-to 100 messages from the given queue, polling the queue for\n# up-to 1 second to fill the batch.\nres = aws_sqs_batchlib.consume(\n    queue_url = "https://sqs.eu-north-1.amazonaws.com/123456789012/MyQueue",\n    batch_size=100,\n    maximum_batching_window_in_seconds=1,\n    VisibilityTimeout=300,\n)\n\n# Returns messages in the same format as boto3 / botocore SQS Client\n# receive_message() method.\nassert res == {\n    \'Messages\': [\n        {\'MessageId\': \'[.]\', \'ReceiptHandle\': \'AQ[.]JA==\', \'MD5OfBody\': \'[.]\', \'Body\': \'[.]\'},\n        {\'MessageId\': \'[.]\', \'ReceiptHandle\': \'AQ[.]wA==\', \'MD5OfBody\': \'[.]\', \'Body\': \'[.]\'}\n        # ... up-to 1000 messages\n    ]\n}\n```\n\n### Delete\n\n```python\nimport aws_sqs_batchlib\n\n# Delete an arbitrary number of messages from a queue\nres = aws_sqs_batchlib.delete_message_batch(\n    QueueUrl="https://sqs.eu-west-1.amazonaws.com/777907070843/test",\n    Entries=[\n        {"Id": "1", "ReceiptHandle": "<...>"},\n        {"Id": "2", "ReceiptHandle": "<...>"},\n        # ...\n        {"Id": "175", "ReceiptHandle": "<...>"},\n        # ...\n    ],\n)\n\n# Returns result in the same format as boto3 / botocore SQS Client\n# delete_message_batch() method.\nassert res == {\n    "Successful": [\n        {"Id": "1"},\n        # ...\n    ],\n    "Failed": [\n        {\n            "Id": "2",\n            "SenderFault": True,\n            "Code": "ReceiptHandleIsInvalid",\n            "Message": "The input receipt handle is invalid.",\n        }\n    ],\n}\n```\n\n\n## Development\n\nRequires Python 3 and Poetry. Useful commands:\n\n```bash\n# Setup environment\npoetry install\n\n# Run tests (integration test requires rights to create, delete and use DynamoDB tables)\nmake test\n\n# Run linters\nmake -k lint\n\n# Format code\nmake format\n```\n\n## Benchmarks & Manual Testing\n\nUse `benchmark/benchmark.py` to benchmark and test the library functionality and performance. Execute following commands in Poetry virtualenv (execute `poetry shell` to get there):\n\n```bash\n# Setup\nexport PYTHONPATH=$(pwd)\nexport AWS_DEFAULT_REGION=eu-north-1\n\n# Send messages to a queue\npython3 benchmark/benchmark.py \\\n  --queue-url https://sqs.eu-north-1.amazonaws.com/123456789012/MyQueue producer\n\n# Consume messages with the plain SQS ReceiveMessage polling\npython3 benchmark/benchmark.py \\\n  --queue-url https://sqs.eu-north-1.amazonaws.com/123456789012/MyQueue consumer-plain\n\n# Consume messages with the libary\npython3 benchmark/benchmark.py \\\n  --queue-url https://sqs.eu-north-1.amazonaws.com/123456789012/MyQueue consumer-lib \\\n  --batch-size 1000\n  --batch-window 1\n```\n\nSingle thread is able to receive / send around 400 messages per second to an SQS queue on the same AWS region (eu-north-1, m5.large instance).\n\n## License\n\nMIT.',
    'author': 'Sami Jaktholm',
    'author_email': 'sjakthol@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
