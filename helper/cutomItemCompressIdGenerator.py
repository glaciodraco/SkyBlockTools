from hyPI.recipeAPI import RecipeAPI
from pysettings.jsonConfig import JsonConfig
import os
from hyPI.constants import ensureTransNor

RECIPE_MAPPING_PATH = os.path.join(os.path.split(os.path.split(__file__)[0])[0], "src", "config", "customCompressItemIDs.json")
RECIPE_MAPPING = JsonConfig.loadConfig(RECIPE_MAPPING_PATH)



rawSecondLayerIDs = [i for i in RECIPE_MAPPING.getData()]

firstLayer = []



for itemName in RECIPE_MAPPING.getData():
    recipe = RecipeAPI.getRecipeFromID(itemName)
    layerBelow = recipe.getItemInputList()
    print(layerBelow, itemName)

    firstLayer.append({"recipe":[*layerBelow], "result":{"name":itemName, "amount":1}})

    #if layerBelow["name"] in rawSecondLayerIDs:
    #    thirdLayer.append({"recipe":recipe.getItemInputList()[0], "result": {"name":recipe.getID(), "amount":1}})
    #else:
    #    secondLayer.append({"recipe":recipe.getItemInputList()[0], "result":{"name":recipe.getID(), "amount":1}})
    #    firstLayer.append({"recipe":layerBelow, "result":{"name":recipe.getID(), "amount":1}})



print(JsonConfig.prettifyData(firstLayer))
