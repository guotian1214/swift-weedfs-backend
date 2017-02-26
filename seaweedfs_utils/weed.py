# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4


"""Main PySeaweed module. Contains WeedFS class
"""

import json
import os
import random
from collections import namedtuple

from exceptions import BadFidFormat
from utils import Connection


class WeedFS(object):
    master_addr = "localhost"
    master_port = 9333

    def __init__(self, master_addr='localhost', master_port=9333,
                 use_session=False):
        '''Creates WeedFS instance.

        Args:
            **master_addr**: Address of weed-fs master server
                             (default: localhost)

            **master_port**: Weed-fs master server port (default: 9333)
            **use_session**: Use request.Session() for connections instead of
                             requests themselves. (default: False)

        Returns:
            WeedFS instance.
        '''
        self.master_addr = master_addr
        self.master_port = master_port
        self.conn = Connection(use_session)

    def __repr__(self):
        return "<{0} {1}:{2}>".format(
            self.__class__.__name__,
            self.master_addr,
            self.master_port
        )

    def get_file(self, url):
        """Get file from WeedFS.

        Returns file content. May be problematic for large files as content is
        stored in memory.

        Args:
            **fid**: File identifier <volume_id>,<file_name_hash>

        Returns:
            Content of the file with provided fid or None if file doesn't
            exist on the server

        .. versionadded:: 0.3.1
        """
        # url = self.get_file_url(fid)
        return self.conn.get_raw_data(url)

    def get_file_location(self, volume_id):
        """
        Get location for the file,
        WeedFS volume is choosed randomly

        :param integer volume_id: volume_id
        :rtype: namedtuple `FileLocation` `{"public_url":"", "url":""}`
        """
        url = ("http://{master_addr}:{master_port}/"
               "dir/lookup?volumeId={volume_id}").format(
            master_addr=self.master_addr,
            master_port=self.master_port,
            volume_id=volume_id)
        data = json.loads(self.conn.get_data(url))
        _file_location = random.choice(data['locations'])
        FileLocation = namedtuple('FileLocation', "public_url url")
        return FileLocation(_file_location['publicUrl'], _file_location['url'])

    def get_file_size(self, url):
        """
        Gets size of uploaded file
        Or None if file doesn't exist.

        Args:
            **fid**: File identifier <volume_id>,<file_name_hash>

        Returns:
            Int or None
        """
        # url = self.get_file_url(fid)
        res = self.conn.head(url)
        if res is not None:
            size = res.headers.get("content-length", None)
            if size is not None:
                return int(size)
        return None

    def file_exists(self, url):
        """Checks if file with provided fid exists

        Args:
            **fid**: File identifier <volume_id>,<file_name_hash>

        Returns:
            True if file exists. False if not.
        """
        res = self.get_file_size(url)
        if res is not None:
            return True
        return False

    def delete_file(self, url):
        """
        Delete file from WeedFS

        :param string fid: File ID
        """
        # url = self.get_file_url(fid)
        return self.conn.delete_data(url)

    def upload_file(self,url,obj_name,obj_content):
        """
        Uploads file to WeedFS

        I takes either path or stream and name and upload it
        to WeedFS server.

        Returns fid of the uploaded file.

        :param string path:
        :param string stream:
        :param string name:
        :rtype: string or None

        """
        res = self.conn.post_file(url, obj_name, obj_content)
        response_data = json.loads(res)
        if "size" in response_data:
            return response_data.get('size')
        return None

    def vacuum(self, threshold=0.3):
        '''
        Force garbage collection

        :param float threshold (optional): The threshold is optional, and
        will not change the default threshold.
        :rtype: boolean

        '''
        url = ("http://{master_addr}:{master_port}/"
               "vol/vacuum?garbageThreshold={threshold}").format(
            master_addr=self.master_addr,
            master_port=self.master_port,
            threshold=threshold)
        res = self.conn.get_data(url)
        if res is not None:
            return True
        return False

    @property
    def version(self):
        '''
        Returns Weed-FS master version

        :rtype: string
        '''
        url = "http://{master_addr}:{master_port}/dir/status".format(
            master_addr=self.master_addr,
            master_port=self.master_port)
        data = self.conn.get_data(url)
        response_data = json.loads(data)
        return response_data.get("Version")


if __name__ == "__main__":
    pass
