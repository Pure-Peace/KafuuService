# -*- coding: utf-8 -*-
'''
@author: PurePeace
@version: 0.2
@date: 2020-4-16

DllLoader nice
'''

from clr import AddReference
from SystemHandler import base_path


AddReference(base_path('static\System.Security.dll'))
from System.Security.Cryptography.X509Certificates import (
    StoreName,
    StoreLocation,
    OpenFlags,
    X509Store,
    X509FindType,
    X509Certificate2
)

