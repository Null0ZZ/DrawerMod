# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import com
@Mod.Binding(name="Script_NeteaseModSrbaKU2A", version="0.0.1")
class Script_NeteaseModSrbaKU2A(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModSrbaKU2AServerInit(self):
        for key in com.serverSysKey:
            serverApi.RegisterSystem(com.modName,key,com.serverSysKey[key])
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModSrbaKU2AServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModSrbaKU2AClientInit(self):
        for key in com.clientSysKey:
            clientApi.RegisterSystem(com.modName,key,com.clientSysKey[key])
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModSrbaKU2AClientDestroy(self):
        pass
