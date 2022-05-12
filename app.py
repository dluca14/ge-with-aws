import json
import os

from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.data_context import DataContext


def handler(event, context):
    data_context: DataContext = DataContext(os.getcwd() + '/project/great_expectations')

    result: CheckpointResult = data_context.run_checkpoint(
        checkpoint_name="getting_started_checkpoint",
        batch_request=None,
        run_name=None,
    )

    body = {
        "message": "Your checkpoint executed unsuccessfully!",
        "input": event
    }
    if not result["success"]:
        body = {
            "message": "Your checkpoint executed successfully!",
            "input": event
        }

    response = {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json'
        },
        "body": json.dumps(body)
    }
    return response
