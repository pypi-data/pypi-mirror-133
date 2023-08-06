import json
import boto3
import logging
import pandas as pd
from io import StringIO, BytesIO
from botocore.exceptions import ClientError


def df_from_s3_csv(bucket, key):
    """

    :param s3_client: a boto3 client object for s3
    :param bucket: str
    :param key: str
    :return: pandas dataframe
    """
    s3_client = boto3.client('s3')

    obj = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj['Body'], sep=',', index_col=0)
    return df


def df_to_s3_csv(bucket, key, df):
    """

    :param s3_client: boto3 client object for s3
    :param bucket: str
    :param key: str
    :param df: pandas dataframe
    :return: True
    """
    s3_client = boto3.client('s3')

    with BytesIO() as csv_buffer:
        df.to_csv(csv_buffer)

        response = s3_client.put_object(Bucket=bucket, Key="bytes" + key, Body=csv_buffer.getvalue())

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    return status


def send_sqs_message(to_sqs_url, msg_body, region_name):
    """

    :param to_sqs_url: str
    :param msg_body: dictionary
    :param region_name: str
    :return:
    """
    sqs_client = boto3.client('sqs', region_name=region_name)

    try:
        msg = sqs_client.send_message(QueueUrl=to_sqs_url,
                                      MessageBody=json.dumps(msg_body))
        return msg

    except ClientError as e:
        logging.error(e)
        return None


def metric_node(
        event,
        context,
        to_sqs_url,
        region_name,
        to_bucket,
        to_key,
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
    completed_stations = [each for each in body['completed_stations']]

    orig_df = df_from_s3_csv(from_bucket, from_key)

    finished_df = func(orig_df)

    status = df_to_s3_csv(bucket=to_bucket, key=to_key, df=finished_df)

    if status == 200:
        logging.info(f'Successful S3 put_object response')

    else:
        logging.info(f'Unsuccessful S3 put_object response - {status}')

    completed_stations.append(context.function_name)

    message = {
        'bucket': from_bucket,
        'key': from_key,
        'completed_stations': completed_stations
    }

    msg = send_sqs_message(to_sqs_url, message, region_name)

    if msg is not None:
        logging.info(f'Sent SQS message ID: {msg["MessageId"]}')

    return {
        'statusCode': status,
        'body': message,
        'cols': list(finished_df.columns[:min(len(finished_df.columns), 5)])
    }
