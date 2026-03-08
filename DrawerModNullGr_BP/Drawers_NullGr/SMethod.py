# -*- coding: utf-8 -*-
import copy
import math
import com
import NullGr.server.Level as Level
import NullGr.server.ExtraData as Extra
import mod.server.extraServerApi as serverApi
compFactory = serverApi.GetEngineCompFactory()
llid = serverApi.GetLevelId()
EN = serverApi.GetEngineNamespace()
ESN = serverApi.GetEngineSystemName()


def unit_vector(A, B):
    """
    计算单位向量AB的坐标
    return : dir(x,y,z)
    """
    # 定义点A和点B的坐标
    xA, yA, zA = A
    xB, yB, zB = B

    # 计算向量AB的坐标差
    dx = xB - xA
    dy = yB - yA
    dz = zB - zA

    # 计算向量AB的长度
    length = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    # 计算单位向量AB的坐标
    unit_vector = (dx / length, dy / length, dz / length)
    return unit_vector

def process_dict( data):
    if isinstance(data, dict) and '__type__' in data and '__value__' in data:
        return data['__value__']
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) and '__type__' in value and '__value__' in value:
                data[key] = process_dict(value)
            else:
                process_dict(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], dict) and '__type__' in data[i] and '__value__' in data[i]:
                data[i] = process_dict(data[i])
            else:
                process_dict(data[i])
def creatItemDict(newItemName,newAuxValue,count):
    reItem = {
        'newItemName': newItemName,
        'count': count,
        'newAuxValue': newAuxValue,
        'enchantData': [], 'durability': 0, 'extraId': '',
        'customTips': '', 'modEnchantData': [], 'itemName': 0,
        'auxValue': 0, 'showInHand': True, 'userData': None
    }
    return reItem

def playMusic(music,pos,volume,p,loop,id = None):
    ss = serverApi.GetSystem(com.modName,com.ssname)
    data = {}
    data['music']  =music
    data['pos']  =pos
    data['p']  =p
    data['volume']  =volume
    data['loop']  =loop
    if id is None:
        ss.BroadcastToAllClient("playerMusic",data)
    else:
        ss.NotifyToClient(id,"playerMusic",data)

def setNeastPostProcess(postName,isOpen = True,id = None):
    """
    服务端直接设置自定义后处理效果
    postName:常见的有[scanmapDemo,oldtvDemo]
    isOpen:是否开启
    id:填入则指定id客户端接收

    """
    ss = serverApi.GetSystem(com.modName,com.ssname)
    data = {}
    data['postName'] = postName
    data['isOpen'] = isOpen
    if id is None:
        ss.BroadcastToAllClient("setNeastPostProcess",data)
    else:
        ss.NotifyToClient(id,"setNeastPostProcess",data)
def getHopperOutPos(pos,dimId):
    x,y,z = pos
    dPosDict = {0: [0, -1, 0], 1: [0, 1, 0], 2: [0, 0, -1], 3: [0, 0, 1], 4: [-1, 0, 0], 5: [1, 0, 0]}
    comp = compFactory.CreateBlockState(serverApi.GetLevelId())
    dir = comp.GetBlockStates((x, y, z), dimId).get('facing_direction')
    if dir is None:return None
    dx, dy, dz = dPosDict[dir]
    return (x + dx, y + dy, z + dz)

def getMaxStackSize(itemDict):
    if not itemDict:return None
    comp = serverApi.GetEngineCompFactory().CreateItem(serverApi.GetLevelId())
    return comp.GetItemBasicInfo(itemDict['newItemName'],itemDict['newAuxValue'])['maxStackSize']
def getAuxFromRot(rot,type = 4):
    if type == 4:
        rot_y  =rot[1]
        auxDict = {
            (45, 135): 3,
            (0, 45): 2,
            (-45, 0): 2,
            (135, 180): 0,
            (-180, -135): 0,
            (-135, -45): 1,
        }

        for key in auxDict:
            if key[0] <= rot_y <= key[1]:return auxDict[key]
        return 0
def ToListenEvent(sys,listenDict,EN = EN,ESN = ESN):#type:(dcit[list]) -> None
    """
    快速监听
    sys:系统名
    listenDict:监听信息
    EN，ESN监听来自何处的事件，默认服务基类
    """
    for evname in listenDict:
        for fun in listenDict[evname]:
            sys.ListenForEvent(EN, ESN, evname, sys, fun)

def playParticles(particleName,pos,rotation,id = None):
    """
    播放原版粒子
    """
    ss = serverApi.GetSystem(com.modName,com.ssname)
    data = {}
    data['rotation']  =rotation
    data['pos']  =pos
    data['particleName']  =particleName
    if id is None:
        ss.BroadcastToAllClient("playParticles",data)
    else:
        ss.NotifyToClient(id,"playParticles",data)


def setBlockMolangValue(dimId,pos,molang,value,id = None):
    """
    服务端直接设置客户端方块实体的molang
    id：默认向所有客户端均设置
    """
    ss = serverApi.GetSystem(com.modName, com.ssname)
    data = {}
    data['dimId'] = dimId
    data['pos'] = pos
    data['molang'] = molang
    data['value'] = value
    if id:
        ss.NotifyToClient(id,"setBlockMolangValue",data)
    else:
        ss.BroadcastToAllClient('setBlockMolangValue',data)

def setEntityMolangValue(eid,molang,value,id = None):
    """
    服务端直接设置客户端实体的molang
    id：默认向所有客户端均设置
    """
    ss = serverApi.GetSystem(com.modName, com.ssname)
    data = {}

    data['eid'] = eid
    data['molang'] = molang
    data['value'] = value
    if id:
        ss.NotifyToClient(id,"setEntityMolangValue",data)
    else:
        ss.BroadcastToAllClient('setEntityMolangValue',data)

def myPrintPopOn(playerId,childMessge,c_c,titile,t_c):
    comp = serverApi.GetEngineCompFactory().CreateGame(playerId)
    comp.SetOnePopupNotice(playerId, "§"+t_c+ titile, "§"+c_c+ childMessge )

enchanName={
0:'保护',
1:'火焰保护',
 2:'摔落保护',
3:'爆炸保护',
 4:'弹射物保护',
5: '荆棘',
6:'水下呼吸',
 7: '深海探索者',
8:'水下速掘',
 9:'锋利',
10:'亡灵杀手',
11:'节肢杀手',
12:'击退',
 13:'火焰附加',
14:'抢夺',
15:'效率',
16:'精准采集',
17:'耐久',
18:'时运',
19:'力量',
 20:'冲击',
21:'火矢',
 22:'无限',
 23:'海之眷顾',
24:'饵钓',
25:'冰霜行者',
26:'经验修补',
27:'绑定诅咒',
28:'消失诅咒',
29:'穿刺',
30:'激流',
31:'忠诚',
 32:'引雷',
 33:'多重射击',
34:'穿透',
 35:'快速装填',
36:'灵魂疾行',

 255:'自定义附魔'
}

def getDetailItemLabel(itemDict,emc,inItemEmc = 0):
    """
    以文本的形式
    返回物品的详细信息
    """
    zhName = \
    Level.Item.GetItemBasicInfo(itemDict['newItemName'], itemDict['newAuxValue'], bool(itemDict.get('enchantData')))[
        'itemName']

    enchanData = itemDict.get('enchantData', [])
    ench_t = ''
    for i in enchanData:
        enchName = enchanName.get(i[0])
        if enchName: ench_t += enchName + " {}\n".format(i[1])

    in_emcLable = ""
    if inItemEmc > 0: in_emcLable = "\n储存emc:{}".format(round(inItemEmc,2))
    t = "{}\n{}{}emc:{}{}".format(zhName, ench_t, getShulkerBoxItemZh(itemDict), round(emc,2), in_emcLable)
    return t


baseItem = {
'newItemName':'',
'count': 1,
'newAuxValue': 0,
'enchantData': [] , 'durability': 0,  'extraId': '',
'customTips': '',  'modEnchantData': [],
'showInHand': True,'userData':None
}
def getShulkerBoxItemZh(itemDict):
    """
    返回潜影盒内的物品名称
    return : str
    """
    if not itemDict:return ''
    shulker_box = ['minecraft:undyed_shulker_box', 'minecraft:shulker_box']
    if itemDict['newItemName'] not in shulker_box:return ''
    userData = itemDict.get('userData',{})
    if not userData:return ''
    if not userData.get('Items'):return ''
    s = ''
    for itemdata in userData.get('Items'):
        item = baseItem
        item['count'] = itemdata['Count']['__value__']
        item['newItemName'] = itemdata['Name']['__value__']
        Block = itemdata.get('Block',{})
        if not Block or not Block.get('val'):
            item['newAuxValue'] = 0
        else:
            item['newAuxValue'] = Block['val']['__value__']

        zh_name = Level.Item.GetItemBasicInfo(item['newItemName'],item['newAuxValue'])['itemName']
        t = "{} x {}\n".format(zh_name,item['count'])
        s+=t

    return s

# def myPrintPopOn(playerId,childMessge,c_c,titile,t_c):
#     comp = serverApi.GetEngineCompFactory().CreateGame(playerId)
#     # playerId 变量改为具体的玩家Id
#     comp.SetOnePopupNotice(playerId, "§"+t_c+ titile, "§"+c_c+ childMessge )
#todo---------------------------------------------------
def setPlayerIdEmc(pid,emc):
    re = Extra.ExtraData(pid).SetExtraData('transtuteEmc', str(emc))
    if re: return re
    return False
def getPlayerIdEmc(pid):
    re = Extra.ExtraData(pid).GetExtraData('transtuteEmc')
    if re: return float(re)
    return 0.0


def getFootPos(id):
    comp = serverApi.GetEngineCompFactory().CreatePos(id)
    return comp.GetFootPos()


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


def getZhName(itemDict):
    """
    返回物品的中文名称,当有附魔时，会以附魔数字为后缀
    return:zhName_enchanNum_...
    such as : 苹果_[(4,1),(3,2)]
    """
    enchantData = itemDict.get('enchantData')
    comp = serverApi.GetEngineCompFactory().CreateItem(serverApi.GetLevelId())
    baseData = comp.GetItemBasicInfo(itemDict['newItemName'],itemDict['newAuxValue'],bool(enchantData))
    zhName = baseData['itemName']+"_"+str(enchantData)
    return zhName






def getAllEId():
    ed = serverApi.GetEngineActor()
    return ed
def getAllId():
    ids = []
    eids = getAllEId()
    for id in eids:
        ids.append(id)
    ids+=getAllPId()
    return ids
def getEntityDimId(eid):
    comp = serverApi.GetEngineCompFactory().CreateDimension(eid)
    dimID = comp.GetEntityDimensionId()
    return dimID

def getAllowEidFront(pid,r):
    compRot = serverApi.GetEngineCompFactory().CreateRot(pid)
    rot = compRot.GetRot()
    dir = serverApi.GetDirFromRot(rot)
    ppos = getEPos(pid)

    eids = getAllEId()
    allowID = []
    for eid in eids:
        x,y,z = getEPos(eid)
        if math.sqrt((ppos[0]-x)**2+(ppos[1]-y)**2+(ppos[2]-z)**2) < r:
            xa = [dir[0],dir[2]]
            xb = [x-ppos[0],z-ppos[2]]

            dx = xb[0]/math.sqrt(xb[0]**2+xb[1]**2)
            dy = xb[1]/math.sqrt(xb[0]**2+xb[1]**2)
            posB = [ppos[0]+dir[0],ppos[2]+dir[2]]
            posC = [ppos[0]+dx,ppos[2]+dy]

            a = math.sqrt((posB[0]-posC[0])**2+(posC[1]-posB[1])**2)
            if a < math.sqrt(2.0):
                allowID.append(eid)

    return allowID
def creatExplosion(x,y,z,r,isfire,isbreakblock,sourceId,playerId,llid):
    comp = serverApi.GetEngineCompFactory().CreateExplosion(llid)
    comp.CreateExplosion((x, y, z), r, isfire, isbreakblock, sourceId, playerId)
def getEPos( eid):
    return serverApi.GetEngineCompFactory().CreatePos(eid).GetPos()


def getPlayerSCItemId(id):

    comp = serverApi.GetEngineCompFactory().CreateItem(id)
    d = comp.GetPlayerItem(2, 0)
    return d["newItemName"]

def getPlayerSCItemNum(id):

    comp = serverApi.GetEngineCompFactory().CreateItem(id)
    d = comp.GetPlayerItem(2, 0)
    return d["count"]
def getEName( eid):
    comp = serverApi.GetEngineCompFactory().CreateEngineType(eid)
    name = comp.GetEngineTypeStr()
    return name

def setBagPosNum(pid,pos,num):

    comp = serverApi.GetEngineCompFactory().CreateItem(pid)
    comp.SetInvItemNum(pos, num)

def getBagSelectPos(pid):

    comp = serverApi.GetEngineCompFactory().CreateItem(pid)
    bagpos = comp.GetSelectSlotId()
    return  bagpos

def setHealth( eid, health):
    comp = serverApi.GetEngineCompFactory().CreateAttr(eid)
    comp.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, health)
    comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, health)


def getHealth( eid):
    comp = serverApi.GetEngineCompFactory().CreateAttr(eid)
    re = comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
    return re


def creatEntity( self,id, x, y, z):
    ServerSystem = serverApi.GetServerSystemCls()
    entityId = self.CreateEngineEntityByTypeStr(self,id, (x, y, z), (0, 0), 0)


def addblock( id, x, y, z):
    blockDict = {
        'name': id,
        'aux': 5
    }
    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(0)
    comp.SetBlockNew((x, y, z), blockDict, 0, 0)


def getblockId( X, Y, Z, llid):
    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(llid)
    bd = comp.GetBlockNew((X, Y, Z), 0)
    return bd


def killEntity( eid, llid):
    comp = serverApi.GetEngineCompFactory().CreateGame(llid)
    comp.KillEntity(eid)


def getAllPId():
    id = serverApi.GetPlayerList()
    return id


def getEScale( eid):
    comp = serverApi.GetEngineCompFactory().CreateScale(eid)
    re = comp.GetEntityScale()
    return re


def setEScale( eid, scale):
    comp = serverApi.GetEngineCompFactory().CreateScale(eid)
    result = comp.SetEntityScale(eid, scale)

def setEpos(x,y,z,eid):
    import mod.server.extraServerApi as serverApi
    comp = serverApi.GetEngineCompFactory().CreatePos(eid)
    comp.SetPos((x, y, z))
def creattree( X, Y, Z, rootid, leafid):
    rh = randX(6, 8)
    for dy in range(rh):
        addblock(rootid, X, Y + dy, Z)
    Y = Y + rh - 4
    for dh in range(1, 5):
        r = 3
        if dh > 2:
            r = 2
        for dx in range(X - r, X + r):
            for dz in range(Z - r, Z + r):
                if getblockId(dx, Y + dh, dz, 0)["name"] == "minecraft:air":
                    addblock(leafid, dx, Y + dh, dz)
                if dx == X - r or dx == X + r or dz == Z - r or dz == Z + r:
                    n = randX(1, 2)
                    if (n == 1):
                        addblock("minecraft:air", dx, Y + dh, dz)


# 矿物生成
def creatOrg( X, Y, Z, r, h, id, num):
    for i in range(num):
        v = randX(2, 6)
        x = randX(-r, r) + X
        y = randX(Y, Y + h)
        z = randX(-r, r) + Z
        for j in range(v):
            for k in range(v):
                for m in range(v):
                    a = randX(1, 10)
                    if (a == 1):
                        import mod.server.extraServerApi as serverApi
                        blockDict = {
                            'name': id,
                            'aux': 5
                        }
                        comp = serverApi.GetEngineCompFactory().CreateBlockInfo(0)
                        comp.SetBlockNew((x + j, y + k, m + z), blockDict, 0, 0)

def creatPosOn(x,y,z,r):
    for i in range(2000):
        X = randX(int(x - r), int(x + r))
        Z = randX(int(z - r), int(z + r))
        Y = randX(y,128)
        while (getblockId(X, Y, Z, 0)["name"] == "minecraft:air" or getblockId(X, Y + 1, Z, 0)[
            "name"] != "minecraft:air"):
            Y = Y + 1
            if (Y > 128):
                Y = -1
                break
        if Y != -1:
            pos = (X,Y,Z)
            return pos
    pos = (randX(x,x+100),randX(y,128),randX(z,z+100))
    return pos



def ceartBlockOn( x, y, z, r, id, num):
    for i in range(num):
        X = randX(int(x - r), int(x + r))
        Z = randX(int(z - r), int(z + r))
        Y = 0
        while (getblockId(X, Y, Z, 0)["name"] != "minecraft:grass" or getblockId(X, Y + 1, Z, 0)[
            "name"] != "minecraft:air"):
            Y = Y + 1
            if (Y > 128):
                Y = -1
                break
        if Y != -1:
            addblock(id, X, Y + 1, Z)
        else:
            num += 1


def randX( a, b):
    import random
    return random.randint(int(a), int(b))

def setAIBlock(eid,isblock,keepDZ):
    """
    :param eid: id
    :param isblock: 是否屏蔽AI
    :param keepDZ: 是否保留动作
    :return: 无
    """
    import mod.server.extraServerApi as serverApi
    comp = serverApi.GetEngineCompFactory().CreateControlAi(eid)
    comp.SetBlockControlAi(False, True)

def setCommond(cmd,pid = None,llid = serverApi.GetLevelId()):
    comp = serverApi.GetEngineCompFactory().CreateCommand(llid)
    comp.SetCommand(cmd,pid,False)
