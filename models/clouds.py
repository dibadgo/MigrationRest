from enum import Enum


class CloudType(Enum):
    """The supported cloud type definition"""

    AWS = 'aws'
    AZURE = 'azure'
    VSPHERE = 'vsphere'
    VCLOUD = 'vcloud'