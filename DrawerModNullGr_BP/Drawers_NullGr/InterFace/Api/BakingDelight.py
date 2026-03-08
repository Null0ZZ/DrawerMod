# coding=utf-8
"""
该接口文件废弃不用
Oven（烤炉）相关接口已移动至主包接口
"""
import mod.server.extraServerApi as serverApi
class ServerSys():
    def __init__(self):
       pass

    def GetOven(self):
        return Oven()



class Oven():
    def __init__(self):
        self.cookingrecipe = {}


    def getSys(self):#type:() -> serverApi.GetSystem()
        return serverApi.GetSystem('','')

    def GetCookingRecipe(self):
        return self.cookingrecipe
        pass




    def AddCookingRecipe(self,recipeDict):#type:(dict)->None
        self.cookingrecipe.update(recipeDict)

        pass

    def SendCookingRecipeToClient(self,id = None):
       pass








