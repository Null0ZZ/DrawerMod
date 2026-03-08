# -*- coding: utf-8 -*-
"""
屠宰相关接口
"""
class ServerSys():
    def __init__(self, namespace, systemName):
        pass


    def getDryingRack(self):
        """
        返回一个晾干架管理实例
        """
        return DryingRack()

    def getSkinKnife(self):
        """
        返回剥皮刀操作管理实例
        """
        return SkinKinfe()

    def getGutKnife(self):
        """
        返回穿肠刀操作管理实例
        """
        return GutKnie()

    def getBoneSaw(self):
        """
        返回骨锯操作管理实例
        """
        return BoneSaw()

    def getButcher(self):
        """
        返回屠刀操作管理实例
        """
        return ButcherKnife()
    def getCarcass(self):
        """
        返回悬挂尸体（例如猪牛羊尸体）的管理实例
        """
        return Carcass()
    def getMeatHook(self):
        """
        返回挂钩操作实例
        """
        return MeatHook()



class DryingRack():
    def __init__(self):
        self.dring_recipe = {}
        self.render_type = {}
    def ExtendDryingRecipe(self,drying_reicpe_data):
        """
        扩展晾干架的配方
        'minecraft:kelp':{
        -1:{#放置物品的aux,无特殊情况一般为-1，表示任意aux均符合
            'output':[#输出为一个字典列表
                {
                    'newItemName':'minecraft:dried_kelp',
                    'newAuxValue':0,
                    'count':1
                }
            ]

        }
    },
        """
        self.dring_recipe.update(drying_reicpe_data)

    def setItemRenderType(self,itemDict,render_type):
        """
        设置某物品在晾干架上的渲染类型
        如蛋糕虽然类型为方块，但渲染时为二维贴图非立体方块，因此蛋糕的render_type则需要设置为0.0
        #item:0.0
        #block:1.0
        """
        if not isinstance(itemDict,dict):return False
        itemName = itemDict['newItemName']
        self.render_type[itemName] = render_type

    def ExtendItemRenderType(self,renderTypeData):
        """
        批量注册物品的渲染类型，该方法直接将renderTypeData并入config配置文件
        拓展物品的渲染类型
        #item:0.0
        #block:1.0
        格式：
        renderTypeData = {
            itemName:type,
            itemName2:type2,
            str : int,
            ...
            }
        """
        self.render_type.update(renderTypeData)


class SkinKinfe():
    def __init__(self):
        self.skin_knife = {}
        self.skin_recipe = {}
        pass

    def ExtendSkinKnifeList(self,knife_list):#type:(list)->bool
        """
        拓展刨皮刀列表
        """
        if not isinstance(knife_list,list):return False
        self.skin_knife += knife_list
        return True

    def ExtendSkinKnifeRecipe(self,recipe):#type:(dict)->bool
        """
        拓展去皮配方
        return : bool
        格式：
        "butchercraft_nullgr:cow_hook":{#被刀点击的尸体方块id
        -1:{#尸体方块的aux，-1表示不限制aux
            'after':{#被去皮后变为何种方块
                'name':'butchercraft_nullgr:cow_skinned_2',
                'aux':-1#int，-1表示跟随原尸体方块aux
            },
            'drop':[#掉落
                {
                    'newItemName':str,
                    'newAuxValue':int,
                    'count':int,
                    'odds':int,#可选填字段，0-100,表示掉落的概率，若为100，则百分百掉落，若该字段（odds)没有，则默认100掉落
                }
            ]
        """

        self.skin_recipe.update(recipe)


class GutKnie():
    def __init__(self):
        self.gutted_knife = {}
        self.gutted_recipe = {}

    def ExtendGutKnifeList(self, knife_list):
        """
        拓展穿肠刀列表
        """
        if not isinstance(knife_list, list): return False
        self.gutted_knife += knife_list
        return True

    def ExtendGutKnifeRecipe(self, recipe):
        """
        拓展穿肠配方
        return : bool
        """

        self.gutted_recipe.update(recipe)


class BoneSaw():
    def __init__(self):
        self.bonesaw = {}
        self.bonesaw_recipe = {}

    def ExtendBoneSawList(self, knife_list):
        """
        拓展骨锯列表
        """
        if not isinstance(knife_list, list): return False
        self.bonesaw += knife_list
        return True

    def ExtendBoneSawRecipe(self, recipe):
        """
        拓展骨锯配方
        return : bool
        """

        self.bonesaw_recipe.update(recipe)


class ButcherKnife():
    def __init__(self):
        self.butchers = {}
        self.butcher_recipe = {}
        self.butcher_destory_recipe = {}
        self.butcher_attack_reicpe = {}


    def ExtendButcherList(self, knife_list):
        """
        拓展骨锯列表
        """
        if not isinstance(knife_list, list): return False
        self.butchers += knife_list
        return True

    def ExtendButcherRecipe(self, recipe):
        """
        拓展骨锯配方
        return : bool
        """

        self.butcher_recipe.update(recipe)
        return True

    def ExtendButcherDestoryRecipe(self,recipe):
        """
        拓展屠刀的破坏方块配方
        return : bool
        """
        self.butcher_destory_recipe.update(recipe)
        return True

    def ExtendButcherAttackRecipe(self,recipe):
        """
        拓展屠刀的攻击实体配方
        return : bool
        """
        self.butcher_attack_reicpe.update(recipe)
        return True


class Carcass():
    def __int__(self):
        self._carcass = {}
        self.loots = {}
        self.all_carcass_blocks= []
        self.lastCarcass = []

    def ExtendCarcass(self,carcassData):
        self._carcass.update(carcassData)
        for itemName in carcassData:
            block = carcassData[itemName]['place_block']['name']
            itemDict = {}
            itemDict['newItemName'] = itemName
            itemDict['newAuxValue'] = 0
            itemDict['count'] = 1
            self.loots[block] = itemDict
            self.all_carcass_blocks.append(block)

    def ExtendLastCarcassList(self,lastCarcassList):
        self.lastCarcass += lastCarcassList


class MeatHook():
    def __init__(self):
        self.meatHook = []
        self.meatHookConnectType = {}

    def ExtendMeatHookConnectType(self, connect_type_data):
        self.meatHookConnectType.update(connect_type_data)

    def AddMeatHookList(self, MeatHookList):
        self.meatHook += MeatHookList