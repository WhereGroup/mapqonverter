import os
import binascii


class LayoutUuidProvider:
    uuid_dict = {}

    def __init__(self):
        pass

    @staticmethod
    def create_uuid(object_name):
        """
        This function creates a Unique ID and writes it in the dictionary connected with the name of the object 
        :param object_name: the name of the object
        """
        uuid = '{}-{}-{}-{}'.format(
            binascii.b2a_hex(os.urandom(4)),
            binascii.b2a_hex(os.urandom(2)),
            binascii.b2a_hex(os.urandom(2)),
            binascii.b2a_hex(os.urandom(6)),
        )
        LayoutUuidProvider.uuid_dict[object_name] = uuid
