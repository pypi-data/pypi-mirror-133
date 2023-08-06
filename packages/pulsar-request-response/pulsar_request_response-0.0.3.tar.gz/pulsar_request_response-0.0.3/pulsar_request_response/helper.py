#!/usr/bin/env python
# coding: utf-8

class Helper(object):
    """
    辅助基类模块
    """

    def __init__(self):
        self._config = dict()


        self._partition = 0
        # 发送消息的状态，True 是成功发送，False 是发送失败
        self._send_error = None
        self._send_msg = None

    def config_servers(self, url:str):
        """
        配置连接的服务器,如['localhost:9092']
        """
        self._config["url"] = f'pulsar://{url}'
        return self

    def config_tenant(self, tenant:str):
        """ 配置租户 """
        self._config["tenant"] = tenant
        return self

    def config_namespace(self, namespace:str):
        """ 配置命名空间 """
        self._config["namespace"] = namespace
        return self
