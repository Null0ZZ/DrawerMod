# coding=utf-8
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from Api.FarmDelight import ServerSys as FarmDelightSys
from Api.ProjectE import ServerSys as ProjectESys
from Api.SuperTransTable import ServerSys as SuperTransTable
from Api.WaterStrainer import ServerSys as WaterStrainerSys
from Api.ButcherDelight import ServerSys as ButcherSys
from Api.BakingDelight import ServerSys as BakingSys


def GetFarmDelightInterFaceSys():  # type:() -> FarmDelightSys
    """
    返回农夫乐事接口系统
    """
    return serverApi.GetSystem('FarmerDelightMod', 'FarmerDelight_InterFace_ServerSys')


def GetProjectEInterFaceSys():  # type:() -> ProjectESys
    """
    返回等价交换接口
    """
    return serverApi.GetSystem('projectE_nullgr', 'ProjectEInterFaceServerSys_nullgr')


def GetSuperTransTableInterFaceSys():  # type:() -> SuperTransTable
    """
    返回超级转换桌接口
    """
    return serverApi.GetSystem('projectE_nullgrv0', 'ProjectV0InterFaceServerSys_nullgr')


def GetWaterStrainerInterFaceSys():  # type:() -> WaterStrainerSys
    """
    返回滤水器接口
    """
    return serverApi.GetSystem('WaterStrainer', 'InterFaceSys_Main_ServerSys')


def GetButcherDelightInterFaceSys():  # type:() -> ButcherSys
    """

    """
    return serverApi.GetSystem('ButcherCraft', 'ButcherCraft_InterFace_nullgr_ServerSys')


def GetBakingDelightInterFaceSys():  # type:() -> BakingSys
    """

    """
    return serverApi.GetSystem('BakingDelight', 'BakingDelight_InterFace_ServerSys')


from Api.CountryCookingInterFaceSys import InterFaceSys as CountryCookingInterFace


def GetCountryCookingInterFaceSys():  # type:()->CountryCookingInterFace|None
    interFaceModule = serverApi.ImportModule("CountryCooking_NullGr.ModSys.InterFace.interFace_ss")
    if not interFaceModule: return None
    interFaceSys = interFaceModule.InterFaceSys()
    return interFaceSys


def ClientGetCountryCookingInterFaceSys():  # type:()->CountryCookingInterFace|None
    interFaceModule = clientApi.ImportModule("CountryCooking_NullGr.ModSys.InterFace.interFace_ss")
    if not interFaceModule: return None
    interFaceSys = interFaceModule.InterFaceSys()
    return interFaceSys





