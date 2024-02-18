import os


class Config(object):
    AZURE_ACCOUNT = os.environ.get("AZURE_ACCOUNT")
    AZURE_STORAGE_KEY = os.environ.get("AZURE_STORAGE_KEY")
    AZURE_CONTAINER = os.environ.get("AZURE_CONTAINER")
