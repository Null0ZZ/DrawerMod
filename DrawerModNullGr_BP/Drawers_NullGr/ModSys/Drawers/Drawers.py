# -*- coding: utf-8 -*-
"""
抽屉数据类 - 继承客户端渲染基类
提供抽屉数据读写方法，兼容旧存档数据结构
"""
import copy
import mod.server.extraServerApi as serverApi
import Drawers_NullGr.SMethod as sm
import Drawers_NullGr.com as com
import Drawers_NullGr.NullGr.server.Level as Level
from Drawers_NullGr.ClientRenderClass.BaseClass_RenderMoreServer import RenderBlockBaseMoreServer
import config

compFactory = serverApi.GetEngineCompFactory()
Enum = serverApi.GetMinecraftEnum()


class Drawers(RenderBlockBaseMoreServer):
    """
    抽屉数据类
    继承 RenderBlockBaseMoreServer 获得客户端渲染能力
    """
    
    def __init__(self, dimId, pos):
        """
        :param dimId: 维度ID
        :param pos: 方块坐标 (x, y, z)
        """
        RenderBlockBaseMoreServer.__init__(self, dimId, pos)
        self.dimId = dimId
        self.pos = pos
        self.blockName = Level.BlockInfo.GetBlockNew(pos, dimId).get('name', '')
        
        # BlockEntity 数据键名（兼容旧存档）
        self.key_drawersDataDict = 'drawersDataDict'
        self.key_chestDataDict = 'chestDataDict'
        self.key_maxNum = 'maxNum'
        self.key_isLocked = 'isLocked'
        self.key_user = 'user'
        self.key_isShowCount = 'isShowCount'
        self.key_isShowPro = 'isShowPro'
        self.key_shroud = 'shroud'
    
    # ─── 基础信息 ─────────────────────────────────────────────────────────────
    
    def getDrawersConfig(self):
        """获取当前抽屉的配置信息"""
        return config.drawersData.get(self.blockName, {})
    
    def getDrawersSize(self):
        """
        获取抽屉的储物格子数
        :return: 1, 2, 4 或 -1（非抽屉方块）
        """
        cfg = self.getDrawersConfig()
        return cfg.get('slots', -1)
    
    def getSize(self):
        """
        重写基类方法：返回渲染位置数量
        对于抽屉，渲染位置数 = 储物格子数
        """
        size = self.getDrawersSize()
        return size if size > 0 else 1
    
    def isCompact(self):
        """判断是否为压缩抽屉"""
        cfg = self.getDrawersConfig()
        return cfg.get('compact', False)
    
    # ─── 物品数据读写（兼容旧存档）────────────────────────────────────────────
    
    def getDrawersAllDict(self):
        """
        获取抽屉所有格子的物品字典
        :return: {slot(str): itemDict} 或 {}
        """
        data = self.data()
        if not data:
            return {}
        drawersDataDict = data[self.key_drawersDataDict]
        if drawersDataDict is None:
            return {}
        return drawersDataDict
    
    def setDrawersAllDict(self, drawersDict):
        """
        设置抽屉所有格子的物品字典
        :param drawersDict: {slot(str): itemDict}
        :return: bool
        """
        if not isinstance(drawersDict, dict):
            return False
        data = self.data()
        if not data:
            return False
        size = self.getDrawersSize()
        if len(drawersDict) > size:
            return False
        data[self.key_drawersDataDict] = drawersDict
        return True
    
    def getDrawersItemDict(self, slot=0):
        """
        获取抽屉某个格子的物品字典
        :param slot: 格子索引
        :return: itemDict 或 None
        """
        drawersDataDict = self.getDrawersAllDict()
        return drawersDataDict.get(str(slot))
    
    def setDrawersItemDict(self, itemDict, slot=0):
        """
        设置抽屉某个格子的物品字典
        :param itemDict: 物品字典，None 或 count=0 表示清空
        :param slot: 格子索引
        :return: bool
        """
        drawersDataDict = self.getDrawersAllDict()
        
        # 处理空物品
        if itemDict and itemDict.get('count', 0) <= 0:
            itemDict = None
        
        drawersDataDict[str(slot)] = itemDict
        return self.setDrawersAllDict(drawersDataDict)
    
    def getFirstItemData(self):
        """
        获取抽屉第一个有物品的格子信息
        :return: {'slot': slot, 'itemDict': itemDict} 或 None
        """
        drawersDataDict = self.getDrawersAllDict()
        for slot_str in drawersDataDict:
            item = drawersDataDict[slot_str]
            if item and item.get('count', 0) > 0:
                return {'slot': slot_str, 'itemDict': item}
        return None
    
    # ─── 容量管理 ─────────────────────────────────────────────────────────────
    
    def getDrawersRawVolume(self):
        """获取抽屉原始基础容量（未经升级）"""
        cfg = self.getDrawersConfig()
        return cfg.get('baseVolume', 2048)
    
    def getDrawersMaxVolume(self):
        """获取抽屉当前最大容量（已计算升级）"""
        data = self.data()
        if not data:
            return self.getDrawersRawVolume()
        maxNum = data[self.key_maxNum]
        if maxNum is None:
            return self.getDrawersRawVolume()
        return maxNum
    
    def setDrawersMaxVolume(self, volume):
        """设置抽屉最大容量"""
        data = self.data()
        if not data:
            return False
        data[self.key_maxNum] = volume
        return True
    
    # ─── 升级槽管理 ───────────────────────────────────────────────────────────
    
    def getUpgradeSize(self):
        """获取升级槽数量"""
        return config.UPGRADE_SLOT_COUNT
    
    def getUpgradeAllDict(self):
        """获取所有升级槽物品"""
        data = self.data()
        if not data:
            return {}
        chestDataDict = data[self.key_chestDataDict]
        if chestDataDict is None:
            return {}
        return chestDataDict
    
    def setUpgradeAllDict(self, allDict):
        """设置所有升级槽物品"""
        data = self.data()
        if not data:
            return False
        data[self.key_chestDataDict] = allDict
        return True
    
    def getUpgradeItemDict(self, slot=0):
        """获取某个升级槽的物品"""
        upgs = self.getUpgradeAllDict()
        return upgs.get(str(slot))
    
    def setUpgradeItemDict(self, itemDict, slot=0):
        """设置某个升级槽的物品"""
        upgs = self.getUpgradeAllDict()
        upgs[str(slot)] = itemDict
        return self.setUpgradeAllDict(upgs)
    
    # ─── 锁定与私有化 ─────────────────────────────────────────────────────────
    
    def isLocked(self):
        """判断抽屉是否锁定物品类型"""
        data = self.data()
        if not data:
            return False
        isLocked = data[self.key_isLocked]
        return isLocked if isLocked is not None else False
    
    def lockDrawers(self):
        """锁定抽屉物品类型"""
        data = self.data()
        if not data:
            return False
        data[self.key_isLocked] = True
        return True
    
    def unlockDrawers(self):
        """解锁抽屉物品类型"""
        data = self.data()
        if not data:
            return False
        data[self.key_isLocked] = False
        return True
    
    def isPrivateDrawers(self):
        """判断是否为私有抽屉"""
        data = self.data()
        if not data:
            return False
        return data[self.key_user] is not None
    
    def getPrivateDrawersUserId(self):
        """获取私有抽屉拥有者ID"""
        data = self.data()
        if not data:
            return None
        return data[self.key_user]
    
    def setPrivateDrawers(self, userId):
        """设置为私有抽屉"""
        data = self.data()
        if not data:
            return False
        data[self.key_user] = userId
        return True
    
    def disPrivateDrawers(self):
        """解除私有抽屉"""
        data = self.data()
        if not data:
            return False
        data[self.key_user] = None
        return True
    
    # ─── 显示设置 ─────────────────────────────────────────────────────────────
    
    def isShowCountUI(self):
        """判断是否显示数量UI"""
        data = self.data()
        if not data:
            return True
        isShowCount = data[self.key_isShowCount]
        return isShowCount if isShowCount is not None else True
    
    def setDrawersShowCountUI(self, show=True):
        """设置是否显示数量UI"""
        data = self.data()
        if not data:
            return False
        data[self.key_isShowCount] = show
        return True
    
    def isShieldEntityIcon(self):
        """判断是否屏蔽生物图标渲染"""
        data = self.data()
        if not data:
            return False
        shroud = data[self.key_shroud]
        return shroud if shroud is not None else False
    
    def setShieldEntityIcon(self, shroud=False):
        """设置是否屏蔽生物图标渲染"""
        data = self.data()
        if not data:
            return False
        data[self.key_shroud] = shroud
        return True
    
    # ─── 渲染相关方法重写 ─────────────────────────────────────────────────────
    
    # direction 到正面 face 的映射
    # direction: 0=南, 1=西, 2=北, 3=东
    # face: 0=下, 1=上, 2=北, 3=南, 4=西, 5=东
    DIR_TO_FACE = {0: 3, 1: 4, 2: 2, 3: 5}
    
    def getRotRenderItemEntityFromAux(self, blockAux):
        """
        根据方块朝向返回渲染实体旋转角度
        方块 direction: 0=南, 1=西, 2=北, 3=东
        物品需要面向玩家（与方块正面一致）
        """
        rot_dict = {
            0: (90, 180, 0),  # 南：物品朝南(+Z)
            1: (90, 90, 0),   # 西：物品朝西(-X)
            2: (90, 0, 0),    # 北：物品朝北(-Z)
            3: (90, -90, 0),  # 东：物品朝东(+X)
        }
        return rot_dict.get(blockAux, (90, 0, 0))
    
    def getRenderBaseData(self):
        """
        返回渲染位置数据 - 根据方块朝向动态计算
        物品显示在抽屉正面
        """
        slots = self.getDrawersSize()
        state = Level.BlockState.GetBlockStates(self.pos, self.dimId)
        direction = state.get('direction', 2) if state else 2
        
        # 是否为压缩抽屉（压缩抽屉正面在方块中心）
        compact = self.isCompact()
        dr = 0.02  # 离方块表面的距离
        
        if compact:
            # 压缩抽屉正面偏移
            base_near = 0.5 - dr
            base_far = 0.5 + dr
        else:
            # 普通抽屉正面在边缘
            base_near = 0 + dr
            base_far = 1 - dr
        
        # 根据朝向计算渲染位置
        # direction: 0=南(正面z=1), 1=西(正面x=0), 2=北(正面z=0), 3=东(正面x=1)
        dp = 0.12  # 物品向正面偏移，避免与方块重叠
        
        if slots == 1:
            return self._calcRenderPos1(direction, base_near, base_far, dp)
        elif slots == 2:
            return self._calcRenderPos2(direction, base_near, base_far, dp)
        elif slots == 4:
            return self._calcRenderPos4(direction, base_near, base_far, dp)
        
        return {0: {'epos': (0.5, 0.5, 0.5), 'scale': 0.8, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)}}
    
    def _calcRenderPos1(self, direction, base_near, base_far, dp):
        """单格抽屉渲染位置"""
        if direction == 0:  # 南
            return {0: {'epos': (0.5 - dp, 0.5, base_far), 'scale': 0.8, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)}}
        elif direction == 2:  # 北
            return {0: {'epos': (0.5 + dp, 0.5, base_near), 'scale': 0.8, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)}}
        elif direction == 1:  # 西
            return {0: {'epos': (base_near, 0.5, 0.5 - dp), 'scale': 0.8, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)}}
        elif direction == 3:  # 东
            return {0: {'epos': (base_far, 0.5, 0.5 + dp), 'scale': 0.8, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)}}
        return {0: {'epos': (0.5, 0.5, base_near), 'scale': 0.8, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)}}
    
    def _calcRenderPos2(self, direction, base_near, base_far, dp):
        """双格抽屉渲染位置（上下布局）"""
        if direction == 0:  # 南
            return {
                0: {'epos': (0.5 - dp, 0.75, base_far), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                1: {'epos': (0.5 - dp, 0.25, base_far), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            }
        elif direction == 2:  # 北
            return {
                0: {'epos': (0.5 + dp, 0.75, base_near), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                1: {'epos': (0.5 + dp, 0.25, base_near), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            }
        elif direction == 1:  # 西
            return {
                0: {'epos': (base_near, 0.75, 0.5 - dp), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                1: {'epos': (base_near, 0.25, 0.5 - dp), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            }
        elif direction == 3:  # 东
            return {
                0: {'epos': (base_far, 0.75, 0.5 + dp), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                1: {'epos': (base_far, 0.25, 0.5 + dp), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            }
        return {
            0: {'epos': (0.5, 0.75, base_near), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            1: {'epos': (0.5, 0.25, base_near), 'scale': 0.5, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
        }
    
    def _calcRenderPos4(self, direction, base_near, base_far, dp):
        """四格抽屉渲染位置（2x2布局）
        格子编号：
        0 1  (上排)
        2 3  (下排)
        """
        if direction == 0:  # 南：正面z=1，玩家站在南侧往北看
            return {
                0: {'epos': (0.25 - dp, 0.75, base_far), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                1: {'epos': (0.75 - dp, 0.75, base_far), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                2: {'epos': (0.25 - dp, 0.25, base_far), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                3: {'epos': (0.75 - dp, 0.25, base_far), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            }
        elif direction == 2:  # 北：正面z=0，玩家站在北侧往南看
            return {
                0: {'epos': (0.75 + dp, 0.75, base_near), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                1: {'epos': (0.25 + dp, 0.75, base_near), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                2: {'epos': (0.75 + dp, 0.25, base_near), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                3: {'epos': (0.25 + dp, 0.25, base_near), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            }
        elif direction == 1:  # 西：正面x=0，玩家站在西侧往东看
            return {
                0: {'epos': (base_near, 0.75, 0.25 - dp), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                1: {'epos': (base_near, 0.75, 0.75 - dp), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                2: {'epos': (base_near, 0.25, 0.25 - dp), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                3: {'epos': (base_near, 0.25, 0.75 - dp), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            }
        elif direction == 3:  # 东：正面x=1，玩家站在东侧往西看
            return {
                0: {'epos': (base_far, 0.75, 0.75 + dp), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                1: {'epos': (base_far, 0.75, 0.25 + dp), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                2: {'epos': (base_far, 0.25, 0.75 + dp), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
                3: {'epos': (base_far, 0.25, 0.25 + dp), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            }
        return {
            0: {'epos': (0.25, 0.75, base_near), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            1: {'epos': (0.75, 0.75, base_near), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            2: {'epos': (0.25, 0.25, base_near), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
            3: {'epos': (0.75, 0.25, base_near), 'scale': 0.35, 'rotation': (0, 0, 0), 'dpos': (0, 0, 0)},
        }
    
    def isFrontFace(self, face):
        """
        判断点击的面是否是抽屉正面
        :param face: 点击的面 (0=下, 1=上, 2=北, 3=南, 4=西, 5=东)
        :return: bool
        """
        state = Level.BlockState.GetBlockStates(self.pos, self.dimId)
        direction = state.get('direction', 2) if state else 2
        return face == self.DIR_TO_FACE.get(direction)
    
    def getClickedSlot(self, clickX, clickY, clickZ, face):
        """
        根据点击位置计算点击的格子
        只有点击正面时才返回有效slot，否则返回None
        :return: slot index 或 None（非正面点击）
        """
        # 首先检查是否点击正面
        if not self.isFrontFace(face):
            return None
        
        slots = self.getDrawersSize()
        
        # 获取方块朝向
        state = Level.BlockState.GetBlockStates(self.pos, self.dimId)
        direction = state.get('direction', 2) if state else 2
        
        v = clickY  # 垂直方向始终用 Y
        
        # 根据朝向确定水平坐标和是否需要反转
        # direction: 0=南, 1=西, 2=北, 3=东
        if direction == 0:  # 南：玩家站南侧看北，左边是东(x大)，右边是西(x小)
            h = 1 - clickX  # 反转X
        elif direction == 2:  # 北：玩家站北侧看南，左边是西(x小)，右边是东(x大)
            h = clickX
        elif direction == 1:  # 西：玩家站西侧看东，左边是北(z小)，右边是南(z大)
            h = clickZ
        elif direction == 3:  # 东：玩家站东侧看西，左边是南(z大)，右边是北(z小)
            h = 1 - clickZ  # 反转Z
        else:
            h = clickX
        
        if slots == 1:
            return 0
        elif slots == 2:
            # 上下布局：y > 0.5 为上格(0)，y <= 0.5 为下格(1)
            return 0 if v > 0.5 else 1
        elif slots == 4:
            # 2x2 布局（玩家视角）
            # 0 1  (上排：左上 右上)
            # 2 3  (下排：左下 右下)
            left = h < 0.5
            top = v > 0.5
            if top:
                return 0 if left else 1
            else:
                return 2 if left else 3
        
        return 0
    
    def getPlaceSlot(self, clickX, clickY, clickZ, face):
        """
        返回放入物品时的目标格子
        优先放入点击的格子，若已满则找第一个空格子
        """
        clicked = self.getClickedSlot(clickX, clickY, clickZ, face)
        if clicked is not None:
            # 检查点击格子是否可以存入
            item = self.getDrawersItemDict(clicked)
            if not item or item.get('count', 0) < self.getDrawersMaxVolume():
                return clicked
        
        # 找第一个空格或未满的格子
        return self.findFirstSlot(findType='isEmpty')
    
    def getTakeSlot(self, clickX, clickY, clickZ, face):
        """
        返回取出物品时的目标格子
        返回点击的格子（如果有物品）
        """
        clicked = self.getClickedSlot(clickX, clickY, clickZ, face)
        if clicked is not None:
            item = self.getDrawersItemDict(clicked)
            if item and item.get('count', 0) > 0:
                return clicked
        return None
    
    # ─── 同步渲染数据 ─────────────────────────────────────────────────────────
    
    def syncRenderData(self):
        """
        同步抽屉物品数据到渲染数据
        将 drawersDataDict 转换为 render_itemDict_dict 格式
        """
        drawersData = self.getDrawersAllDict()
        renderData = {}
        
        for slot_str, itemDict in drawersData.items():
            if itemDict and itemDict.get('count', 0) > 0:
                # 只保留渲染需要的字段
                renderData[int(slot_str)] = {
                    'newItemName': itemDict.get('newItemName', ''),
                    'newAuxValue': itemDict.get('newAuxValue', 0),
                    'count': 1,  # 渲染只显示图标，不需要真实数量
                }
        
        self.setRenderItemDataDict(renderData)
        return True
