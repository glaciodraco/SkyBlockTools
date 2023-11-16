from hyPI.hypixelAPI import fileLoader, APILoader, HypixelBazaarParser
from hyPI.constants import BazaarItemID, AuctionItemID, HypixelAPIURL
from hyPI import setAPIKey, setPlayerName
from hyPI.skyCoflnetAPI import SkyConflnetAPI
from typing import Tuple, List

from skyMath import getMedianExponent, parsePrizeList


def getPlotData(itemId:BazaarItemID | AuctionItemID | str, func):
    hist = func(itemId)
    pastRawBuyPrizes = []
    pastRawSellPrizes = []
    pastBuyVolume = []
    pastSellVolume = []
    timestamps = []
    for single in hist.getTimeSlots()[::-1]:
        buyPrice = single.getBuyPrice()
        sellPrice = single.getSellPrice()
        buyVolume = single.getBuyVolume()
        sellVolume = single.getSellVolume()
        pastRawBuyPrizes.append(0 if buyPrice is None else buyPrice)
        pastRawSellPrizes.append(0 if sellPrice is None else sellPrice)
        pastBuyVolume.append(0 if buyVolume is None else buyVolume)
        pastSellVolume.append(0 if sellVolume is None else sellVolume)
        ts = single.getTimestamp()
        time = ts.strftime('%d-%m-%Y-(%H:%M:%S)')
        timestamps.append(time)

    #price
    exp, pricePref = getMedianExponent(pastRawSellPrizes + pastRawBuyPrizes)
    pastBuyPrizes = parsePrizeList(pastRawBuyPrizes, exp)
    pastSellPrizes = parsePrizeList(pastRawSellPrizes, exp)

    #volume
    exp, volumePref = getMedianExponent(pastBuyVolume + pastSellVolume)
    pastBuyVolume = parsePrizeList(pastBuyVolume, exp)
    pastSellVolume = parsePrizeList(pastSellVolume, exp)

    return {
        "time_stamps":timestamps,
        "past_buy_prices":pastBuyPrizes,
        "past_sell_prices":pastSellPrizes,
        "past_raw_buy_prices": pastRawBuyPrizes,
        "past_raw_sell_prices": pastRawSellPrizes,
        "past_buy_volume":pastBuyVolume,
        "past_sell_volume":pastSellVolume,
        "history_object":hist,
        "price_prefix":pricePref,
        "volume_prefix":volumePref,
    }

