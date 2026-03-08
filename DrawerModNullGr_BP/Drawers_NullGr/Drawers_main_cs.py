# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
llid = clientApi.GetLevelId()
import CMenthod as cm
import time
import random
EN = clientApi.GetEngineNamespace()
ESN = clientApi.GetEngineSystemName()
Enum = clientApi.GetMinecraftEnum()

compFactory = clientApi.GetEngineCompFactory()
comp_block  = clientApi.GetEngineCompFactory().CreateBlockInfo(llid)
comp_camera = clientApi.GetEngineCompFactory().CreateCamera(llid)
import com
from NullGr.client.NullgrClientSystem import NullgrClientSystem
from ClientRenderClass.BaseClass_RenderMoreClient import RenderBlockBaseMoreClient
class Drawers_nullgr_main_ClientSys(NullgrClientSystem):
    def __init__(self, namespace, systemName):
        super(Drawers_nullgr_main_ClientSys, self).__init__(namespace, systemName)
        listenDict = {
            'UiInitFinished':[self.UiInitFinished]
        }
        cm.ToListenEvent(self,listenDict)
        self.ListenSerToClient()
        self.molangInit()
    def ListenSerToClient(self):
        listenDict = {
            'playerMusic': [self.playerMusic],
            'playParticles': [self.playParticles],
            'setBlockMolangValue': [self.setBlockMolangValue],
            'setEntityMolangValue': [self.setEntityMolangValue],
            'setNeastPostProcess': [self.setNeastPostProcess],
        }
        cm.ToListenEvent(self, listenDict,com.modName, com.ssname)
        self.ListenForEvent(com.modName, com.ssname, 'RenderItemEntityClientRedner', self, self.RenderItemEntityClientRedner)
        self.ListenForEvent(com.modName, com.ssname, 'DestroyRenderEntity', self, self.DestroyRenderEntity)
    

    def RenderItemEntityClientRedner(self,a):
        slotList = a['slotList']
        rot = a['rot']
        dimId = a['dimId']
        pos = a['pos']
        renderBaseData = a['renderBaseData']
        clearEntityData = a.get('clearEntityData',None)
        renderClientObject = RenderBlockBaseMoreClient(dimId,pos)

        renderClientObject.RenderItemEntityClientRedner(slotList,rot,renderBaseData = renderBaseData,clearEntityData = clearEntityData)

    def DestroyRenderEntity(self,a):
        slotList = a['slotList']
        dimId = a['dimId']
        pos = a['pos']
        # clearEidList = a.get('clearEidList',[])
        renderClientObject = RenderBlockBaseMoreClient(dimId,pos)
        renderClientObject.DestroyRenderEntity(slotList)

    def molangInit(self):
        comp = clientApi.GetEngineCompFactory().CreateQueryVariable(llid)
        molang_dict = {
            'query.mod.xxxxx': 0.0,
        }
        for m in molang_dict:comp.Register(m, molang_dict[m])



    def UiInitFinished(self, a):
        #weapon_thnder_UI，ui_skill自行修改
        namespace = "weapon_thunder_UI"
        uiKey = "ui_skill"#ui唯一标识符
        clientApi.RegisterUI(namespace, uiKey, com.uiPath, "weapon_ui.main")
        self.uiNode = clientApi.CreateUI(namespace, uiKey, {"isHud": 1})

    # todo ----------------------------------------------------
    def playerMusic(self, a):
        music = a['music']
        pos = a['pos']
        volum = a['volume']
        p = a['p']
        loop = a['loop']
        cm.playMusic(music, pos, volum, p, loop)

    def setBlockMolangValue(self, a):
        dimId = a['dimId']
        pos = a['pos']
        molang = a['molang']
        value = a['value']
        comp_molang = compFactory.CreateBlockInfo(llid)
        comp_molang.SetBlockEntityMolangValue(pos, molang, value)

    def setEntityMolangValue(self, a):
        eid = a['eid']
        molang = a['molang']
        value = a['value']
        comp_molang = compFactory.CreateQueryVariable(eid)

        comp_molang.Set(molang, value)

    def playParticles(self, a):
        comp = clientApi.GetEngineCompFactory().CreateParticleSystem(llid)
        particleName = a['particleName']
        pos = a['pos']
        rotation = a['rotation']
        parId = comp.Create(particleName, pos, rotation)
        # print parId,a

    def setNeastPostProcess(self, a):
        postName = a['postName']
        isOpen = a['isOpen']
        postComp = clientApi.GetEngineCompFactory().CreatePostProcess(llid)
        print postComp.SetEnableByName(postName, isOpen)
        print a
    def Destroy(self):
        pass