import json
import os
from datetime import datetime
from uuid import uuid4 as generate_id

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('AuditProducer-handler')


class AuditProducer(AbstractLambda):
    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(f'Using table: \n{json.dumps(event, indent=2)}')
        # Resolving
        lambda_name = os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'NO_NAME')
        dyn_table = lambda_name.replace('audit_producer', 'Audit')
        dyn_resource = boto3.resource('dynamodb')
        _LOG.info(f'Using table: {dyn_table}')
        table = dyn_resource.Table(dyn_table)

        for record in event['Records']:
            self.add_audit_action(table, record)

    def add_audit_action(self, table, record):
        recVal = record['dynamodb']
        payload = {
            'id': str(generate_id()),
            'itemKey': recVal['newImage']['key'],
            'modificationTime': datetime.now().isoformat()
        }
        if record['eventName'] == 'INSERT':
            payload['newValue'] = {
                'key': recVal['newImage']['key'],
                'value': recVal['newImage']['value']
            }
        elif record['eventName'] == 'MODIFY':
            payload['updatedAttribute'] = 'value'
            payload['oldValue'] = recVal['oldImage']['value']
            payload['newValue'] = recVal['newImage']['value']

        table.put_item(Item=payload)


HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
