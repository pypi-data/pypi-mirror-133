import json
import boto3
import logging
from botocore.exceptions import ClientError

def send_sqs_message(to_sqs_url, msg_body, region_name,):
    """Send a message to SQS"""

    # Send the SQS message
    sqs_client = boto3.client('sqs', region_name=region_name)

    try:
        msg = sqs_client.send_message(QueueUrl=to_sqs_url,
                                      MessageBody=json.dumps(msg_body))
    except ClientError as e:
        logging.error(e)
        return None
    return msg

def metric_node(event, context, to_sqs_url, region_name, func=lambda x: x):
    """Execute function on filename found in the body of the event"""

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    fname = event["Records"][0]["body"]["filename"]
    func(fname)
    message = {'filename': fname}
    msg = send_sqs_message(to_sqs_url, json.dumps(message), region_name)
    if msg is not None:
        logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
    return {
        'statusCode': 200,
        'body': message
    }