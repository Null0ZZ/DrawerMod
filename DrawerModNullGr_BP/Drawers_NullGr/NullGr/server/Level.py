
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
compFactory = serverApi.GetEngineCompFactory()

levelId = serverApi.GetLevelId()
Item = compFactory.CreateItem(levelId)
BlockEntity = compFactory.CreateBlockEntityData(levelId)
Game = compFactory.CreateGame(levelId)
Block = compFactory.CreateBlock(levelId)
BlockState = compFactory.CreateBlockState(levelId)
BlockInfo = compFactory.CreateBlockInfo(levelId)
ExtraData = compFactory.CreateExtraData(levelId)
Projectile = compFactory.CreateProjectile(levelId)






