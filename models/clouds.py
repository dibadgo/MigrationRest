from enum import Enum


class CloudType(str, Enum):
    """The supported cloud type definition"""

    AWS = 'aws'
    AZURE = 'azure'
    VSPHERE = 'vsphere'
    VCLOUD = 'vcloud'