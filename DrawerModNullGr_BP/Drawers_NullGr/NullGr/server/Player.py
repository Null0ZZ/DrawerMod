import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
compFactory = serverApi.GetEngineCompFactory()

PlayerComp = serverApi.GetEngineCompFactory().CreatePlayer
ExtraData = compFactory.CreateExtraData
Item = compFactory.CreateItem
Fly = compFactory.CreateFly
Rot = compFactory.CreateRot
Attr = compFactory.CreateAttr
Hurt = compFactory.CreateHurt
Motion = compFactory.CreateActorMotion
Effect = compFactory.CreateEffect
Pos = compFactory.CreatePos
