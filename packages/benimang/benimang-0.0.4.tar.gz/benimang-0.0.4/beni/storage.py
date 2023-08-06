from typing import Any

import yaml

from beni import list_file, remove, writefile_text
from beni.internal import getStorageFile, storagePath


def getstorage(key: str, default: Any = None):
    storageFile = getStorageFile(key)
    if storageFile.is_file():
        content = storageFile.read_text()
        return yaml.safe_load(content)
    else:
        return default


def setstorage(key: str, value: Any):
    storageFile = getStorageFile(key)
    content = yaml.safe_dump(value)
    return writefile_text(storageFile, content)


def clearStorage(*keyList: str):
    for key in keyList:
        storageFile = getStorageFile(key)
        remove(storageFile)


def clearAllStorage():
    for storageFile in list_file(storagePath):
        remove(storageFile)
