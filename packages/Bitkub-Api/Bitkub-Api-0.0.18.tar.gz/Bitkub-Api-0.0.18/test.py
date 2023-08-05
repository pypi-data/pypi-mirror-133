from Bitkub_Api.bitkub_api import Bitkub
import time


api_key = 'c7665571dabaccc585c91673a9cb5401'
api_secret = b'a2f0a90053823a32acf7748f6b4b0057'

bitkub = Bitkub(api_key, api_secret)

print(bitkub.tradingview("BTC_THB", "1", int(time.time() - 100), int(time.time())))
