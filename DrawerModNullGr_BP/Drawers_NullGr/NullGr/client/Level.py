import mod.client.extraClientApi as clientApi
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()

Game = compFactory.CreateGame(levelId)
Item = compFactory.CreateItem(levelId)
Block = compFactory.CreateBlock(levelId)
BlockInfo = compFactory.CreateBlockInfo(levelId)
Recipe = compFactory.CreateRecipe(levelId)
Time = compFactory.CreateTime(levelId)
