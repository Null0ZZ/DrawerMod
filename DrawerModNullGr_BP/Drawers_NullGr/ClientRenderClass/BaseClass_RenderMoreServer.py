# -*- coding: utf-8 -*-
"""
全新的客户端渲染物品类
解决服务端卡顿问题，但不适用于有动画的物品渲染
"""
import copy
import threading
import time
import math
import mod.server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
import Drawers_NullGr.SMethod as sm
import Drawers_NullGr.com as com
EN = serverApi.GetEngineNamespace()
ESN = serverApi.GetEngineSystemName()
Enum = serverApi.GetMinecraftEnum()
import Drawers_NullGr.NullGr.server.Level as Level
import Drawers_NullGr.NullGr.server.Player as Player

renderTypes = {
    'minecraft:beetroot':0.0,
    'minecraft:wheat':0.0,
    'minecraft:cake':0.0,
    'minecraft:bone_meal':0.0,


}
class RenderBlockBaseMoreServer():
    """
    拥有渲染物品功能的方块基类
    客户端版本
    """

    def __init__(self,dimId,pos):
        self.dimId  = dimId
        self.pos = pos
        self.key_itemDataDict = 'render_itemDict_dict'
        self.key_render_id = 'render_entityId_dict'


    def data(self):#type:()->dict
        """
        返回blockEntity
        """
        return Level.BlockEntity.GetBlockEntityData(self.dimId,self.pos) # type: ignore

    def getSize(self):
        """
        返回渲染的最大位置数量
        defalut:6
        """
        return 6


    def getRenderItemDataDict(self):#type:()->dict
        """
        返回记录的渲染物品信息
        return dict
        dict = {
        slot : itemDict
        }
        """
        data = self.data()
        if not data:return {}
        re = data[self.key_itemDataDict]
        if re is None:return {}
        for slot in re.keys(): # type: ignore
            re[int(slot)] = re.pop(slot) # type: ignore
            if isinstance(re[int(slot)],dict):
                listModEnchantData =re[int(slot)].get('enchantData',[])
                ModEnchantData = [tuple(v) for v in listModEnchantData]
                re[int(slot)]['enchantData'] = ModEnchantData
        return re

    def setRenderItemDataDict(self,itemDataDict,autoRender = True,renderBaseData = None):
        """
        记录的渲染物品信息
        return Bool
        itemDataDict = {
        slot : itemDict
        ...
        }
        """
        data = self.data()
        if not data:return False
        if itemDataDict is None:itemDataDict = {}
        DataDict = copy.deepcopy(itemDataDict)
        
        for slot in DataDict.keys():
            DataDict[str(slot)] = DataDict.pop(slot)
            if isinstance(DataDict[str(slot)],dict):
                modEnchantData = DataDict[(str(slot))].get('enchantData',[])
                listModEnchantData = [list(v) for v in modEnchantData]
                DataDict[str(slot)]['enchantData'] = listModEnchantData
            
        data[self.key_itemDataDict] = DataDict

        # self.DestroyRenderEntity(d_slot)
        if autoRender:
            self.RenderItemEntity(renderBaseData=renderBaseData)


        return True

#废弃，实体记录数据无需存档
    def getRenderItemEntityDataDict(self):
        """
        返回渲染的实体id
        return dict
        dict = {
        slot : eid
        }
        """

        data = self.data()
        if not data:return {}
        re = data[self.key_render_id]
        if not re:return {}
        for slot in re.keys(): # type: ignore
            re[int(slot)] = re.pop(slot) # type: ignore

        return re

#废弃
    def setRenderItemEntityDataDict(self,EntityDataDict):
        """
        设置渲染的实体id
        return Bool
        EntityDataDict = {
        slot : eid
        }
        """
        data = self.data()
        if not data:return False
        DataDict = copy.deepcopy(EntityDataDict)
        for slot in DataDict.keys():
            DataDict[str(slot)] = DataDict.pop(slot)
        data[self.key_render_id] = DataDict
        return True


    def getRotRenderItemEntityFromAux(self,blockAux):
        """
        getRot
        """
        rot_dict = {2: (0, 0,90), 0: (0, 0,-90), 1: (0, 0,0), 3: (0, 0,-180)}
        return rot_dict.get(blockAux, (0, 0,0))
    
    
    def getRenderBaseData(self):
        """
        ---&&区别于旧的渲染类，新增$rotation旋转字段
        返回渲染的基础信息字典
        return:dict
        slot:{
                'epos':(0,0,0),'rotation':(0,0,0),'scale':1.0
            },
        """
        re = {
            0: {
                'epos': (0.5, 0.5, 0.5), 'scale': 1.0, 'rotation': (0, 0, 0),'dpos':(-0.5,-0.5,0)
            },
            1: {
                'epos':  (0.5, 0.5, 0.5), 'scale': 1.0, 'rotation': (0, 0, 0),'dpos':(1,-0.5,0)
            },
            2: {
                'epos':  (0.5, 0.5, 0.5), 'scale': 1.0, 'rotation': (0, 0, 0),'dpos':(-0.5,0,0)
            },
            3: {
                'epos':  (0.5, 0.5, 0.5), 'scale': 1.0, 'rotation': (0, 0, 0),'dpos':(1,0,0)
            },
            4: {
                'epos':  (0.5, 0.5, 0.5), 'scale': 1.0, 'rotation': (0, 0, 0),'dpos':(-0.5,1,0)
            },
            5: {
                'epos':  (0.5, 0.5, 0.5), 'scale': 1.0, 'rotation': (0, 0, 0),'dpos':(1,1,0)
            }
        }
        return re


    def RenderItemEntity(self, slotList=None,rot = None,ss = None,clearEntityData = None,client_id = None,renderBaseData = None):
        """
        渲染实体
        slot : list[int] 渲染哪些格子,默认 【0】
        return : bool
        """
        if slotList is None:
            slotList = range(self.getSize())
        if not ss:ss = serverApi.GetSystem(com.modName,com.ssname)
        state = Level.BlockState.GetBlockStates(self.pos, self.dimId)
        direction = state['direction']
        block_aux = Level.BlockInfo.GetBlockNew(self.pos, self.dimId)['aux']
        block_aux = direction

        if rot is None:
            rot = self.getRotRenderItemEntityFromAux(block_aux)
            # print rot
        if not renderBaseData:
            renderBaseData = self.getRenderBaseData()
        if client_id:
            ss.NotifyToClient(client_id,'RenderItemEntityClientRedner',
                                {
                                    'slotList':slotList,
                                    'rot':rot,
                                    'dimId':self.dimId,
                                    'pos':self.pos,
                                    'renderBaseData':renderBaseData,
                                    'clearEntityData':clearEntityData
                                })
        else:
            ss.BroadcastToAllClient('RenderItemEntityClientRedner',
                                    {
                                        'slotList':slotList,
                                        'rot':rot,
                                        'dimId':self.dimId,
                                        'pos':self.pos,
                                        'renderBaseData':renderBaseData,
                                        'clearEntityData':clearEntityData
                                    })


    def DestroyRenderEntity(self,slotList = [0],ss = None):
        """
        清除摸个被已经渲染的实体
        将eid -> None
        ss目前仅能为主系统，所以只能填None
        """

        if not isinstance(slotList,list):return False
        if not ss: ss = serverApi.GetSystem(com.modName, com.ssname)
        # clearEidList = self.getRenderItemEntityDataDict()

        ss.BroadcastToAllClient(
            'DestroyRenderEntity',
            {
                'slotList':slotList,
                'dimId':self.dimId,
                'pos':self.pos,
                # 'clearEidList':clearEidList
            }
        )


    #todo:------------------

    def getClickedSlot(self, clickx, clicky, clickz, face):
        """
        通过点击坐标和点击方位，判断点击了哪个格子，返回格子index或None
        抽象方法，具体实现由子类实现
        :param clickx: float 点击的相对坐标x (0~1)
        :param clicky: float 点击的相对坐标y (0~1)
        :param clickz: float 点击的相对坐标z (0~1)
        :param face: int 点击的方位
        :return: int or None
        """
        pass

    def findFirstSlot(self, findType='isEmpty', slotStart=None, slotEnd=None):
        """
        按顺序返回范围内第一个满足条件的格子
        :param findType: 'isItem' 返回第一个有物品的格子, 'isEmpty' 返回第一个空格子
        :param slotStart: 查找起始格子(含)，默认为 0
        :param slotEnd: 查找结束格子(含)，默认为 getSize()-1
        :return: int or None
        """
        if slotStart is None:
            slotStart = 0
        if slotEnd is None:
            slotEnd = self.getSize() - 1
        itemDict = self.getRenderItemDataDict()
        for slot in range(slotStart, slotEnd + 1):
            hasItem = slot in itemDict and itemDict[slot] is not None
            if findType == 'isItem' and hasItem:
                return slot
            if findType == 'isEmpty' and not hasItem:
                return slot
        return None

    def findLastSlot(self, findType='isItem', slotStart=None, slotEnd=None):
        """
        按逆序返回范围内第一个满足条件的格子
        :param findType: 'isItem' 返回最后一个有物品的格子, 'isEmpty' 返回最后一个空格子
        :param slotStart: 查找起始格子(含)，默认为 0
        :param slotEnd: 查找结束格子(含)，默认为 getSize()-1
        :return: int or None
        """
        if slotStart is None:
            slotStart = 0
        if slotEnd is None:
            slotEnd = self.getSize() - 1
        itemDict = self.getRenderItemDataDict()
        for slot in range(slotEnd, slotStart - 1, -1):
            hasItem = slot in itemDict and itemDict[slot] is not None
            if findType == 'isItem' and hasItem:
                return slot
            if findType == 'isEmpty' and not hasItem:
                return slot
        return None

    














