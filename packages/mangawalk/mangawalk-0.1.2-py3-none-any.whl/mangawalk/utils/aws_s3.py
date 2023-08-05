import os

def s3_upload(s3_client, local_fullpath, bucket, prefix):
    """[summary]

    Args:
        s3_client ([type]): [description]
        local_fullpath ([type]): [description]
        bucket ([type]): [description]
        prefix ([type]): [description]

    Returns:
        [type]: [description]
    """
    s3_client.upload_file(local_fullpath, bucket, prefix)
    os.remove(local_fullpath)
    return f"s3://{bucket}/{prefix}"