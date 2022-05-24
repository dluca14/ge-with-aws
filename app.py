import json
import os

from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.data_context import DataContext


class ErrorResponse(Exception):
    def __init__(self, message='An error occurred', status_code=500):
        self.status_code = status_code
        self.body = json.dumps(message)
        self.headers = {
            'Content-Type': 'application/json',
        }

    def __str__(self):
        return {'status_code': self.status_code,
                'body': self.body,
                'headers': self.headers}


def handler(event, context):
    try:
        data_context: DataContext = DataContext(os.getcwd() + '/project/great_expectations')
        result: CheckpointResult = data_context.run_checkpoint(
            checkpoint_name="getting_started_checkpoint",
            batch_request=None,
            run_name=None,
        )
    except Exception as _e:
        e = _e
        if not isinstance(e, ErrorResponse):
            e = ErrorResponse('Error while running checkpoint results')

        return e.__str__()

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
