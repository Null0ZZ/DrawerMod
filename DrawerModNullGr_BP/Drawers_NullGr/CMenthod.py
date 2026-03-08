# -*- coding: utf-8 -*-

import copy
import mod.client.extraClientApi as clientApi
EN = clientApi.GetEngineNamespace()
ESN = clientApi.GetEngineSystemName()
llid = clientApi.GetLevelId()
def ToListenEvent(sys,listenDict,EN = EN,ESN = ESN):#type:(dcit[list]) -> None
    """
    快速监听
    sys:系统名
    listenDict:监听信息
    EN，ESN监听来自何处的事件，默认系统基类
    """
    for evname in listenDict:
        for fun in listenDict[evname]:
            sys.ListenForEvent(EN, ESN, evname, sys, fun)


def AddButtonListen(back_fun,path,uiNode = clientApi.CreateUI('','')):
    button = uiNode.GetBaseUIControl(path).asButton()
    button.AddTouchEventParams({'isSwallow': True})
    button.SetButtonTouchUpCallback(back_fun)
    return button
def playMusic(music,pos,volume,p,loop):
    comp = clientApi.GetEngineCompFactory().CreateCustomAudio(0)
    musicId = comp.PlayCustomMusic(music, pos, volume, p, loop, None)
    return musicId
def cmpItemDict(item1,item2):
    if not item1:return False
    if not item2:return False
    cmp_item1 = copy.deepcopy(item1)
    cmp_item1['count'] = 1
    cmp_item2 = copy.deepcopy(item2)
    cmp_item2['count'] = 1
    cmp_key = ['enchantData', 'newItemName', 'durability', 'count', 'extraId', 'customTips', 'newAuxValue', 'modEnchantData', 'userData','showInHand']
    for key in cmp_key:
        if key not in cmp_item1:return False
        if key not in cmp_item2:return False
        if cmp_item1[key] != cmp_item2[key]:return False
    return True

def getZXEntityId(llid):
    comp = clientApi.GetEngineCompFactory().CreateCamera(llid)
    pickData = comp.PickFacing()
    return pickData["entityId"]
def getZXBlockPos(llid):
    comp = clientApi.GetEngineCompFactory().CreateCamera(llid)
    pickData = comp.PickFacing()
    pos = [pickData["x"],pickData["y"],pickData["z"]]
    return pos
def getPlayerCarriedItem(pid):
    comp = clientApi.GetEngineCompFactory().CreateItem(pid)
    cd = comp.GetCarriedItem()
    return cd

def getPlayerId():
    localId = clientApi.GetLocalPlayerId()
    return localId
