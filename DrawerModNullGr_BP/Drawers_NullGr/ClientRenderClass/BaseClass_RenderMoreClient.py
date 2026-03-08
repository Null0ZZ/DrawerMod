# coding=utf-8
import copy
import math

import mod.client.extraClientApi as clientApi

compFactory = clientApi.GetEngineCompFactory()
levelId  = clientApi.GetLevelId()
import Drawers_NullGr.com as com
import render_data
# 还原二进制命名标签
def simplify_data_structure(data):
    # 如果输入是字典类型
    if isinstance(data, dict):
        # 检查是否是需要简化的特殊格式 {"__value__": value, "__type__": int}
        if "__value__" in data and "__type__" in data and len(data) == 2:
            return data["__value__"]

        # 对字典中的每个键值对递归处理
        simplified_dict = {}
        for key, value in data.items():
            simplified_dict[key] = simplify_data_structure(value)
        return simplified_dict
    # 如果输入是列表类型，对列表中的每个元素递归处理
    elif isinstance(data, list):
        return [simplify_data_structure(item) for item in data]
    # 其他类型保持不变
    else:
        return data



class RenderBlockBaseMoreClient():
    def __init__(self, dimId, pos):
        self.dimId = dimId
        self.pos = pos
        self.key_itemDataDict = 'render_itemDict_dict'
        self.key_render_id = 'render_entityId_dict'
        pass



    def data(self):
        comp = compFactory.CreateBlockInfo(levelId)
        re = comp.GetBlockEntityData(self.pos)
        return re

    def getRenderItemEntityDataDict(self):
        """
        返回渲染的物品字典
        """
        key = (self.pos[0],self.pos[1],self.pos[2],self.dimId)
        eidDataDict = render_data.render_id_data.get(key,{})
        return eidDataDict

    def setRenderItemEntityDataDict(self,eidDataDict):
        """
        设置渲染的物品字典
        """
        key = (self.pos[0],self.pos[1],self.pos[2],self.dimId)
        render_data.render_id_data[key] = eidDataDict


    def getRenderItemDataDict(self):
        """
        返回渲染的物品数据字典
        """
        data = self.data()
        if not data:return {}
        exData = data.get('exData')
        if not exData:return {}
        itemDataDictNbt = exData.get(self.key_itemDataDict,{})
        itemDataDict = simplify_data_structure(itemDataDictNbt)
        for slot in itemDataDict.keys():
            if isinstance(itemDataDict.get(slot),dict):
                itemDataDict[int(slot)] = itemDataDict.pop(slot)
            else:
                itemDataDict.pop(slot)

        return itemDataDict





    def RenderItemEntityClientRedner(self, slotList=None, rot=(0,0,0), cs=None,renderBaseData=None,clearEntityData = None):
        """
        客户端渲染，渲染后发送渲染结果给服务端

        """

        if cs is None:
            cs = clientApi.GetSystem(com.modName,com.csname)
            if not cs:return False
        key = (self.pos[0],self.pos[1],self.pos[2],self.dimId)
        # print '渲染id_0',render_data.render_id_data.get(key)
        if clearEntityData:
            if key in render_data.render_id_data:
                eids = render_data.render_id_data.pop(key)
                for slot in eids:
                    eid = eids[slot]
                    if not eid:continue
                    compFactory.CreateItem(levelId).DeleteClientDropItemEntity(eid)

        itemDataDict = self.getRenderItemDataDict()
        eidsDataDict = render_data.render_id_data.get(key,{})

        comp_item = compFactory.CreateItem(levelId)
        clientDropEidList = comp_item.GetClientDropItemEntityIdList()

        # 保存旧的物品数据用于比较是否发生变化
        key = (self.pos[0],self.pos[1],self.pos[2],self.dimId)
        oldItemDataDict = render_data.render_id_data.get(key + ('_itemData',), {})
        
        # print '客户端渲染',renderBaseData
        for slot in slotList:
            renderData = renderBaseData.get(slot)
            if not renderData:continue
            edpos = renderData.get('epos', (0, 0, 0))
            rotation = renderData.get('rotation', (0, 0, 0))
            dpos = renderData.get('dpos', (0, 0, 0))
            rotation = (rotation[0]+rot[0],rotation[1]+rot[1],rotation[2]+rot[2])
            pos_default = (self.pos[0]+edpos[0]+dpos[0],self.pos[1]+edpos[1]+dpos[1],self.pos[2]+edpos[2]+dpos[2])

            scale = renderData.get('scale', 1.0)
            item = itemDataDict.get(slot)
            eid = eidsDataDict.get(slot,'')
            oldItem = oldItemDataDict.get(slot)
            
            # print '渲染物品',slot,item,eid,eid in clientDropEidList
            if (not item or item['count'] <= 0): #and eid in clientDropEidList:
                re = comp_item.DeleteClientDropItemEntity(eid)
                if re:
                    # print 'deleted_id',eid
                    eidsDataDict.pop(slot)

                continue
            # 检查物品是否改变（比较物品名称和auxValue）
            elif item and oldItem and item.get('newItemName') == oldItem.get('newItemName') and item.get('newAuxValue') == oldItem.get('newAuxValue') and eid and eid in clientDropEidList:
                # 物品未改变，且实体仍存在，不需要重新创建
                pass
            elif item and (not eid or eid not in clientDropEidList):
                # 第一次创建实体或旧实体已失效
                renderItem = copy.deepcopy(item)
                renderItem['count'] = 1
                eid = comp_item.AddDropItemToWorld(renderItem,self.dimId,pos_default,bobSpeed=0,spinSpeed=0)

                if not eid:continue
                comp_item.SetDropItemTransform(eid, pos_default, rotation, scale)
                eidsDataDict[slot] = eid
            elif item and eid and eid in clientDropEidList:
                # 物品改变了，需要删除旧实体并创建新实体
                comp_item.DeleteClientDropItemEntity(eid)
                renderItem = copy.deepcopy(item)
                renderItem['count'] = 1
                newEid = comp_item.AddDropItemToWorld(renderItem,self.dimId,pos_default,bobSpeed=0,spinSpeed=0)
                if newEid:
                    comp_item.SetDropItemTransform(newEid, pos_default, rotation, scale)
                    eidsDataDict[slot] = newEid

        for slot in eidsDataDict:
            eid = eidsDataDict[slot]
            renderData = renderBaseData.get(slot)
            if not renderData: continue

            epos = renderData.get('epos', (0, 0, 0))
            rotation = renderData.get('rotation', (0, 0, 0))
            rotation = (rotation[0] + rot[0], rotation[1] + rot[1], rotation[2] + rot[2])
            dpos = renderData.get('dpos', (0, 0, 0))
            pos_default = (self.pos[0] + epos[0]+dpos[0], self.pos[1] + epos[1]+dpos[1], self.pos[2] + epos[2]+dpos[2])
            scale = renderData.get('scale', 1.0)
            re = comp_item.SetDropItemTransform(eid, pos_default, rotation, scale)
            if not re and isinstance(eid,str):
                comp_item.DeleteClientDropItemEntity(eid)

            # print pos_default
            # print comp_item.SetDropItemTransform('-9223372036854775732',pos_default,(0,0,0),2)



        pid = clientApi.GetLocalPlayerId()
        host_id = clientApi.GetHostPlayerId()
        key = (self.pos[0],self.pos[1],self.pos[2],self.dimId)
        render_data.render_id_data[key] = eidsDataDict
        # 保存物品数据缓存以便下次对比
        render_data.render_id_data[key + ('_itemData',)] = copy.deepcopy(itemDataDict)
        

        print '渲染id',eidsDataDict
        return True




    def DestroyRenderEntity(self,slotList=None,cs = None):
        """
        销毁渲染的实体
        """
        if cs is None:
            cs = clientApi.GetSystem(com.modName,com.csname)
            if not cs:return False

        if not slotList:return False
        comp_item = compFactory.CreateItem(levelId)

        clearEidList = self.getRenderItemEntityDataDict()
        allClientDropItem = comp_item.GetClientDropItemEntityIdList()
        for slot in slotList:
            eid = clearEidList.get(slot)
            if not eid:continue
            # if eid in allClientDropItem:
            re = comp_item.DeleteClientDropItemEntity(eid)
            if eid not in allClientDropItem or re :
                clearEidList.pop(slot)
        self.setRenderItemEntityDataDict(clearEidList)




        pid = clientApi.GetLocalPlayerId()
        host_id = clientApi.GetHostPlayerId()
        # if pid == host_id:
        #     #客户端通知服务端更新数据
        #     cs.NotifyToServer(
        #         eventName = 'DestroyRenderEntity',
        #         eventData = {
        #             'slotList':slotList,
        #             'dimId':self.dimId,
        #             'pos':self.pos,
        #         }
        #     )







