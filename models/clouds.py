from enum import Enum


class CloudType(Enum):
    AWS = 'aws'
    AZURE = 'azure'
    VSPHERE = 'vsphere'
    VCLOUD = 'vcloud'