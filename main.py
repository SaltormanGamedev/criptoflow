import ccxt
from flet import *
from head.exchangesP import *


class Data_login():
    def __init__(self):
        self.key_master = TextField(text_align='CENTER')
        self.password_master = TextField(text_align=TextAlign.CENTER)
        self.exchange_a = Dropdown(bgcolor=colors.WHITE10)
        self.exchange_b = Dropdown(bgcolor=colors.WHITE10)
        self.user_info = None
        self.DataMaster = MasterExchanges()
        self.progressBar = ProgressBar(value=0,color=colors.GREEN)
        self.text_indbar = Text(value='0%')
        self.busquedaBoton = ElevatedButton(text="Arbitration")
        self.Dataexchanges()
        self.data_wallet = ListView(expand=1,on_scroll=1)
        self.info = None
        # creacion de tabla
        self.data_table = DataTable(columns=[
            DataColumn(Text("MARKET")),
            DataColumn(Text("Exchange A")),
            DataColumn(Text("Price")),
            DataColumn(Text("Exchange B")),
            DataColumn(Text("Price")),
            DataColumn(Text("Profits")),
        ],expand=True)
        dataNull = 'None'
        self.data_table.rows.append(
            DataRow(
                [DataCell(Text(dataNull)), DataCell(Text(dataNull)), DataCell(Text(dataNull)), DataCell(Text(dataNull)),
                 DataCell(Text(dataNull)), DataCell(Text(dataNull))]
            ))

    def DataAr(self, data):
        self.data_table.rows.clear()
        for i in data:
            self.data_table.rows.append(
                DataRow(
                    [DataCell(Text(i[0])), DataCell(Text(i[1])), DataCell(Text(str(float(i[2])))), DataCell(Text(i[3])),
                     DataCell(Text(str(float(i[4])))), DataCell(Text(i[5] + " %"))]
                ))

    def Check_user(self):
        exchange_final = None
        if self.key_master.value != "" and self.password_master.value != '':
            exchange_final = ccxt.binance({
                'options': {
                    'adjustForTimeDifference': True,
                },
                'enableRateLimit': True,
                'apiKey': self.key_master.value,
                'secret': self.password_master.value,
            })
            master=exchange_final.fetch_balance()
            self.info = master.pop('total')
            self.data_wallet.controls.clear()
            for the_key, the_value in self.info.items():
                self.data_wallet.controls.append(Text(str(the_key)+":"+str(the_value)))
            abase="'"
            abaseb='"'

            return True,
        else:
            return False

    def Dataexchanges(self):
        target = self.DataMaster.show_exchanges()
        if len(target) != 0:
            for i in target:
                self.exchange_a.options.append(dropdown.Option(i))
                self.exchange_b.options.append(dropdown.Option(i))


def main(page: Page):
    def Login():
        if app_m.Check_user():
            page.go('/tienda')
    def fastTest():
        page.go('/tienda')

    def Busqueda(e):
        app_m.data_table.rows.clear()
        app_m.text_indbar.value = "Please wait..."
        app_m.progressBar.value = None
        app_m.busquedaBoton.disabled = True
        page.update()
        check_data = app_m.DataMaster.masgerss(app_m.exchange_a.value, app_m.exchange_b.value, app_m, page)
        app_m.busquedaBoton.disabled = False
        app_m.DataAr(check_data)
        page.update()

    page.title = 'Testing'
    app_m = Data_login()

    def route_change(route):
        page.clean()
        if route == '/':
            page.views.append(
                View('/',
                     [AppBar(title=Text("App Samuel")),
                      ElevatedButton(text="presionar", on_click=lambda _: page.go('/tienda'))
                      ]
                     )
            )
        elif page.route == '/tienda':
            app_m.busquedaBoton.on_click = Busqueda
            page.views.append(
                View('/tienda',

                     [AppBar(title=Text("Cripto-flow")),
                      Container(
                          Row(
                              [Column([Text("Exchange A")]),
                                  Column([app_m.exchange_a]),
                               Column([Text("Exchange B")]),
                               Column([app_m.exchange_b]),
                               Column([app_m.busquedaBoton])
                               ]
                          ),
                          alignment=alignment.center
                      ),
                      Container(
                          Column(
                              [app_m.progressBar,
                               ]
                          ),
                          alignment=alignment.center
                      ),
                      Container(
                          Column(
                              [app_m.text_indbar,
                               ]
                          ),
                          alignment=alignment.center
                      ),Container(Column([app_m.data_table]),alignment=alignment.top_center,expand=1),
                      Container(
                          Row([Column([Row([Text("WALLET BINANCE",bgcolor=colors.GREEN)],expand=1)],width=300),
                               Column([app_m.data_wallet],alignment=alignment.center,expand=1)
                               ,]
                              )
                          , expand=True, alignment=alignment.center, adaptive=True
                      ,bgcolor=colors.BLUE),
                      ]
                     , bgcolor=colors.BLACK
                     ))
        else:
            page.views.append(
                View('/Home',
                     [
                         Container(
                             Container(
                                 Column(
                                     [Image(src='images/sx.png',scale=1.5)]
                                 ),
                                 alignment=alignment.center, bgcolor=colors.BLACK
                             ))
                         ,
                         Container(
                             Column(
                                 [Text("API KEY")]
                             ),
                             alignment=alignment.center, bgcolor=colors.BLACK12
                         ),
                         Container(
                             Column(
                                 [
                                     app_m.key_master
                                 ]
                             ),
                             alignment=alignment.center, bgcolor=colors.WHITE10
                         ),
                         Container(
                             Column(
                                 [Text("PASSWORD")]
                             ),
                             alignment=alignment.center, bgcolor=colors.BLACK12
                         ),
                         Container(
                             Column(
                                 [
                                     app_m.password_master
                                 ]
                             ),
                             alignment=alignment.center, bgcolor=colors.WHITE10
                         ),
                         Container(Checkbox(label="remember", value=True),alignment=alignment.center),
                         Container(
                             Column(
                                 [

                                     ElevatedButton(text="Login", bgcolor=colors.BLUE,on_click=lambda _: Login(),scale=1),
                                     ElevatedButton(text=" Test ", bgcolor=colors.BLUE_50,on_click=lambda _: fastTest())
                                 ]
                             ),
                             alignment=alignment.center, bgcolor=colors.BLACK

                         )
                     ], bgcolor=colors.BLACK,padding=90,
                     ))
        page.update()

    def view_pop(view):
        # page.views.pop()
        top_view = page.views[-1]
        page.go(page.route)

    page.title = 'Criptoflow'
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go('/')


app(target=main,view=WEB_BROWSER)
