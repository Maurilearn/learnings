import uuid

def file_prefix():
    filename = uuid.uuid4().hex
    return filename[:10]