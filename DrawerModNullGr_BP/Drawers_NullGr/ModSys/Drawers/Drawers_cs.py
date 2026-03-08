# -*- coding: utf-8 -*-
"""
抽屉模块 - 客户端系统
预留，当前客户端渲染由主系统 Drawers_main_cs 统一处理
未来可扩展：
- 抽屉专属UI
- 点击特效
- 声音播放
"""
import mod.client.extraClientApi as clientApi
import Drawers_NullGr.CMenthod as cm
import Drawers_NullGr.com as com
from Drawers_NullGr.NullGr.client.NullgrClientSystem import NullgrClientSystem
import config

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()
llid = clientApi.GetLevelId()


class Drawers_ClientSys(NullgrClientSystem):
    """抽屉模块客户端系统（预留）"""
    
    def __init__(self, namespace, systemName):
        super(Drawers_ClientSys, self).__init__(namespace, systemName)
        
        listenDict = {
            # 预留事件监听
        }
        cm.ToListenEvent(self, listenDict)
        
        self.ListenSerToClient()
    
    def ListenSerToClient(self):
        """注册服务端到客户端的消息监听"""
        listenDict = {
            # 预留消息监听
        }
        cm.ToListenEvent(self, listenDict, com.modName, com.ssname)
    
    def Destroy(self):
        """系统销毁"""
        pass
