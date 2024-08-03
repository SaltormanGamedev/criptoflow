import ccxt
import numpy as np


class MasterExchanges(object):
    def __init__(self):
        self.bid = None
        self.ask = None
        self.iniciobarra = None
        self.estimado_barra = None
        self.book = None
        self.accion = None
        self.clients = None
        self.exchanges = None
        self.symbols = None
        self.ex_a = 'BINANCE'
        self.ex_b = 'YOBIT'
        self.general_p = 0
        self.result_arbit = []
        self.list_exchanges = ccxt.exchanges

    def show_exchanges(self):
        return self.list_exchanges

    def masgerss(self, a, b, app, page):
        app.text_indbar.value = "Please wait..."
        self.result_arbit = []
        self.ex_a = a
        self.ex_b = b
        if self.general_p == 0:
            if (len(self.ex_a) != 0 and len(self.ex_b) != 0):
                if self.ex_a != self.ex_b:
                    total = []
                    total.append(self.ex_a)
                    total.append(self.ex_b)
                    self.exchanges = total
                    self.accion = 1
                else:
                    # print("Exchanged homogeneos")
                    pass
            else:
                print("Verifique campos")
        elif self.general_p == 1:
            self.exchanges = ["Binance", "Bitfinex", "Cex", "Exmo", "Hitbtc",
                              "Kraken", "Kucoin", "Poloniex", "Yobit"]
            self.accion = 1

        if self.accion == 1:
            self.clients = [getattr(ccxt, e.lower())() for e in self.exchanges]
            self.symbols = ["ADA/BTC", "BCH/BTC", "BTG/BTC", "BTS/BTC", "BTC/CLAIM", "DASH/BTC", "DOGE/BTC",
                            "EDO/BTC",
                            "EOS/BTC",
                            "ETC/BTC", "ETH/BTC", "FCT/BTC", "ICX/BTC", "IOTA/BTC", "LSK/BTC", "LTC/BTC",
                            "MAID/BTC", "NEO/BTC",
                            "OMG/BTC", "QTUM/BTC", "STR/BTC", "TRX/BTC", "VEN/BTC", "XEM/BTC", "XLM/BTC", "XMR/BTC",
                            "XRP/BTC",
                            "ZEC/BTC"]
            # self.symbols = ["BTC/USDT"]
            self.iniciobarra = 0.00

            self.estimado_barra = (100 / (len(self.symbols)))
            self.ask = np.zeros((len(self.symbols), len(self.clients)))
            self.bid = np.zeros((len(self.symbols), len(self.clients)))
            for row, symbol in enumerate(self.symbols):
                for col, client in enumerate(self.clients):
                    try:
                        self.book = client.fetch_order_book(symbol)
                        self.ask[row, col] = self.book['asks'][0][0]
                        self.bid[row, col] = self.book['bids'][0][0]
                    except Exception as error:
                        self.ask[row, col] = '0'
                        self.bid[row, col] = '0'

                self.iniciobarra += self.estimado_barra
                app.progressBar.value = self.iniciobarra * 0.01
                app.text_indbar.value = str(int(self.iniciobarra))+"%"
                page.update()

            fee = 0

            for i, symbol in enumerate(self.symbols):
                for j1, exchange1 in enumerate(self.exchanges):
                    for j2, exchange2 in enumerate(self.exchanges):
                        roi = 0
                        if j1 != j2 and self.ask[i, j1] > 0:
                            roi = ((self.bid[i, j2] * (1 - fee / 100)) / (
                                    self.ask[i, j1] * (1 + fee / 100)) - 1) * 100
                            if roi > 0:
                                ganancia = False
                                if round(roi, 2) < 10:
                                    ganancia = True
                                elif round(roi, 2) > 10 and round(roi, 2) < 65:
                                    ganancia = True
                                elif round(roi, 2) > 65:
                                    ganancia = True
                                self.result_arbit.append(
                                    [symbol, exchange1, str(self.ask[i, j1]), exchange2, str(self.bid[i, j2]), str(round(roi, 2)),
                                     ganancia])
            self.result_arbit = sorted(self.result_arbit, reverse=True, key=lambda x: x[5])
        app.text_indbar.value = "0%"
        return self.result_arbit


test_master = MasterExchanges()
