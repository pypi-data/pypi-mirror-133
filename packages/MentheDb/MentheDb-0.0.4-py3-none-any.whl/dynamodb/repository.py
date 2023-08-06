from abc import ABC
from botocore.exceptions import ClientError
import logging
import boto3
from botocore.config import Config

class Repository(ABC):
    pass


class DynamoRepository(Repository, ABC):
    def __init__(self, db_name: str, aws_key_id=None, aws_secret_key=None, region=str, table_name=None,
                 connect_timeout=5):
        self.db_name = db_name
        self.aws_secret_id = aws_key_id
        self.aws_secret_access_key = aws_secret_key
        self.region_name = region
        self.config = Config(connect_timeout=connect_timeout) # , read_timeout=1,  retries={'max_attempts': 1}
        self.dynamodb = boto3.resource(self.db_name, aws_access_key_id=self.aws_secret_id,
                                       aws_secret_access_key=self.aws_secret_access_key,
                                       region_name=self.region_name, config=self.config)
        if table_name is not None:
            self.table_object = self.dynamodb.Table(table_name)


class DynamoBaseInfoClientRepository(DynamoRepository):

    def __init__(self, db_name: str, aws_key_id=None, aws_secret_key=None, region=None, table_name=None,
                 connect_timeout=5):
        super().__init__(db_name=db_name, aws_key_id=aws_key_id,
                         aws_secret_key=aws_secret_key, region=region,
                         table_name=table_name, connect_timeout=connect_timeout)

    def create_table(self, second_index_name: str, t_name: str):
        table = self.dynamodb.create_table(
            TableName=t_name,
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'username',
                    'KeyType': 'RANGE'
                }

            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'registered_date',
                    'AttributeType': 'S'
                },

            ],
            LocalSecondaryIndexes=[
                {
                    'IndexName': t_name + second_index_name,
                    'KeySchema': [
                        {
                            'AttributeName': 'email',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'registered_date',
                            'KeyType': 'RANGE'
                        },

                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )
        print("Table status:", table.table_status)

    def put_item(self, item: dict, **kwargs):
        """
        A function to insert a new item into a specific table.
        There is an option to add a condition expression
        for possible kwargs:
        https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html

        :param item: item in dictionary form
        :return: dynamodb api response
        """
        table = self.table_object
        try:
            logging.info('Trying to inserting a single item: %s with additional key arg: %s' % (item, kwargs))
            response = table.put_item(Item=item, **kwargs)
        except ClientError as e:
            logging.info("Received error: %s", e, exc_info=True)
            response = e.response['Error']
        return response

    def update_item(self, key: dict, **kwargs):
        """
        A function to update a specifics fields of a given key item of a given table.
        for possible kwargs:
        https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html

        :param key: the keys to match
        :return: dynamodb api response
        """
        table = self.table_object
        try:
            logging.info('Trying to update a key item: %s with additional key arg: %s' % (key, kwargs))
            response = table.update_item(Key=key, **kwargs)
        except ClientError as e:
            logging.info("Received error: %s", e, exc_info=True)
            response = e.response['Error']

        return response

    def delete_item(self, key: dict, **kwargs):
        """

        for possible kwargs:
        https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html


        :param key: the keys to match
        :return: dynamodb api response
        """
        table = self.table_object
        try:
            logging.info('Trying to delete a key item: %s with additional key arg: %s' % (key, kwargs))
            response = table.delete_item(
                Key=key, **kwargs
            )
        except ClientError as e:
            logging.info("Received error: %s", e, exc_info=True)
            response = e.response['Error']

        return response

    def scan_all_registers(self, **kwargs):
        """
        A function which returns all registers of a table
        https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html

        :param kwargs: Scan arguments
        :return:
        """
        table = self.table_object

        done = False
        start_key = None
        response = table.scan(**kwargs)
        data = response.get('Items', None)
        while not done:
            if start_key:
                kwargs['ExclusiveStartKey'] = start_key
            response = table.scan(**kwargs)
            data.extend(response.get('Items', None))
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return data

    def get_item_by_key(self, **kwargs):

        table = self.table_object

        try:
            logging.info('Trying to get a key item: %s' % kwargs)
            response = table.query(**kwargs)
            # response = table.get_item(**kwargs)
        except ClientError as e:
            logging.info("Received error: %s", e, exc_info=True)
            response = e.response['Error']

        return response
