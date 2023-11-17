from hyPI.APIError import APIConnectionError, NoAPIKeySetException
from hyPI.hypixelAPI import HypixelAPIURL, HypixelBazaarParser, APILoader
from hyPI.skyCoflnetAPI import SkyConflnetAPI
from pysettings import tk
from pysettings.text import TextColor
from traceback import format_exc
from datetime import datetime
from constants import INFO_LABEL_GROUP as ILG
from settings import Config


def requestHypixelAPI(master):
    try:
        parser = HypixelBazaarParser(
            #fileLoader(r"C:\Users\langh\Desktop\bz_test.txt") # temp
            APILoader(HypixelAPIURL.BAZAAR_URL, Config.SETTINGS_CONFIG["api_key"], Config.SETTINGS_CONFIG["player_name"])
        )
    except APIConnectionError as e:
        TextColor.print(format_exc(), "red")
        tk.SimpleDialog.askError(master, e.getMessage(), "SkyBlockTools")
        return None
    except NoAPIKeySetException as e:
        TextColor.print(format_exc(), "red")
        tk.SimpleDialog.askError(master, e.getMessage(), "SkyBlockTools")
        return None
    return parser

def updateInfoLabel(api):
    if api is not None:
        ts:datetime = api.getLastUpdated()
        ILG.setFg("green")
        ILG.setText(f"SkyBlock-API successful! Last request: {ts.strftime('%H:%M:%S')}")
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



def prizeToStr(inputPrize:int | float)->str:
    exponent = 0
    prefix = ["coins", "k coins", "m coins", "b coins", "Tr", "Q"]
    while inputPrize > 1000:
        inputPrize = inputPrize/1000
        exponent += 1
        if exponent > 5:
            return f"Overflow {inputPrize}"
    return str(round(inputPrize, 1)) +" "+ prefix[exponent]