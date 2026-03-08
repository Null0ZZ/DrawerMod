# -*- coding: utf-8 -*-

class InterFaceSys():
    def __init__(self):
        pass
    def GetCountryCookingPotManger(self):
        return CountryCookingPot()

    def GetCountrySkilletManger(self):
        return CountrySkillet()

    def GetJarMangger(self):
        return Jar()

    def GetRecipeBookManger(self):
        return RecipeBook()





class Jar():
    def __init__(self):

        pass

class CountrySkillet():
    contentVar = {}
    seasoningList = []
    initMolangValue = {}
    skilletData = {}
    boneData = {}
    beforFryReady = {}
    itemContentType = {}
    trayData = {}
    FryRecipe = {}

    def UpdateSkilletData(self,skilletData):#type:(dict)->None
        """
        更新Content内容信息
        自动生成配置boneData
        """
        pass


    def UpdateTrayData(self,trayData):#type:(dict) -> bool
        """
        更新锅底内容信息
        """
        if not isinstance(trayData,dict):return False
        self.trayData.update(trayData)
        return True




    def UpdateContentVar(self,contentVar):
        """
        更新块名称对应的molang变量
        """
        self.contentVar.update(contentVar)

    def UpdateInitMolangValue(self,molangValueDict):
        """
        更新初始molang池内容
        包含所有块，子块的molang初始信息
        """
        self.initMolangValue.update(molangValueDict)

    def ExtendSeasoningList(self,seasoningList):
        """
        拓展调味料列表信息
        """
        self.seasoningList+=seasoningList

    def UpdateBeforFryReady(self,beforReady):
        """
        更新预备工作需求字典
        """
        self.beforFryReady.update(beforReady)

    def UpdateItemContentType(self,itemContentTypeDict):
        """
        更新可放入道具及对应内容字典
        """
        self.itemContentType.update(itemContentTypeDict)

    def UpdateFryRecipe(self,recipeDict):
        """
        更新总配方信息
        """
        self.FryRecipe.update(recipeDict)

class CountryCookingPot():
    contentVar = {}
    initMolangValue = {}
    cookingPotData = {}
    boneData = {}
    cookingPotPlaceItems = {}
    FryRecipe = {}
    stirringTools = []
    potList = []
    soupData = {}

    def UpdateCookingPotData(self,skilletData):
        pass



    def UpdateSoupData(self,soupData):#type:(dict)->bool
        """
        更新汤底总配置
        """
        if not isinstance(soupData,dict):return False
        self.soupData.update(soupData)
        return True


    def UpdateContentVar(self,contentVar):
        self.contentVar.update(contentVar)

    def UpdateInitMolangValue(self,molangValueDict):
        self.initMolangValue.update(molangValueDict)



    def UpdateItemContentType(self,itemContentTypeDict):
        self.cookingPotPlaceItems.update(itemContentTypeDict)

    def UpdateFryRecipe(self,recipeDict):
        self.FryRecipe.update(recipeDict)

    def ExtentPotList(self,potList):#type:(list[str])->bool
        """
        拓展pot列表
        """
        if not isinstance(potList,list):return False
        self.potList+=potList

    def ExtentStirringToolsList(self,toolsList):#type:(list[str])-> bool
        """
        拓展stirTools
        """
        if not isinstance(toolsList,list):return False
        self.stirringTools+=toolsList
        return True




class RecipeBook():
    modData = {}
    books = []

    def UpdateModData(self,modData):
        self.modData.update(modData)

    def ExtendBooksItem(self,itemList):
        self.books+=itemList











