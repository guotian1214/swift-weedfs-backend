from seaweedfs_utils.weed import WeedFS
class Seaweedfs_operation():
    def __init__(self):
        self.seaweedfs = WeedFS();
        self.filter_ip = "127.0.0.1"
        self.filter_port = "8888"
    def PUT(self,url, obj_content):
        """
        upload file to seaweedfs
        :param url:
        :param obj_content:
        :return: obj size
        """
        account,container,obj_name = self.parseURL(url)
        url_complete = u"http://{filter_ip}:{filter_port}/{account}/{container}/".format(filter_ip=self.filter_ip,
                                                                                         filter_port=self.filter_port,
                                                                                         account=account,container=container)
        return self.seaweedfs.upload_file(url_complete,obj_name,obj_content)

    def DELETE(self,url):
        """
        delete a file from seaweedfs
        :param url:
        :return: Boolean: True:delete success
        """
        url_complete = u"http://{filter_ip}:{filter_port}{url}".format(filter_ip=self.filter_ip,
                                                                       filter_port=self.filter_port,url=url)
        return self.seaweedfs.delete_file(url_complete)

    def GET(self,url):
        """
        download a file from seaweedfs
        :param url:
        :return:
            Content of the file with provided url or None if file doesn't
                exist on the server
        """
        url_complete = "http://{filter_ip}:{filter_port}{url}".format(filter_ip=self.filter_ip,
                                                                      filter_port=self.filter_port,url=url)
        return self.seaweedfs.get_file(url_complete)

    def parseURL(self,url):
        """
        parse url to account, container, obj_name
        :param url:
        :return: account, container, obj_name
        """
        url_split = url.split('/')
        return url_split[1],url_split[2],url_split[3]

# if __name__ == '__main__':
#     test = Seaweedfs_operation()
#     account = u"AUTH_test"
#     container = u"memtest"
#     obj_name = u"aaaaa.txt"
#     obj_content = u"12345678901234567890"
#     url = "/AUTH_test/memtest/aaaaa.txt"
#     import StringIO
#     obj = StringIO.StringIO("test111")
#     obj.seek(0,2)
#     metadata = {'a':'a1','b':'b1'}
#     obj.write('\n' + str(metadata))
#     obj.seek(0)
#     # test.PUT(url,obj.read())   #pass
#     # test111 = test.GET(url)   # pass
#     # print test111
#     # print test.DELETE(url)
#     test111 = test.GET(url)   # pass
#     print test111
# # #     print test.GET(account,container,obj_name)
# #     print test111.rfind("\n")