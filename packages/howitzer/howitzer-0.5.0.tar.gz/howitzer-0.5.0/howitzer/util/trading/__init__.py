from datetime import datetime, timedelta, timezone, tzinfo
from howitzer.util.date import shortStringFormat
from howitzer.util.trading.indicators import *
from os.path import join
import dateutil.parser as dateparse
import ujson as json
import math
time_index = 0
low_index = 1
high_index = 2
open_index = 3
close_index = 4
volume_index= 5

class Candle:
    def __init__(self, currentData: list, previousClose: float = None):
        self.time = datetime.fromtimestamp(currentData[time_index], tz=timezone.utc)
        self.low = currentData[low_index]
        self.high = currentData[high_index]
        self.open = currentData[open_index]
        self.close = currentData[close_index]
        self.volume = currentData[volume_index]
        self.percent = 100 * (self.close - self.open) / self.open
        self.diff = self.close - self.open
        self.range = self.high - self.low
        self.green = self.close > self.open
        self.red = self.close < self.open
        self.head = self.high - max(self.close, self.open)
        self.tail = min(self.open, self.close) - self.low
        self.body = max(self.close, self.open) - min(self.close, self.open)
        self.twap = (self.close + self.high + self.low) / 3
        self.tr = self.range
        if previousClose is not None:
            self.tr = max(self.range, abs(self.high-previousClose),
                          abs(self.low-previousClose))

    def getTimeStr(self):
        return self.time.strftime("%Y-%m-%dT%H:%M:%S.000Z")


class Chart:
    def __init__(this, _rawCandleData: list):
        this.candles = []
        rawCandleData = _rawCandleData.copy()
        number_of_candles_to_parse = len(rawCandleData)
        for i in range(number_of_candles_to_parse):
            if i < number_of_candles_to_parse - 1:
                this.candles.append(
                    Candle(rawCandleData[i], previousClose=rawCandleData[i+1][close_index]))
            if i == number_of_candles_to_parse - 1:
                this.candles.append(Candle(rawCandleData[i]))

    def Aroon(this, length: int = None, offset: int = 0):
        # offset added to match trading view
        targetTimeFrame = this.PreProcess(length+1, offset)
        return Aroon(candles=targetTimeFrame)

    def EMA(this, length: int = None, lookback: int = math.inf, offset: int = 0, lhoc: str = "close"):
        targetTimeFrame = this.candles[offset:]
        return ema(targetTimeFrame, length, lookback, lhoc)

    def IndexOfHighest(this, length: int = None, offset: int = 0, lhoc: str = "high"):
        targetTimeFrame = this.PreProcess(length, offset)
        return indexOfHighest(candles=targetTimeFrame, lhoc=lhoc)

    def IndexOfLowest(this, length: int = None, offset: int = 0, lhoc: str = "low"):
        targetTimeFrame = this.PreProcess(length, offset)
        return indexOfLowest(candles=targetTimeFrame, lhoc=lhoc)

    def SMA(this, length: int = None, offset: int = 0, lhoc: str = "close"):
        targetTimeFrame = this.PreProcess(length, offset)
        return sma(candles=targetTimeFrame, lhoc=lhoc)

    def PreProcess(this, length, ofs):
        if length is None:
            length = len(this.candles)
        if length > len(this.candles):
            raise "Not enough candles"
        offset = 0 if ofs is None else abs(ofs)
        targetTimeFrame = this.candles[offset: offset + length]
        return targetTimeFrame


def chartFromDataFiles(pathToDataFolder: str, startDate: datetime, endDate: datetime):
    def BLANK_CANDLE():
        return [0, 0, 0, 0, 0, 0]

    stopTime = endDate.timestamp()
    dailyRawCandles = []
    # todo: add days to queu and then deque on multiple threads to get data, sort after the fact
    while(startDate.timestamp() <= stopTime):
        tempDaily = BLANK_CANDLE()
        nextDay = startDate + timedelta(days=1)

        targetFileName = shortStringFormat(startDate) + ".json"
        targetFilePath = join(pathToDataFolder, targetFileName)
        f = open(targetFilePath)

        data = json.load(f)
        # daily logic
        tempDaily[time_index] = dateparse.parse(data[0]["time"]).timestamp()
        tempDaily[open_index] = data[0]["open"]
        for minute in data:
            candleTime = dateparse.parse(minute["time"])
            if candleTime.timestamp() < nextDay.timestamp():
                tempDaily[volume_index] += minute["volume"]
                tempDaily[close_index] = minute["close"]
                tempDaily[high_index] = max(tempDaily[high_index], minute["high"])
                tempDaily[low_index] = min(tempDaily[low_index], minute["low"])

        dailyRawCandles.append(tempDaily)
        startDate = nextDay
        f.close()

    dailyRawCandles.reverse()

    return {
        "daily": Chart(dailyRawCandles)
    }
