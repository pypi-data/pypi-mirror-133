import logging
import boto3
from botocore.exceptions import ClientError
import os
from aiohttp import web
from heaserver.service import response
from aiohttp.web import Response
from aiohttp.web import Request

"""
Available functions
AWS object
- get

- change_storage_class            TODO
- copy_object
- delete_bucket_objects
- delete_bucket
- delete_folder
- delete_object
- download_object
- download_archive_object         TODO
- generate_presigned_url
- get_object_meta
- get_object_content
- get_all_buckets
- get all
- opener                          TODO -> return file format -> returning metadata containing list of links following collection + json format
-                                         need to pass back collection - json format with link with content type, so one or more links, most likely
- post_bucket
- post_folder
- post_object
- post_object_archive             TODO
- put_bucket
- put_folder
- put_object
- put_object_archive              TODO
- transfer_object_within_account
- transfer_object_between_account TODO
- rename_object
- update_bucket_policy            TODO

TO DO
- accounts?
"""


def get_account(request: Request, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Gets the content to populate the aws account object. Only get since you can't delete or put id information currently being accessed.
    If organizations get included, then the delete, put, and post will be added for name, phone, email, ,etc.
    NOTE: maybe get email from the login portion of the application?

    :return: account object with
        account id
        account name
        full name
        phone number
        alternate contact name
        alternate email address
        alternate phone number
        charge account?
    """
    aws_object_dict = {}
    sts_client = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    iam_client = boto3.client('iam', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # account_client = boto3.client('account', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # gets email and name, and maybe alternate contact stuff?, require higher permissions.
    # org = boto3.client('organizations')
    # account_name = org.describe_account(AccountId='account-id').get('Account')
    # print(account_name['Name'])
    # response = iam_client.get_alternate_contact(
    #     AccountId=sts_client.get_caller_identity().get('Account'),
    #     AlternateContactType='BILLING' | 'OPERATIONS' | 'SECURITY'
    # )
    # print(response)

    aws_object_dict["account_id"] = sts_client.get_caller_identity().get('Account')
    aws_object_dict["alias"] = iam_client.list_account_aliases()['AccountAliases'][0]
    aws_object_dict["username"] = iam_client.get_user()["User"]["UserName"]
    aws_object_dict["user_id"] = iam_client.get_user()["User"]["UserId"]
    return response.get(request, aws_object_dict)


def post_account():
    """
    Placeholder for when this may get implemented in the future.
    """
    return response.status_not_found()


def put_account():
    """
    Placeholder for when this may get implemented in the future.
    """
    return response.status_not_found()


def delete_account():
    """
    Placeholder for when this may get implemented in the future.
    """
    return response.status_not_found()


def change_storage_class():
    """
    change storage class (Archive, un-archive) (copy and delete old)

    S3 to archive -> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.upload_archive
        save archive id for future access?
        archived gets charged minimum 90 days
        buckets = vault?
        delete bucket
    archive to S3
        create vault? link vault to account as attribute?
        delete vault
    """


def copy_object(source_path, destination_path, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    copy/paste (duplicate), throws error if destination exists, this so an overwrite isn't done
    throws another error is source doesn't exist
    https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
    https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3

    :param source_path: (str) s3 path of object, includes bucket and key values together
    :param destination_path: (str) s3 path of object, includes bucket and key values together
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    # Copy object A as object B
    s3_resource = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    source_bucket_name = source_path.partition("/")[0]
    source_key_name = source_path.partition("/")[2]
    copy_source = {'Bucket': source_bucket_name, 'Key': source_key_name}
    destination_bucket_name = destination_path.partition("/")[0]
    destination_key_name = destination_path.partition("/")[2]
    try:
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3_client.head_object(Bucket=destination_bucket_name, Key=destination_key_name)  # check if destination object exists, if doesn't throws an exception
        return web.HTTPBadRequest()
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':  # object doesn't exist
            try:
                s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
                s3_client.head_object(Bucket=source_bucket_name, Key=source_key_name)  # check if source object exists, if not throws an exception
                s3_resource.meta.client.copy(copy_source, destination_path.partition("/")[0], destination_path.partition("/")[2])
                logging.info(e)
                return web.HTTPCreated()
            except ClientError as e:
                logging.error(e)
                return web.HTTPBadRequest()
        else:
            logging.info(e)
            return web.HTTPBadRequest()


def delete_bucket_objects(bucket_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Deletes all objects inside a bucket

    :param bucket_name: Bucket to delete
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    try:
        s3_resource = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3_client.head_bucket(Bucket=bucket_name)
        s3_bucket = s3_resource.Bucket(bucket_name)
        bucket_versioning = s3_resource.BucketVersioning(bucket_name)
        if bucket_versioning.status == 'Enabled':
            del_obj_all_result = s3_bucket.object_versions.delete()
            logging.info(del_obj_all_result)
        else:
            del_obj_all_result = s3_bucket.objects.all().delete()
            logging.info(del_obj_all_result)
        return web.HTTPNoContent()
    except ClientError as e:
        logging.error(e)
        return web.HTTPNotFound()


def delete_bucket(bucket_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Deletes bucket and all contents

    :param bucket_name: Bucket to delete
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        delete_bucket_objects(bucket_name)
        del_bucket_result = s3_client.delete_bucket(Bucket=bucket_name)
        logging.info(del_bucket_result)
        return web.HTTPNoContent()
    except ClientError as e:
        logging.error(e)
        return web.HTTPNotFound()


def delete_folder(path_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Deletes folder and all contents

    :param path_name: path to delete folder, split into bucket and folder for function
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library

    https://izziswift.com/amazon-s3-boto-how-to-delete-folder/
    """
    # TODO: bucket.object_versions.filter(Prefix="myprefix/").delete()     add versioning option like in the delete bucket?
    # TODO: throws error if bucket doesn't exist, should this be desired effect?
    bucket_name = path_name.partition("/")[0]
    folder_name = path_name.partition("/")[2]
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        s3_client.head_object(Bucket=bucket_name, Key=(folder_name + '/'))  # check if folder exists, if not throws an exception
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name + '/', MaxKeys=10000000)
        for object_f in response['Contents']:
            s3_client.delete_object(Bucket=bucket_name, Key=object_f['Key'])
        delete_folder_result = s3_client.delete_object(Bucket=bucket_name, Key=folder_name + '/')
        logging.info(delete_folder_result)
        return web.HTTPNoContent()
    except ClientError as e:
        logging.error(e)
        return web.HTTPNotFound()


def delete_object(path_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Deletes a single object, checks if object exists before deleting, throws error if it doesn't

    :param path_name: path to the object to delete
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
    """
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket_name = path_name.partition("/")[0]
    key_name = path_name.partition("/")[2]
    try:
        # TODO: when last object is deleted the folder is also deleted. Should this be saved?
        s3_client.head_object(Bucket=bucket_name, Key=key_name)  # check if object exists, if not throws an exception
        delete_response = s3_client.delete_object(Bucket=bucket_name, Key=key_name)
        logging.info(delete_response)
        return web.HTTPNoContent()
    except ClientError as e:
        logging.error(e)
        return web.HTTPBadRequest()


def download_object(object_path, save_path, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    r"""
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file

    :param object_path: path to the object to download
    :param save_path: path of where object is to be saved, note, needs to include the name of the file to save to
        ex: r'C:\Users\...\Desktop\README.md'  not  r'C:\Users\...\Desktop\'
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    try:
        s3_resource = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        bucket_name = object_path.partition("/")[0]
        folder_name = object_path.partition("/")[2]
        s3_resource.meta.client.download_file(bucket_name, folder_name, save_path)
    except ClientError as e:
        logging.error(e)


def download_archive_object(length=1):
    """

    """


def get_archive():
    """
    Don't think it is worth it to have a temporary view of data, expensive and very slow
    """


def generate_presigned_url(path_name, expiration=3600, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """Generate a presigned URL to share an S3 object

    :param path_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :return: Presigned URL as string. If error, returns None.

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    """
    # Generate a presigned URL for the S3 object
    try:
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        bucket_name = path_name.partition("/")[0]
        folder_name = path_name.partition("/")[2]
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': folder_name}, ExpiresIn=expiration)
        logging.info(response)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response


def get_object_meta(path_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    preview object in object explorer

    :param path_name: path to the object to get, includes both bucket and key values
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    try:
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        bucket_name = path_name.partition("/")[0]
        folder_name = path_name.partition("/")[2]
        response = s3_client.get_object(Bucket=bucket_name, Key=folder_name)
        logging.info(response["ResponseMetadata"])
        return response["ResponseMetadata"]  # .read(amt=1024)
        # return response  # ["Body"] .read()   .read(amt=chunk_size)
    except ClientError as e:
        logging.error(e)


def get_object_content(path_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    preview object in object explorer

    :param path_name: path to the object to get, includes both bucket and key values
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    try:
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        bucket_name = path_name.partition("/")[0]
        folder_name = path_name.partition("/")[2]
        response = s3_client.get_object(Bucket=bucket_name, Key=folder_name)
        logging.info(response["ResponseMetadata"])
        return response["Body"]  # .read(amt=1024)
        # return response  # ["Body"] .read()   .read(amt=chunk_size)
    except ClientError as e:
        logging.error(e)


def get_all_buckets(aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    List available buckets by name

    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library

    :return: (list) list of available buckets
    """
    try:
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        response = s3_client.list_buckets()
        bucket_list = []
        for bucket in response['Buckets']:
            bucket_list.append(f'{bucket["Name"]}')
        return bucket_list
    except ClientError as e:
        logging.error(e)


def get_all(bucket_name, max_keys=1000, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    List all objects in entire bucket. This includes folder names.

    :param bucket_name: (str) name of bucket to list objects in
    :param max_keys: (int) max number of objects to list, list_objects_v2 defualts to 1000
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    try:
        object_list = []
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=max_keys)
        logging.info(response)
        for val in response["Contents"]:
            object_list.append(val["Key"])
        return object_list
    except ClientError as e:
        logging.error(e)


def opener(aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """

    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """


def post_bucket(bucket_name, region=None, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Create an S3 bucket in a specified region, checks that it is the first, if already exists errors are thrown
    If a region is not specified, the bucket is created in the S3 default region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        response = s3_client.head_bucket(Bucket=bucket_name)  # check if bucket exists, if not throws an exception
        logging.info(response)
        return web.HTTPBadRequest(body="bucket already exists")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':  # bucket doesn't exist
            if region is None:
                create_bucket_result = s3_client.create_bucket(Bucket=bucket_name)
                logging.info(create_bucket_result)
                return web.HTTPCreated()
                # return response.put(create_bucket_result["ResponseMetadata"]["HTTPStatusCode"])
            else:
                create_bucket_result = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
                logging.info(create_bucket_result)
                return web.HTTPCreated()
        elif error_code == '403':  # already exists
            logging.error(e)
            return web.HTTPBadRequest(body="bucket exists, no permission to access")
        else:
            logging.error(e)
            return web.HTTPBadRequest()


def post_folder(path_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Adds a folder to bucket given in parameter, checks that it is the first, if already exists errors are thrown

    :param path_name: (str) path to delete folder, split into bucket and folder for function, input as bucket and key values together
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    bucket_name = path_name.partition("/")[0]
    folder_name = path_name.partition("/")[2]
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=(folder_name + '/'))  # check if folder exists, if not throws an exception
        logging.info(response)
        return web.HTTPBadRequest(body="folder already exists")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':  # folder doesn't exist
            add_folder_result = s3_client.put_object(Bucket=bucket_name, Key=(folder_name + '/'))
            logging.info(add_folder_result)
            return web.HTTPCreated()
        else:
            logging.error(e)
            return web.HTTPBadRequest()


def post_object(path_name, file_path, object_name=None, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """Upload a file to an S3 bucket, checks that it is the first, if already exists errors are thrown

    :param file_path: Path to the file to upload
    :param path_name: path to the location of object
    :param object_name: S3 object name. If not specified then file_name is used
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename((os.path.normpath(file_path)))  # only gets the last part of the path so identifiable info not included

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket_name = path_name.partition("/")[0]
    key_name = path_name.partition("/")[2]
    try:
        upload_response = s3_client.head_object(Bucket=bucket_name, Key=key_name + object_name)  # check if folder exists, if not throws an exception
        logging.info(upload_response)
        return web.HTTPBadRequest(body="object already exists")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':  # folder doesn't exist
            upload_response = s3_client.upload_file(file_path, bucket_name, key_name + object_name)
            logging.info(upload_response)
            return web.HTTPCreated()
        else:
            logging.info(e)
            return web.HTTPBadRequest()


def post_object_archive():
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html
    """


def put_bucket(bucket_name, region=None, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Create an S3 bucket in a specified region, if it doesn't exist an error will be thrown
    If a region is not specified, the bucket is created in the S3 default region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        s3_client.head_bucket(Bucket=bucket_name)  # check if bucket exists, if not throws an exception
        if region is None:
            create_bucket_result = s3_client.create_bucket(Bucket=bucket_name)
            logging.info(create_bucket_result)
            return web.HTTPCreated()
        else:
            create_bucket_result = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
            logging.info(create_bucket_result)
            return web.HTTPCreated()
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            logging.error(e)
            return web.HTTPBadRequest(body="bucket doesn't exist")
        elif error_code == '403':
            logging.error(e)
            return web.HTTPBadRequest(body="bucket exists, no permission to access")
        else:
            logging.error(e)
            return web.HTTPBadRequest()


def put_folder(path_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    Adds a folder to bucket given in parameter, if it doesn't exist, throws error

    :param path_name: (str) path to delete folder, split into bucket and folder for function, input as bucket and key values together
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    bucket_name = path_name.partition("/")[0]
    folder_name = path_name.partition("/")[2]
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        s3_client.head_object(Bucket=bucket_name, Key=(folder_name + '/'))  # check if folder exists, if not throws an exception
        add_folder_result = s3_client.put_object(Bucket=bucket_name, Key=(folder_name + '/'))
        logging.info(add_folder_result)
        return web.HTTPCreated()
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':  # folder doesn't exist
            logging.error(e)
            return web.HTTPBadRequest()
        else:
            logging.error(e)
            return web.HTTPBadRequest()


def put_object(path_name, file_path, object_name=None, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """Upload a file to an S3 bucket, if doesn't exist, throws error

    :param file_path: Path to the file to upload
    :param path_name: path to the location of object
    :param object_name: S3 object name. If not specified then file_name is used
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename((os.path.normpath(file_path)))  # only gets the last part of the path so identifiable info not included

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket_name = path_name.partition("/")[0]
    folder_name = path_name.partition("/")[2]
    try:
        s3_client.head_object(Bucket=bucket_name, Key=folder_name + object_name)  # check if folder exists, if not throws an exception
        upload_response = s3_client.upload_file(file_path, bucket_name, folder_name + object_name)
        logging.info(upload_response)
        return web.HTTPCreated()
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':  # folder doesn't exist
            logging.error(e)
            return web.HTTPBadRequest()
        else:
            logging.error(e)
            return web.HTTPBadRequest()


def put_object_archive():
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html
    """


def transfer_object_within_account(object_path, new_path, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    same as copy_object, but also deletes the object

    :param object_path (str) gives the old location of the object, input as the bucket and key together
    :param new_path: (str) gives the new location to put the object
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    copy_object(object_path, new_path, aws_access_key_id, aws_secret_access_key)
    delete_object(object_path, aws_access_key_id, aws_secret_access_key)


def transfer_object_between_account():
    """
    https://markgituma.medium.com/copy-s3-bucket-objects-across-separate-aws-accounts-programmatically-323862d857ed
    """
    # TODO: use update_bucket_policy to set up "source" bucket policy correctly
    """
    {
    "Version": "2012-10-17",
    "Id": "Policy1546558291129",
    "Statement": [
        {
            "Sid": "Stmt1546558287955",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<AWS_IAM_USER>"
            },
            "Action": [
              "s3:ListBucket",
              "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::<SOURCE_BUCKET>/",
            "Resource": "arn:aws:s3:::<SOURCE_BUCKET>/*"
        }
    ]
    }
    """
    # TODO: use update_bucket_policy to set up aws "destination" bucket policy
    """
    {
    "Version": "2012-10-17",
    "Id": "Policy22222222222",
    "Statement": [
        {
            "Sid": "Stmt22222222222",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                  "arn:aws:iam::<AWS_IAM_DESTINATION_USER>",
                  "arn:aws:iam::<AWS_IAM_LAMBDA_ROLE>:role/
                ]
            },
            "Action": [
                "s3:ListBucket",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::<DESTINATION_BUCKET>/",
            "Resource": "arn:aws:s3:::<DESTINATION_BUCKET>/*"
        }
    ]
    }
    """
    # TODO: code
    source_client = boto3.client('s3', "SOURCE_AWS_ACCESS_KEY_ID", "SOURCE_AWS_SECRET_ACCESS_KEY")
    source_response = source_client.get_object(Bucket="SOURCE_BUCKET", Key="OBJECT_KEY")
    destination_client = boto3.client('s3', "DESTINATION_AWS_ACCESS_KEY_ID", "DESTINATION_AWS_SECRET_ACCESS_KEY")
    destination_client.upload_fileobj(source_response['Body'], "DESTINATION_BUCKET", "FOLDER_LOCATION_IN_DESTINATION_BUCKET")


def rename_object(object_path, new_name, aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key')):
    """
    BOTO3, the copy and rename is the same
    https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
    https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3

    :param object_path: (str) path to object, includes both bucket and key values
    :param new_name: (str) value to rename the object as, will only replace the name not the path. Use transfer object for that
    :param aws_access_key_id: (str) authentication keys from aws account needed to perform calls by the boto3 library
    :param aws_secret_access_key: (str) authentication keys from aws account needed to perform calls by the boto3 library
    """
    # TODO: check if ACL stays the same and check existence
    try:
        s3_resource = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        copy_source = {'Bucket': object_path.partition("/")[0], 'Key': object_path.partition("/")[2]}
        bucket_name = object_path.partition("/")[0]
        old_name = object_path.rpartition("/")[2]
        s3_resource.meta.client.copy(copy_source, bucket_name, object_path.partition("/")[2].replace(old_name, new_name))
    except ClientError as e:
        logging.error(e)


def update_bucket_policy():
    """

    """


# if __name__ == "__main__":
    # print(get_account())
    # print(post_bucket('richardmtest'))
    # print(put_bucket("richardmtest"))
    # print(get_all_buckets())
    # print(get_all("richardmtest"))
    # print(post_folder('richardmtest/temp'))
    # print(put_folder("richardmtest/temp"))
    # print(post_object(r'richardmtest/temp/', r'C:\Users\u0933981\IdeaProjects\heaserver\README.md'))
    # print(put_object(r'richardmtest/temp/', r'C:\Users\u0933981\IdeaProjects\heaserver\README.md'))
    # download_object(r'richardmtest/temp/README.md', r'C:\Users\u0933981\Desktop\README.md')
    # rename_object(r'richardmtest/README.md', 'readme2.md')
    # print(copy_object(r'richardmtest/temp/README.md', r'richardmtest/temp/README.md'))
    # print(transfer_object_within_account(r'richardmtest/temp/readme2.md', r'timmtest/temp/README.md'))
    # print(generate_presigned_url(r'richardmtest/temp/'))
    # print(get_object_content(r'richardmtest/temp/README.md'))  # ["Body"].read())
    # print(delete_object('richardmtest/temp/README.md'))
    # print(delete_folder('richardmtest/temp'))
    # print(delete_bucket_objects("richardmtest"))
    # print(delete_bucket('richardmtest'))
    # print("done")
