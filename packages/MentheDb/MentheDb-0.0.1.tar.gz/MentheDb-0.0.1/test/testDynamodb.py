from src.dynamodb import repository
import datetime
import uuid
from boto3.dynamodb.conditions import Key

# client = boto3.client('dynamodb', aws_access_key_id='AKIAUF7JYOLKZRLIZWNP',
#                       aws_secret_access_key='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',
#                       region_name='eu-west-1')
# db = boto3.resource('dynamodb', aws_access_key_id='AKIAUF7JYOLKZRLIZWNP',
#                       aws_secret_access_key='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',
#                       region_name='eu-west-1')


dynamodbObject = repository.DynamoBaseInfoClientRepository(table_name='BaseInfoClient', db_name='dynamodb',
                                                           region='eu-west-1')
# a = dynamodbObject.scan_all_registers(ProjectionExpression='email, registered_date1', Limit=10,
#                                   FilterExpression=Attr('name').eq('Nikolay') & Attr('mobilephone').eq('610983805'))
dynamodbObject = repository.DynamoBaseInfoClientRepository()
dynamodbObject.create_table(t_name='BaseInfoClient', second_index_name='OnCreateDate')

# tables = list(db.tables.all())
#
# pr = db.Table(name='id_cliente')
# baseInfo_cliente = db.Table(name='BaseInfoClient')
pru = dynamodbObject.put_item(item={
            'username': 'nichkata10',
            'email': 'nikolay.gyuneliev@gmail.com',
            'base_role': 'admin',
            'name': 'Nikolay',
            'surname': 'Gyuneliev',
            'password': 'dsfsafsaf',
            'mobilephone': '610983805',
            'registered_date': datetime.datetime.utcnow().replace(microsecond=0, second=0).isoformat(),
            'id_cliente': str(uuid.uuid4())
        }, ConditionExpression='attribute_not_exists(email)')

# UpdateExpression=upd_exp, ExpressionAttributeValues=expr_attr, ReturnValues="UPDATED_NEW"
# expr, val = StringExpressionsGen.gen_update_str_expression({'password': 'holadenuevo', 'activation_date': datetime.datetime.utcnow().replace(microsecond=0, second=0).isoformat()})
# dynamodbObject.delete_item(key={'email': 'nikolay.gyuneliev@gmail.com',
#                                                         'username': 'nichkata10'}, ConditionExpression="base_role=:val AND password=:pass",
#                            ExpressionAttributeValues={":val": "admin", ":pass": 'dsfsafsaf'})
# dynamodbObject.update_item(key={'email': 'nikolay.gyuneliev@gmail.com', 'username': 'nichkata10'},
#                            UpdateExpression=expr,
#                            ExpressionAttributeValues=val, ReturnValues="UPDATED_NEW")

# print((dynamodbObject.get_item_by_key(IndexName='BaseInfoClientOnCreateDate',
#                                       KeyConditionExpression=Key('email').eq('nikolay.gyuneliev@gmail.com'))))
# print(dynamodbObject.get_item_by_key(Key={'email': 'nikolay.gyuneliev@gmail.com', 'username': 'nichkata10'}))
# print(id_cliente.query(
#     IndexName='cliente_profile',
#     KeyConditionExpression=Key('email').eq('nikolay.gyuneliev@gmail.com')
# ))
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with AWS Key Management Service (AWS KMS)
to encrypt and decrypt data.
"""

import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class KeyEncrypt:
    def __init__(self, kms_client):
        self.kms_client = kms_client

    def encrypt(self, key_id):
        """
        Encrypts text by using the specified key.

        :param key_id: The ARN or ID of the key to use for encryption.
        :return: The encrypted version of the text.
        """
        text = input("Enter some text to encrypt: ")
        try:
            cipher_text = self.kms_client.encrypt(
                KeyId=key_id, Plaintext=text.encode())['CiphertextBlob']
        except ClientError as err:
            logger.error(
                "Couldn't encrypt text. Here's why: %s", err.response['Error']['Message'])
        else:
            print(f"Your ciphertext is: {cipher_text}")
            return cipher_text

    def decrypt(self, key_id, cipher_text):
        """
        Decrypts text previously encrypted with a key.

        :param key_id: The ARN or ID of the key used to decrypt the data.
        :param cipher_text: The encrypted text to decrypt.
        """
        answer = input("Ready to decrypt your ciphertext (y/n)? ")
        if answer.lower() == 'y':
            try:
                text = self.kms_client.decrypt(
                    KeyId=key_id, CiphertextBlob=cipher_text)['Plaintext']
            except ClientError as err:
                logger.error(
                    "Couldn't decrypt your ciphertext. Here's why: %s",
                    err.response['Error']['Message'])
            else:
                print(f"Your plaintext is {text.decode()}")
        else:
            print("Skipping decryption demo.")

    def re_encrypt(self, source_key_id, cipher_text):
        """
        Takes ciphertext previously encrypted with one key and reencrypt it by using
        another key.

        :param source_key_id: The ARN or ID of the original key used to encrypt the
                              ciphertext.
        :param cipher_text: The encrypted ciphertext.
        :return: The ciphertext encrypted by the second key.
        """
        destination_key_id = input(
            f"Your ciphertext is currently encrypted with key {source_key_id}. "
            f"Enter another key ID or ARN to reencrypt it: ")
        if destination_key_id != '':
            try:
                cipher_text = self.kms_client.re_encrypt(
                    SourceKeyId=source_key_id, DestinationKeyId=destination_key_id,
                    CiphertextBlob=cipher_text)['CiphertextBlob']
            except ClientError as err:
                logger.error(
                    "Couldn't reencrypt your ciphertext. Here's why: %s",
                    err.response['Error']['Message'])
            else:
                print(f"Reencrypted your ciphertext as: {cipher_text}")
                return cipher_text
        else:
            print("Skipping reencryption demo.")


def key_encryption(kms_client):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    print('-'*88)
    print("Welcome to the AWS Key Management Service (AWS KMS) key encryption demo.")
    print('-'*88)

    key_id = input("Enter a key ID or ARN to start the demo: ")
    if key_id == '':
        print("A key is required to run this demo.")
        return

    key_encrypt = KeyEncrypt(kms_client)
    cipher_text = key_encrypt.encrypt(key_id)
    print('-'*88)
    if cipher_text is not None:
        key_encrypt.decrypt(key_id, cipher_text)
        print('-'*88)
        key_encrypt.re_encrypt(key_id, cipher_text)

    print("\nThanks for watching!")
    print('-'*88)


if __name__ == '__main__':
    try:
        key_encryption(boto3.client('kms'))
    except Exception:
        logging.exception("Something went wrong with the demo!")



