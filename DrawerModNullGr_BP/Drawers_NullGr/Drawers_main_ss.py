# -*- coding: utf-8 -*-
import time
import math
import SMethod as sm
import com
import mod.server.extraServerApi as serverApi
import NullGr.server.Level as Level
import NullGr.server.Player as Player
from NullGr.server.NullgrServerSystem import NullgrServerSystem
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
EN = serverApi.GetEngineNamespace()
ESN = serverApi.GetEngineSystemName()
Enum = serverApi.GetMinecraftEnum()
class Drawers_nullgr_main_ServerSys(NullgrServerSystem):
    def __init__(self, namespace, systemName):
        super(Drawers_nullgr_main_ServerSys, self).__init__(namespace, systemName)
        listenDict = {

        }
        sm.ToListenEvent(self,listenDict)
        print "server yes"
        self.ListenCliToServer()
    def ListenCliToServer(self):
        listenDict = {

        }
        sm.ToListenEvent(self, listenDict,com.modName,com.csname)
        print "ListenCliToServer Great!!!"




    def Destroy(self):
        pass