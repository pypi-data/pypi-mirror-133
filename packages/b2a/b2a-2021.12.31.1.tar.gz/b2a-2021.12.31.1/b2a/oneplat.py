# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# @File    :  oneplat.py
# @Date    :  2021/06/17
# @Author  :  Yaronzz
# @Version :  1.0
# @Contact :  yaronhuang@foxmail.com
# @Desc    :
# """
# import io
# import json
# import math
# import os
# import pickle
# import sys
# import time
# from typing import List
# from xml.dom.minidom import parseString

# import aigpy
# import oauthlib
# import requests

# from b2a.downloader import Downloader
# from b2a.platformImp import FileAttr
# from requests_oauthlib import OAuth2Session

# from b2a import PlatformImp, printErr


# class OnedriveKey(object):
#     def __init__(self):
#         super().__init__()
#         self.api = None
#         self.cookies = ''
#         self.root_uri = "https://microsoftgraph.chinacloudapi.cn/v1.0" + "/me/drive/root"

#     def login(self, cookiesStr: str) -> bool:
#         try:
#             # cookies = dict()
#             # array = cookiesStr.split(';')
#             # for item in array:
#             #     values = item.split('=')
#             #     cookies[values[0].strip(' ')] = values[1]
#             # self.api = BaiduPCSApi(bduss=cookies['BDUSS'], cookies=cookies)
#             # self.cookies = cookiesStr
#             return True
#         except:
#             return False

#     # 取目录路径
#     def get_path(self, path):
#         sep = ":"
#         if path == '/': path = ''
#         if path[-1:] == '/':
#             path = path[:-1]
#         if path[:1] != "/" and path[:1] != sep:
#             path = "/" + path
#         if path == '/': path = ''
#         # if path[:1] != sep:
#         #     path = sep + path
#         try:
#             from urllib.parse import quote
#         except:
#             from urllib import quote
#         # path = quote(path)

#         return path.replace('//', '/')

#     def build_uri(self, path="", operate=None, base=None):
#         """构建请求URL

#         API请求URI格式参考:
#             https://graph.microsoft.com/v1.0/me/drive/root:/bt_backup/:content
#             ---------------------------------------------  ---------- --------
#                                   base                        path    operate
#         各部分之间用“：”连接。
#         :param path 子资源路径
#         :param operate 对文件进行的操作，比如content,children
#         :return 请求url
#         """

#         if base is None:
#             base = self.root_uri
#         path = self.get_path(path)
#         sep = ":"
#         if operate:
#             if operate[:1] != "/":
#                 operate = "/" + operate

#         if path:
#             uri = base + sep + path
#             if operate:
#                 uri += sep + operate
#         else:
#             uri = base
#             if operate:
#                 uri += operate

#         return uri

#     def list(self, remotePath: str) -> List[FileAttr]:
#         path = remotePath.rstrip('/')

#         list_uri = self.build_uri(path, operate="/children")

#         data = []
#         response = requests.get(list_uri, headers=self.get_authorized_header())
#         status_code = response.status_code
#         if status_code == 200:
#             if DEBUG:
#                 print("DEBUG:")
#                 print(response.json())
#             response_data = response.json()
#             drive_items = response_data["value"]

#             for item in drive_items:
#                 tmp = {}
#                 tmp['name'] = item["name"]
#                 tmp['size'] = item["size"]
#                 if "folder" in item:
#                     # print("{} is folder:".format(item["name"]))
#                     # print(item["folder"])
#                     tmp["type"] = None
#                     tmp['download'] = "";
#                 if "file" in item:
#                     tmp["type"] = "File"
#                     tmp['download'] = item["@microsoft.graph.downloadUrl"];
#                     # print("{} is file:".format(item["name"]))
#                     # print(item["file"])

#                 formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
#                 t = None
#                 for time_format in formats:
#                     try:
#                         t = datetime.datetime.strptime(
#                             item["lastModifiedDateTime"], time_format)
#                         break
#                     except:
#                         continue
#                 t += datetime.timedelta(hours=8)
#                 ts = int(
#                     (time.mktime(t.timetuple()) + t.microsecond / 1000000.0))
#                 tmp['time'] = ts
#                 data.append(tmp)

#         mlist = {'path': path, 'list': data}
#         return mlist


#         sid = self.__getPathId__(remotePath)
#         if not sid:
#             return []

#         try:
#             requests_data = {"drive_id": self.driveId, "parent_file_id": sid, 'marker': nextMarker, 'limit': 100}
#             requests_post = requests.post('https://api.aliyundrive.com/v2/file/list',
#                                           data=json.dumps(requests_data),
#                                           headers=self.headers,
#                                           verify=False).json()
#             ret = []
#             for item in requests_post['items']:
#                 obj = FileAttr()
#                 obj.isfile = item['type'] != 'folder'
#                 obj.name = item['name']
#                 obj.path = remotePath + '/' + item['name']
#                 obj.uid = item['file_id']
#                 obj.size = item['size'] if 'size' in item else 0
#                 if not obj.isfile:
#                     self.__updatePathId__(obj.path, obj.uid)

#                 ret.append(obj)

#             next_marker = requests_post.get('next_marker')
#             if next_marker and nextMarker != requests_post['next_marker']:
#                 ret.extend(self.list(remotePath, next_marker))

#             return ret
#         except Exception as e:
#             printErr("获取目录文件列表失败：" + str(e))
#             return []


# class OnedrivePlat(PlatformImp):
#     def __init__(self):
#         super().__init__()

#     def __safeAPI__(self, method, para):
#         retry = 10
#         while retry > 0:
#             try:
#                 if method == 'list':
#                     return self.key.api.list(para)
#                 elif method == 'download_link':
#                     return self.key.api.download_link(para)
#                 elif method == 'is_file':
#                     return self.key.api.is_file(para)
#                 elif method == 'file_stream':
#                     return self.key.api.file_stream(para)
#             except:
#                 printErr("重新尝试获取：BdyPlat " + method)
#                 retry -= 1
#         return None

#     def list(self, remotePath: str, includeSubDir: bool = False) -> List[FileAttr]:
#         array = []
#         if len(remotePath) <= 0:
#             remotePath = '/'

#         res = self.__safeAPI__('list', remotePath)
#         for item in res:
#             obj = FileAttr()
#             obj.isfile = item.is_file
#             obj.name = aigpy.path.getFileName(item.path)
#             obj.path = item.path
#             obj.size = item.size
#             obj.uid = item.fs_id
#             array.append(obj)

#             if includeSubDir and item.is_dir:
#                 subList = self.list(item.path, includeSubDir)
#                 array.extend(subList)
#         return array

#     def downloadFile(self, fileAttr: FileAttr, localFilePath: str) -> bool:
#         path = aigpy.path.getDirName(localFilePath)
#         name = aigpy.path.getFileName(localFilePath)
#         check = aigpy.path.mkdirs(path)

#         # stream = self.__safeAPI__('file_stream', fileAttr.path)
#         # if not stream:
#         #     return False
#         #
#         # curSize = 0
#         # part = 1024 * 1024 * 1
#         # totalSize = len(stream)
#         # with open(localFilePath, 'wb+') as f:
#         #     with tqdm.wrapattr(stream, "read", desc='下载中', miniters=1, total=totalSize, ascii=True) as fs:
#         #         while True:
#         #             data = fs.read(part)
#         #             f.write(data)
#         #             curSize += len(data)
#         #             if curSize >= totalSize:
#         #                 break
#         #
#         # stream.close()
#         # return True

#         headers = {
#             "Cookie ": "; ".join(
#                 [f"{k}={v if v is not None else ''}" for k, v in self.key.api.cookies.items()]
#             ),
#             "User-Agent": "netdisk;2.2.51.6;netdisk;10.0.63;PC;android-android",
#             "Connection": "Keep-Alive",
#         }

#         link = self.__safeAPI__('download_link', fileAttr.path)
#         if not link or len(link) <= 0:
#             return False

#         dl = Downloader(link, headers, localFilePath, fileAttr.size, 6)
#         check = dl.run()
#         return check

#     def uploadFile(self, localFilePath: str, remoteFilePath: str) -> bool:
#         return False

#     def downloadLink(self, remoteFilePath: str):
#         link = self.__safeAPI__('download_link', remoteFilePath)
#         return link

#     def uploadLink(self, localFilePath: str, remoteFilePath: str):
#         return None

#     def isFileExist(self, remoteFilePath: str) -> bool:
#         return self.__safeAPI__('is_file', remoteFilePath)
