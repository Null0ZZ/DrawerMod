# coding=utf-8

class ServerSys():
    def __init__(self):
        pass

    def GetKnifeManger(self):
        """
        返回小刀管理器
        用于管理小刀列表，小刀对方块使用、破坏、对生物击杀等操作
        """
        return Knife()

    def GetStoveManger(self):
        """
        返回灶炉管理器
        用于管理灶炉列表
        """
        return Stove()

    def GetCuttingBoard(self):
        return CuttingBoard()

    def getTag(self):
        """
        返回标签管理器
        用于管理开发者自定义的物品或生物标签
        """
        return Tag()

    def GetCookingPot(self):
        """
        返回厨锅管理器
        用于管理厨锅配方，厨锅列表，厨锅热源等数据
        """
        return CookingPot()

    def GetEat(self):
        """
        返回食用操作管理器
        用于配置管理与方块食物的交互，食用特殊效果配置等等
        """
        return Eat()

    def GetFarmland(self):
        """
        返回耕地管理器
        """
        return FarmLand()

    def GetCropper(self):
        """
        返回农作物管理器
        用于配置管理农作物的生长，种植等逻辑
        """
        return Cropper()

    def GetSkillet(self):
        """
        返回煎锅管理器

        """
        return Skillet()
    def GetHelp(self):
        """
        返回说明类管理器
        """
        return Help()


    def GetUseToBlock(self):
        return UseToBlock()

    def getOvenManger(self):
        return Oven()

class Oven():
    """
    烤炉的配方格式与厨锅一致，
    """
    def __init__(self):
        self.ovenRecipe = {}



    def getSys(self):
        pass

    def GetOvenRecipe(self):
        return self.ovenRecipe





    def AddOvenRecipe(self,recipeDict):#type:(dict)->None
        self.ovenRecipe.update(recipeDict)

        pass

    def SendOvenRecipeToClient(self,id = None):
        pass



class Knife():
    def __init__(self):
        self.knifes = []

    def getKnifesList(self):  # type:()->list[str]
        """
        返回所有刀的id列表
        return list
        """
        return self.knifes

    def ExtendKnifeKillRecipe(self, recipeDict={}):#type:(dict)->None
        """
        扩充击杀实体配方，非覆盖式

        """
        pass
    def AddKnifeItemToList(self, itemNameList):  # type:(list)->None
        """
        批量添加物品进刀列表
        itemNameList:要设置为刀的物品列表,list[itemName]
        """
        pass

    def DeletKnifeItemFromList(self, itemName):  # type:(str)->bool
        """
        将一个物品移出刀类
        """
        if itemName not in self.knifes: return False
        self.knifes.remove(itemName)
        return True

    def AddKnifeDestoryRecipe(self,recipeDict):#type:(dict)->None
        """
        增加刀破坏方块配方
        dict = {
        'minecraft:tallgrass':{
        -1:{#aux,-1表示任意aux
            #破坏后额外掉落键
            'drop':[
                {
                    'newItemName':'farmer_delight_nullgr:straw',
                    'newAuxValue':0,
                    'count':1,
                    'odds':33#掉落概率，1-100，该键没有时视为100%掉落
                }
            ]
            #可根据功能拓张其他键
            #...
        }
    },
    }
        """
        pass
    def AddKnifeItemUseOnRecipe(self,recipeDict):#type:(dict)->None
        """
        增加刀对方块使用配方
        """
        pass
    def AddKnifeKillRecipe(self,recipeDict):#type:(dict)->None
        """
        增加击杀实体配方
        """
        pass



class UseToBlock():
    """
    方块点击类管理
    用于控制开发者对方块的点击操作逻辑
    其中包括掉落，音效，等等
    """
    def __init__(self):
        self.useData = {}
        self.placeData = {}

    def ExtendUseData(self,useData):
        """
        拓展玩家点击方块逻辑
        """
        self.useData.update(useData)
    
    def GetUseData(self):
        return self.useData
    
    def ExtendPlaceData(self,placeData):
        self.placeData.update(placeData)
    
    def GetPlaceData(self):
        return self.placeData



class Stove():
    def __init__(self):
        self.stoves = []

    def getStovesList(self):  # type:()->list
        """
        返回所有灶炉列表
        return : list[str]
        """
        return self.stoves

    def AddStoveItemToList(self, itemNameList):  # type:(list[str])->None
        """
        拓展灶炉列表
        itemNameList:list[str]
        """
        pass

    def AddStoveOnItemToList(self, itemNameList):  # type:(list)->None
        """
        拓展灶炉列表(燃烧状态)

        """
        pass

    def DeletStoveItemFromList(self, itemName):  # type:(str)->bool
        """
        从灶炉列表中删除某个灶炉

        """
        if itemName not in self.stoves: return False
        self.stoves.remove(itemName)
        return True


class Tag():
    def __init__(self):
        self.tag = {}

    def ExtendTag(self, tagDictList):
        """
        注册tag信息
        tagDictList:list[dict]
            tag_1 = {'minecraft:egg':'egg','minecrft:wood':'egg'}
            tag_2 = {'minecraft:bowl':'contain_wood'}
            tagDictList = [tag_1,tag_2]

        """
        pass
    def getTagFx(self):
        """
        根据游戏内已注册的tag信息
        返回一个以tag为键，该tag下所有的物品列表为值的一个字典
        return:dict['tag':itemList]
        例如：re = {
                    'egg':['minecraft:egg''minecrft:wood'],
                    'contain_wood':['minecraft:bowl']
                }
        """
        pass

    def getTags(self):
        """
        根据游戏内已注册的tag信息
        返回一个以itemName为键，该itemName下所有的物品tag列表为值的一个字典
        return:dict['itemName':tagList]
        例如：re = {
                    'minecraft:carrot':['vegetable','cropper','carrot'],
                    'minecraft:beef':['meat','raw_meat']
                }
        """
        pass

class CuttingBoard():
    def __init__(self):
        self.cutting_recipe ={}
        self.cuttingBoard = {}

        pass

    def ExtendCuttingBoardBlock(self, cuttingBoardList):
        self.cuttingBoard += cuttingBoardList

    def GetCuttingRecipe(self):  # type:()->dcit
        """
        返回砧板菜谱
        """
        return self.cutting_recipe
        pass

    def AddCuttingRecipe(self, recipeDict):  # type:(dict)->None
        """
        增加砧板菜谱
        """

        pass

    def getSys(self):
        return


class CookingPot():
    def __init__(self):
        self.cookingrecipe = {}
        self.cooking_fireBlock = {}
        self.reservers = {}
        self.hotData = {}
        self.potList = []
        self.potData = {}
        pass
    def ExtendPotData(self,potData):
        self.potData.update(potData)
    def ExtendPotList(self,potList):
        self.potList+=potList

    def GetCookingRecipe(self):
        """
        返回所有配方
        """
        pass

    def AddCookingRecipe(self,recipeDict):#type:(dict)->None
        """
        添加配方
        """
        pass
    def GetReceiveRecipe(self):
        pass

    def AddReserverRecipe(self,recipeDict):#type:(dict)->None
        """
        添加接收物配方
        """
        pass

    def AddFireBlock(self,fireBLockData):#type:(dict)->None
        """
        添加可被识别的热源信息
        """
        pass

    def SendCookingRecipeToClient(self, id=None):
        pass

    def SendReceiveRecipeToClient(self, id=None):
        pass

    def getFireBlockData(self):
        return self.hotData

    def getSys(self):
        pass


class Eat():
    def __init__(self):
        self.contian_food = {}
        pass
    def AddClickEatRecipe(self,reicpeDict):#type:(dict)->None
        """
        添加点击食用配方
        """
        pass
    def ExtendEatEff(self,Eat_Eff):
        pass
    def ExtendContainFoodData(self,data):
        self.contian_food.update(data)
    def getSys(self):
        """
        返回Eat主系统
        """
        pass




class FarmLand():
    def __init__(self):
        self.compposterData = {}
        self.richFarmland = {}
        pass
    def AddTransRecipe(self,recipeDict):#typr:(dict) -> None
        pass

    def AddFccBlockList(self,fccList):#type:(dict) -> None
        """
        增加催化物
        """
        pass

    def AddRichSoilList(self,blockList):#type:(dict) -> None
        pass

    def AddMushroomTranDict(self,tranDict):
        pass


    def ExtendRichFarmLandData(self,dataDict):
        self.richFarmland.update(dataDict)


class Cropper():
    def __init__(self):
        self.seedPlantData = {}
        self.compposterData = {}
        self.blockRemove = {}
        pass
    def ExtendComposterItemData(self,data):
        self.compposterData.update(data)

    def AddCropperDict(self,copperDict):
        """
        增加农作物，增加的农作物会随被水流破坏和不能浮空
        请将作物方块的邻近方块更新发送事件、禁止在水源中放置，以及方块销毁事件打开
        格式:
        dict = {
                'farmer_delight_nullgr:wild_rice_top':{
                'blocks':['farmer_delight_nullgr:wild_rice_bottom'],
                'oprater':'==',
                },
                'namespace:xxxx':{
                'blocks':['farmer_delight_nullgr:wild_rice_bottom'],
                'oprater':'!=',
                },
                }
        """
        pass

    def AddCropperRandomTickGrowthDict(self,cropperGrowthDict):#type:(dict)->None
        """
        给农作物添加农作物随机生长的信息
        cropperGrowthDict格式介绍
        cropperGrowthDict = {
            'farmer_delight_nullgr:rice_stage4':{
                'next':{
                    'name':'farmer_delight_nullgr:rice_stage5','aux':-1
                },
                'next_add':{#可选键
                    "d_pos":(0,1,0),
                    'add_block':{
                        'name':'farmer_delight_nullgr:rice_stage_up5','aux':-1
                    }
                },
                #可选键，控制农作物生长时周围必须要哪些方块
                'need_block':{
                    #and:blocks 下所有位置条件必须均成立
                    #or :blocks 下任一位置条件成立即可
                    'op':'or',#or / and
                    'blocks':{
                    #条件
                    #（相对位置）：[需要存在的方块。。]，位置处存在任一列表中的方块时该条件成立
                    (0,-1,0):['minecraft:dirt','minecraft:grass','minecraft:farmland',]
                    }
                },
                #可选键，适用于树苗等生长成结构的作物
                'structures':{
                    'name':'cultural_delight_nullgr:avocado_tree',#结构名称
                    'pos':(-5,0,-5),#结构生成的相对偏移位置
                    'rotation':0#旋转角度，一般为0,90,180等
                },
            },
        }
        """

    def AddBoneMealCropper(self,boneMealCropper):
        """
        给农作物添加农作物骨粉崔熟的信息
        dict = {
            'farmer_delight_nullgr:rice_stage4':{
                'next':{
                    'name':'farmer_delight_nullgr:rice_stage5','aux':-1
                },
                'next_add':{#可选键
                    "d_pos":(0,1,0),
                    'add_block':{
                        'name':'farmer_delight_nullgr:rice_stage_up5','aux':-1
                    }
                }
            },
        }
        """
        pass
    def ExtendSeedPlantData(self,plantData):
        self.seedPlantData.update(plantData)

    def getBlockRemoveData(self):
        return self.blockRemove

    def setBlockRemoveData(self, data):  # type:(dict)->bool
        if not isinstance(data, dict): return False
        self.blockRemove.update(data)
        return True

    def AddCropperGrowthDataFromFastCropper(self,data):#type:(dict)->bool
        return True




class Skillet():
    def __init__(self):
        pass

    def AddFireBlock(self,fireDataDcit):
        """
        添加热源
        """
        pass
    def ExtendWhiteList(self,white_list):
        """
        拓展白名单
        white_list : list[str]
        """
        return True

    def ExtendSkillet(self, skilletData):
        pass


class Help():
    def __init__(self):
        pass
    def ExtendModData(self, modData):
        pass
    def ExtendHelpDict(self, help_dict):
        """
        拓展help集合
        help_dict:dict
        """
        return True
    def SendHelpDataToClient(self, id=None):
        """
        发送help信息给主包客户端同步
        副包系统一般不使用该接口
        """
        pass
    def ExtendNeedHelpDict(self,need_help_dict):
        """
        拓展need-help
        need_help_key = {
            "nether_delight_nullgr:stuffed_hoglin_11":{
            'base_data_make':True,#是否需要系统自动制作基础信息，例如是否在砧板合成等
            'extra_help':{
                'text':" ---extra---"#额外信息，将会追加在base_data_make制作的信息之后
            }
            #...
         }
        }
        """
        pass


    def getSys(self):
        """
        返回接口系统
        """
        pass
