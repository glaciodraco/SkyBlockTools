from hyPI.APIError import APIConnectionError, NoAPIKeySetException
from hyPI.hypixelAPI import HypixelAPIURL, HypixelBazaarParser, APILoader, fileLoader
from hyPI.skyCoflnetAPI import SkyConflnetAPI
from hyPI.constants import ALL_ENCHANTMENT_IDS
from hyPI import getEnchantmentIDLvl
from pysettings import tk
from pysettings.text import TextColor
from traceback import format_exc
from datetime import datetime
from constants import INFO_LABEL_GROUP as ILG
from settings import Config
from skyMath import parseTimeDelta
from typing import List, Dict

def requestHypixelAPI(master, path=None):
    try:
        if path is not None:
            data = fileLoader(path)
        else:
            data = APILoader(HypixelAPIURL.BAZAAR_URL, Config.SETTINGS_CONFIG["api_key"], Config.SETTINGS_CONFIG["player_name"])
        parser = HypixelBazaarParser(data)
    except APIConnectionError as e:
        TextColor.print(format_exc(), "red")
        tk.SimpleDialog.askError(master, e.getMessage(), "SkyBlockTools")
        return None
    except NoAPIKeySetException as e:
        TextColor.print(format_exc(), "red")
        tk.SimpleDialog.askError(master, e.getMessage(), "SkyBlockTools")
        return None
    return parser
def updateInfoLabel(api:HypixelBazaarParser | None, loaded=False):
    if api is not None:
        ts:datetime = api.getLastUpdated()
        diff = parseTimeDelta(datetime.now()-ts)


        if any([diff.minute, diff.day, diff.hour]):
            ILG.setFg("orange")
        else:
            ILG.setFg("green")
        if loaded:
            ILG.setFg("cyan")

        _timeStr = parseTimeToStr(diff)
        if not loaded:
            ILG.setText(f"SkyBlock-API successful! Last request was [{_timeStr}] ago.")
        else:
            ILG.setText(f"SkyBlock-API was loaded from config! Request was [{_timeStr}] ago.")
    else:
        ILG.setFg("red")
        ILG.setText("SkyBlock-API request failed!")
def modeToBazaarAPIFunc(mode):
    match mode:
        case "hour":
            return SkyConflnetAPI.getBazaarHistoryHour
        case "day":
            return SkyConflnetAPI.getBazaarHistoryDay
        case "week":
            return SkyConflnetAPI.getBazaarHistoryWeek
        case "all":
            return SkyConflnetAPI.getBazaarHistoryComplete
def parseTimeToStr(d)->str:
    out = ""
    av = False
    for t, i in zip([d.day, d.hour, d.minute, d.second], ["d", "h", "m", "s"]):
        if t > 0 or av:
            out += f"{t}{i} "
            av = True
    return out
def prizeToStr(inputPrize:int | float)->str:
    exponent = 0
    neg = inputPrize < 0
    if neg:
        inputPrize = abs(inputPrize)
    prefix = ["coins", "k coins", "m coins", "b coins", "Tr", "Q"]
    while inputPrize > 1000:
        inputPrize = inputPrize/1000
        exponent += 1
        if exponent > 5:
            return f"Overflow {inputPrize}"
    return ("-" if neg else "")+str(round(inputPrize, 1)) +" "+ prefix[exponent]
def getDictEnchantmentIDToLevels()->Dict[str, List[str]]:
    """
    Returns a dictionary to access the valid enchantment levels from raw enchantmentID.

    format: {'ENCHANTMENT_TABASCO': ['ENCHANTMENT_TABASCO_1', 'ENCHANTMENT_TABASCO_2', 'ENCHANTMENT_TABASCO_3']}
    @return:
    """
    typeEnchantment = {}
    for singleEnchantment in ALL_ENCHANTMENT_IDS:
        enchantmentName, _ = getEnchantmentIDLvl(singleEnchantment)
        if enchantmentName in typeEnchantment:
            typeEnchantment[enchantmentName].append(singleEnchantment)
            typeEnchantment[enchantmentName].sort()
        else:
            typeEnchantment[enchantmentName] = [singleEnchantment]
    return typeEnchantment



class BookCraft:
    def __init__(self, data, targetPrice):
        self._book_from_id = data["book_from_id"]
        self._book_from_amount = data["book_from_amount"]
        self._anvil_operation_amount = data["anvil_operation_amount"]
        self._book_from_buy_price = data["book_from_buy_price"]
        self._book_from_buy_volume = data["book_from_buy_volume"]
        self._targetPrice = targetPrice

    def getShowAbleID(self):
        return self.getIDFrom().replace("ENCHANTMENT_", "").lower()
    def getIDFrom(self)->str:
        return self._book_from_id
    def getFromPrice(self):
        return self._book_from_buy_price
    def getFromPriceSingle(self, round_=2):
        return round(self._book_from_buy_price / self.getFromAmount(), round_)
    def getFromAmount(self):
        return self._book_from_amount
    def getSavedCoins(self):
        return self._targetPrice - self.getFromPrice()


    #def __lt__(self, other):
    #    return self.score < other.score







