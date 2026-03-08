# -*- coding: utf-8 -*-
"""
抽屉模块 - 服务端事件监听
处理方块放置、交互、破坏等事件
"""
import time
import copy
import mod.server.extraServerApi as serverApi
import Drawers_NullGr.SMethod as sm
import Drawers_NullGr.com as com
import Drawers_NullGr.NullGr.server.Level as Level
import Drawers_NullGr.NullGr.server.Player as Player
from Drawers_NullGr.NullGr.server.NullgrServerSystem import NullgrServerSystem
from Drawers import Drawers
import config

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()
EN = serverApi.GetEngineNamespace()
ESN = serverApi.GetEngineSystemName()
Enum = serverApi.GetMinecraftEnum()


def _newDrawers(dimId, pos):
    """
    工厂函数：创建 Drawers 实例
    :param dimId: 维度ID
    :param pos: 坐标元组
    :return: Drawers 实例
    """
    return Drawers(dimId, pos)


class Drawers_ServerSys(NullgrServerSystem):
    """抽屉模块服务端系统"""
    
    def __init__(self, namespace, systemName):
        super(Drawers_ServerSys, self).__init__(namespace, systemName)
        
        # 注册事件监听
        listenDict = {
            "ServerPlaceBlockEntityEvent": [self.ServerPlaceBlockEntityEvent],
            "ServerItemUseOnEvent": [self.ServerItemUseOnEvent],
            "ServerBlockUseEvent": [self.ServerBlockUseEvent],
            "BlockRemoveServerEvent": [self.BlockRemoveServerEvent],
        }
        sm.ToListenEvent(self, listenDict)
        
        # 监听客户端消息
        self.ListenCliToServer()
        
        # 防双击时间记录
        self.useTimeDict = {}
        self.itemUseTimeDict = {}
    
    def ListenCliToServer(self):
        """注册客户端到服务端的消息监听"""
        listenDict = {
            'ModBlockEntityLoadedClientEvent': [self.ModBlockEntityLoadedClientEvent],
        }
        sm.ToListenEvent(self, listenDict, com.modName, com.csname)
    
    # ─── 方块放置 ─────────────────────────────────────────────────────────────
    
    def ServerPlaceBlockEntityEvent(self, args):
        """
        方块放置时初始化 BlockEntity 数据
        """
        blockName = args.get('blockName', '')
        dimension = args.get('dimension', 0)
        x = args.get('posX', 0)
        y = args.get('posY', 0)
        z = args.get('posZ', 0)
        
        if blockName not in config.drawersData:
            return
        
        data = Level.BlockEntity.GetBlockEntityData(dimension, (x, y, z))
        if not data:
            return
        
        cfg = config.drawersData[blockName]
        
        # 初始化数据结构（兼容旧存档）
        data['drawersDataDict'] = {}
        data['chestDataDict'] = {}
        data['maxNum'] = cfg.get('baseVolume', 2048)
        data['isLocked'] = False
        data['user'] = None
        data['isShowCount'] = True
        data['isShowPro'] = True
        data['shroud'] = False
        data['render_itemDict_dict'] = {}
    
    # ─── 客户端加载 BlockEntity ────────────────────────────────────────────────
    
    def ModBlockEntityLoadedClientEvent(self, args):
        """
        客户端加载 BlockEntity 时刷新渲染
        """
        blockName = args.get('blockName', '')
        x = args.get('posX', 0)
        y = args.get('posY', 0)
        z = args.get('posZ', 0)
        dimensionId = args.get('dimensionId', 0)
        clientId = args.get('__id__', None)
        
        if blockName not in config.drawersData:
            return
        
        drawer = _newDrawers(dimensionId, (x, y, z))
        drawer.syncRenderData()
        drawer.RenderItemEntity(clearEntityData=True, client_id=clientId)
    
    # ─── 手持物品右键方块（存入物品）────────────────────────────────────────────
    
    def ServerItemUseOnEvent(self, args):
        """
        手持物品右键抽屉：存入物品
        只响应正面点击
        """
        x = args['x']
        y = args['y']
        z = args['z']
        dimensionId = args['dimensionId']
        entityId = args['entityId']
        itemDict = args['itemDict']
        blockName = args['blockName']
        face = args['face']
        clickX = float(args['clickX'])
        clickY = float(args['clickY'])
        clickZ = float(args['clickZ'])
        
        if blockName not in config.drawersData:
            return
        
        if not itemDict or not itemDict.get('newItemName'):
            return
        
        drawer = _newDrawers(dimensionId, (x, y, z))
        
        # 检查是否点击正面
        if not drawer.isFrontFace(face):
            return
        
        # 防双击
        key = (x, y, z, dimensionId)
        if key not in self.itemUseTimeDict:
            self.itemUseTimeDict[key] = 0
        if time.time() - self.itemUseTimeDict[key] < config.PC_TIME_CLICK:
            return
        self.itemUseTimeDict[key] = time.time()
        
        # 潜行时不触发
        if Player.PlayerComp(entityId).isSneaking():
            return
        
        # 检查私有权限
        if drawer.isPrivateDrawers():
            ownerId = drawer.getPrivateDrawersUserId()
            if ownerId != entityId:
                return
        
        # 获取点击的格子（getClickedSlot 只在正面才返回有效值）
        slot = drawer.getClickedSlot(clickX, clickY, clickZ, face)
        if slot is None:
            slot = 0
        
        existingItem = drawer.getDrawersItemDict(slot)
        maxVolume = drawer.getDrawersMaxVolume()
        
        # 检查物品类型是否匹配
        if existingItem and existingItem.get('count', 0) > 0:
            # 格子已有物品，检查是否同类型
            if existingItem.get('newItemName') != itemDict.get('newItemName'):
                return
            if existingItem.get('newAuxValue', 0) != itemDict.get('newAuxValue', 0):
                return
        else:
            # 格子为空
            if drawer.isLocked():
                # 锁定状态不能放入新类型
                return
            existingItem = {
                'newItemName': itemDict.get('newItemName', ''),
                'newAuxValue': itemDict.get('newAuxValue', 0),
                'count': 0,
            }
        
        # 计算可存入数量
        currentCount = existingItem.get('count', 0)
        spaceLeft = maxVolume - currentCount
        if spaceLeft <= 0:
            return
        
        addCount = min(itemDict.get('count', 1), spaceLeft)
        
        # 阻止默认行为
        args['ret'] = True
        
        # 更新抽屉数据
        existingItem['count'] = currentCount + addCount
        drawer.setDrawersItemDict(existingItem, slot)
        
        # 扣除玩家物品
        gameType = Level.Game.GetPlayerGameType(entityId)
        if gameType != Enum.GameType.Creative:
            comp_item = Player.Item(entityId)
            itemDict['count'] -= addCount
            if itemDict['count'] > 0:
                comp_item.SpawnItemToPlayerInv(itemDict, entityId, comp_item.GetSelectSlotId())
        
        # 同步渲染
        drawer.syncRenderData()
        drawer.RenderItemEntity()
    
    # ─── 空手右键方块（取出物品）────────────────────────────────────────────────
    
    def ServerBlockUseEvent(self, args):
        """
        空手右键抽屉：取出物品
        只响应正面点击
        """
        playerId = args['playerId']
        blockName = args['blockName']
        x = args['x']
        y = args['y']
        z = args['z']
        clickX = float(args['clickX'])
        clickY = float(args['clickY'])
        clickZ = float(args['clickZ'])
        dimensionId = args['dimensionId']
        face = args['face']
        
        if blockName not in config.drawersData:
            return
        
        drawer = _newDrawers(dimensionId, (x, y, z))
        
        # 检查是否点击正面
        if not drawer.isFrontFace(face):
            return
        
        # 防双击
        key = (x, y, z, dimensionId)
        if key not in self.useTimeDict:
            self.useTimeDict[key] = 0
        if time.time() - self.useTimeDict[key] < config.PC_TIME_CLICK:
            return
        self.useTimeDict[key] = time.time()
        
        # 检查手持物品（必须空手）
        comp_item = compFactory.CreateItem(playerId)
        carriedItem = comp_item.GetPlayerItem(Enum.ItemPosType.CARRIED, 0)
        if carriedItem:
            return
        
        # 潜行时不触发
        if Player.PlayerComp(playerId).isSneaking():
            return
        
        # 检查私有权限
        if drawer.isPrivateDrawers():
            ownerId = drawer.getPrivateDrawersUserId()
            if ownerId != playerId:
                return
        
        # 获取点击的格子（已验证正面，所以不会返回None）
        slot = drawer.getClickedSlot(clickX, clickY, clickZ, face)
        if slot is None:
            return
        
        existingItem = drawer.getDrawersItemDict(slot)
        if not existingItem or existingItem.get('count', 0) <= 0:
            return
        
        # 取出一组（最多64个）
        takeCount = min(existingItem.get('count', 0), 64)
        
        # 创建掉落物品
        dropItem = copy.deepcopy(existingItem)
        dropItem['count'] = takeCount
        self.CreateEngineItemEntity(dropItem, dimensionId, (x + 0.5, y + 1, z + 0.5))
        
        # 更新抽屉数据
        existingItem['count'] -= takeCount
        if existingItem['count'] <= 0:
            existingItem = None
        drawer.setDrawersItemDict(existingItem, slot)
        
        # 同步渲染
        drawer.syncRenderData()
        drawer.RenderItemEntity()
    
    # ─── 方块破坏 ─────────────────────────────────────────────────────────────
    
    def BlockRemoveServerEvent(self, args):
        """
        方块破坏时掉落内容物
        """
        x = args.get('x', 0)
        y = args.get('y', 0)
        z = args.get('z', 0)
        fullName = args.get('fullName', '')
        dimension = args.get('dimension', 0)
        
        if fullName not in config.drawersData:
            return
        
        # 清理防双击记录
        key = (x, y, z, dimension)
        self.useTimeDict.pop(key, None)
        self.itemUseTimeDict.pop(key, None)
        
        drawer = _newDrawers(dimension, (x, y, z))
        
        # 销毁渲染实体
        drawer.DestroyRenderEntity(list(range(drawer.getSize())))
        
        # 掉落所有物品
        drawersData = drawer.getDrawersAllDict()
        for slot_str, itemDict in drawersData.items():
            if not itemDict or itemDict.get('count', 0) <= 0:
                continue
            self.CreateEngineItemEntity(itemDict, dimension, (x + 0.5, y + 1, z + 0.5))
        
        # 掉落升级组件
        upgradeData = drawer.getUpgradeAllDict()
        for slot_str, itemDict in upgradeData.items():
            if not itemDict or itemDict.get('count', 0) <= 0:
                continue
            self.CreateEngineItemEntity(itemDict, dimension, (x + 0.5, y + 1, z + 0.5))
    
    def Destroy(self):
        """系统销毁时清理"""
        self.useTimeDict.clear()
        self.itemUseTimeDict.clear()
