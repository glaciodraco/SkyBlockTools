from hyPI.recipeAPI import RecipeAPI
from pysettings.jsonConfig import JsonConfig
import os
from hyPI.constants import ensureTransNor

RECIPE_MAPPING_PATH = os.path.join(os.path.split(__file__)[0], "src", "config", "baseCompressItemIDs.json")
RECIPE_MAPPING = JsonConfig.loadConfig(RECIPE_MAPPING_PATH)



rawSecondLayerIDs = [i for i in RECIPE_MAPPING.getData()]

firstLayer = []
secondLayer = []
thirdLayer = []


for itemName in RECIPE_MAPPING.getData():
    recipe = RecipeAPI.getRecipeFromID(itemName)
    layerBelow = recipe.getItemInputList()[0]
    if layerBelow["name"] in rawSecondLayerIDs:
        thirdLayer.append({"recipe":recipe.getItemInputList()[0], "result": {"name":recipe.getID(), "amount":1}})
    else:
        secondLayer.append({"recipe":recipe.getItemInputList()[0], "result":{"name":recipe.getID(), "amount":1}})
        firstLayer.append({"recipe":layerBelow, "result":{"name":recipe.getID(), "amount":1}})







print(f"== First Layer({len(firstLayer)}) ==")
for i in firstLayer:
    print(f"\t{i}")
print(f"== Second Layer({len(secondLayer)}) ==")
for i in secondLayer:
    print(f"\t{i}")
print(f"== Third Layer({len(thirdLayer)}) ==")
for i in thirdLayer:
    print(f"\t{i}")
data = {
    "first_layer":firstLayer,
    "second_layer":secondLayer,
    "third_layer":thirdLayer
}
print(JsonConfig.prettifyData(data))
