import json
import boto3
import logging
import pandas as pd
from io import StringIO
from botocore.exceptions import ClientError


def df_from_s3_csv(s3_client, bucket, key):
    """

    :param s3_client: a boto3 client object for s3
    :param bucket: str
    :param key: str
    :return: pandas dataframe
    """
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj['Body'], sep=',',  index_col=0)


def df_to_s3_csv(s3_client, bucket, key, df):
    """

    :param s3_client: boto3 client object for s3
    :param bucket: str
    :param key: str
    :param df: pandas dataframe
    :return: True
    """
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)

    s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

    return True


def send_sqs_message(to_sqs_url, queue_name, msg_body, region_name):
    """

    :param to_sqs_url: str
    :param queue_name:
    :param msg_body: dictionary
    :param region_name: str
    :return:
    """
    sqs_client = boto3.client('sqs', region_name=region_name)

    if queue_name != "":
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)
        msg = sqs_client.send_message(QueueUrl=queue_url,
                                      MessageBody=json.dumps(msg_body))

    else:
        try:
            msg = sqs_client.send_message(QueueUrl=to_sqs_url,
                                          MessageBody=json.dumps(msg_body))
        except ClientError as e:
            logging.error(e)
            return None
    return msg


def metric_node(
        event,
        context,
        to_sqs_url,
        region_name,
        to_bucket,
        to_key,
        queue_name="",
        func=lambda x: x
):
    """
        The structure of a processing station: receive, load, do, save, send

    Load a pandas dataframe from the buck/key referenced in the triggering event
    Execute func on the dataframe which must return a df
    Put the df into to_bucket/key
    Send message to to_sqs_url

    :param event:
    :param context:
    :param to_sqs_url: str
    :param region_name: str
    :param to_bucket: str
    :param to_key: str
    :param queue_name:  CURRENTLY OVERRIDDEN AS IT FAILS
    :param func: function that takes a pandas df and returns a pandas df
    :return:
    """

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    body = event["Records"][0]["body"]
    if isinstance(body, str):
        body = json.loads(body)

    from_bucket = body['bucket']
    from_key = body['key']
    completed_stations = body['completed_stations']

    s3_client = boto3.client('s3')

    orig_df = df_from_s3_csv(s3_client, from_bucket, from_key)

    finished_df = func(orig_df)

    df_to_s3_csv(s3_client, to_bucket, to_key, finished_df)

    completed_stations.append(context.function_name)

    message = {
        'bucket': from_bucket,
        'key': from_key,
        'completed_stations': completed_stations
    }

    # override queue name until we can find a way to grant access to the queue
    queue_name = ""
    msg = send_sqs_message(to_sqs_url, queue_name, message, region_name)

    if msg is not None:
        logging.info(f'Sent SQS message ID: {msg["MessageId"]}')

    return {
        'statusCode': 200,
        'body': message,
        'cols': list(finished_df.columns[:min(len(finished_df.columns), 5)])
    }
