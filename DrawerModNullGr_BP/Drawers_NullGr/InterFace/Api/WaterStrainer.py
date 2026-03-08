# coding=utf-8
class ServerSys():
    def getWaterStrainer(self):
        return WaterStrainer()

    def Destroy(self):
        pass


class WaterStrainer():
    def __init__(self):
        pass

    def getSys(self):
        pass

    def getAllStrainerItems(self):
        """
        返回滤网物品列表
        return : list
        """
        pass

    def setAllStrainerItems(self, allStrainerItems):
        """
        设置滤网物品列表
        return : bool
        """
        pass

    def ExtendAllStrainerItems(self, allStrainerItems):
        """
        拓展滤网物品列表
        return : bool
        """
        pass
    def getBaitList(self):
        """
        返回饵料列表
        """
        pass

    def ExtendBaitList(self, bait_list):
        """
        拓展饵料列表
        """
        pass