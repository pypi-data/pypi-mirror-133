def get_bucket_and_key(s3_url):
    s3_url = s3_url.split("/") if s3_url else s3_url
    return {
        "bucket": s3_url[2],
        "key": '/'.join(s3_url[3:])
    } if s3_url else None


def get_s3_url(p_args):
    for arg in p_args:
        if 's3://' in arg:
            return arg


def get_recursive_file(p_args):
    return p_args[2]
