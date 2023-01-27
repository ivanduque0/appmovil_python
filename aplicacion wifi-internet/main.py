from kivy.storage.jsonstore import JsonStore
import requests
import threading
from kivy.clock import Clock, mainthread
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivymd.font_definitions import theme_font_styles
import helper
from kivy.lang import Builder
#from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
from kivymd.uix.selectioncontrol import MDSwitch
# from plyer import wifi
from kivy.uix.popup import Popup
import time
from able import BluetoothDispatcher, Permission, require_bluetooth_enabled
from jnius import autoclass
#from jnius import autoclass
# from kivy.uix.screenmanager import ScreenManager, Screen

URL_API='https://webseguricel.up.railway.app/'
#store = DictStore('datos_usuario')
store = JsonStore('datos_usuario.json')
# store.put('datos_usuario', contrato=CONTRATO, id_usuario=ID_USUARIO)

class Dispatcher(BluetoothDispatcher):
    @property
    def service(self):
        return autoclass("org.test.seguricelapp.ServiceAble")

    @property
    def activity(self):
        return autoclass("org.kivy.android.PythonActivity").mActivity

    # Need to turn on the adapter, before service is started
    @require_bluetooth_enabled
    def start_service(self):
        uuid = store.get('accesos')['beacon_uuid']
        self.service.start(
            self.activity,
            uuid
            # Pass UUID to advertise
            
        )
        MDApp.get_running_app().stop()  # Can close the app, service will continue running

    # def stop_service(self):
    #     self.service.stop(self.activity)

class seguricel_prototipo(MDApp):

    def build(self):
        self.ble_dispatcher = Dispatcher(
            # This app does not use device scanning,
            # so the list of required permissions can be reduced
            runtime_permissions=[
                Permission.BLUETOOTH_CONNECT,
                Permission.BLUETOOTH_ADVERTISE,
                Permission.ACCESS_FINE_LOCATION,
            ]
        )
        self.hilopuertaabierta = threading.Thread(target=self.puertaAbierta, daemon=True)
        self.killThread=False
        self.cambiarDatosPtaAbierta=False
        self.cambiarDatosFeedback=False
        self.corriendofeedback=False
        self.cerradoPopUpPtaAbierta=True
        window_sizes=Window.size
        self.fontSizeAccesos ="30sp"
        peatonales=0
        vehiculares=0
        self.id_usuario_cargar=""
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.theme_style = "Dark"
        #self.theme_cls.theme_style = "Light"
        root = FloatLayout()
        self.sm = ScreenManager()
        self.contratos=[]
        self.cerrarpopup=False
        ################################################
        # A PARTIR DE AUQI ESTAN LAS COSAS DE LA SCREEN#
        #                   DE INICIO                  #
        ################################################
        self.screen_inicio = Screen(name='inicio')
        self.screen_entradas = Screen(name='entradas')
        self.screen_salidas = Screen(name='salidas')
        self.screen_espera = Screen(name='espera')

        self.layout_inicio = GridLayout(cols=1, spacing=30, size_hint=(None,None))
        self.layout_inicio.bind(minimum_height=self.layout_inicio.setter('height'),
        minimum_width=self.layout_inicio.setter('width'))
        self.tamano_x=window_sizes[0]*0.9
        self.tamano_y=self.tamano_x*180/300
        btn3 = Button(
                    #  color =(1, 0, .65, 1),
                    #background_normal = 'acceso_principal.png',
                    #  background_down ='down.png',
                     #size_hint = (.9, .3),
                     #pos_hint = {'center_x': 0.5, 'center_y': 0.8},
                     size_hint = (None, None),
                     text='ENTRAR',
                     size=(self.tamano_x, self.tamano_y),
                     font_size = "50sp",
                   )
        btn3.bind(on_press=self.cambiar_entradas)
        #self.screen_inicio.add_widget(btn3)
        self.layout_inicio.add_widget(btn3)

        btn4 = Button(
                    #  color =(1, 0, .65, 1),
                     #background_normal = 'acceso_vehicular.png',
                    #  background_down ='down.png',
                     #size_hint = (.9, .3),
                     #pos_hint = {'center_x': 0.5, 'center_y': 0.45},
                     size_hint = (None, None),
                     text='SALIR',
                     size=(self.tamano_x, self.tamano_y),
                     font_size = "50sp",
                   )
        btn4.bind(on_press=self.cambiar_salidas)
        #self.screen_inicio.add_widget(btn4)
        self.layout_inicio.add_widget(btn4)

        btn6= Builder.load_string(helper.boton_bluetooth)
        btn6.size_hint = (None, None)
        btn6.size=(self.tamano_x, self.tamano_y)
        btn6.font_size="50sp"
        btn6.text = 'ABRIR CON\nBLUETOOTH'

        # btn5 = Button(
        #             #  color =(1, 0, .65, 1),
        #              #background_normal = 'acceso_vehicular.png',
        #             #  background_down ='down.png',
        #              #size_hint = (.9, .3),
        #              #pos_hint = {'center_x': 0.5, 'center_y': 0.25},
        #              size_hint = (None, None),
        #              text='ABRIR CON\nBLUETOOTH',
        #              size=(self.tamano_x, self.tamano_y),
        #              font_size = "50sp",
        #            )
        # btn5.bind(on_press=app.ble_dispatcher.start_service())
        #self.screen_inicio.add_widget(btn5)
        self.layout_inicio.add_widget(btn6)

        scrollview_antesabrir = ScrollView(bar_width='2dp', smooth_scroll_end=10, 
        size_hint=(.9, .9),
        pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        scrollview_antesabrir.add_widget(self.layout_inicio)
        self.screen_inicio.add_widget(scrollview_antesabrir)  
        self.sm.add_widget(self.screen_inicio)
        self.sm.add_widget(self.screen_entradas)
        self.sm.add_widget(self.screen_salidas)
        self.sm.add_widget(self.screen_espera)

        #screen_inicio.add_widget(boton_datos_screen)
        self.layout_entradas = GridLayout(cols=1, spacing=30, size_hint=(None,None))
        self.layout_entradas.bind(minimum_height=self.layout_entradas.setter('height'),
                        minimum_width=self.layout_entradas.setter('width'))

        self.layout_salidas = GridLayout(cols=1, spacing=30, size_hint=(None,None))
        self.layout_salidas.bind(minimum_height=self.layout_salidas.setter('height'),
                        minimum_width=self.layout_salidas.setter('width'))

        try:
            contratos = store.get('contratos')['contratos']
            #print(contratos)
            menu_items= [
                    {
                        "text": f"{contrato}",
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=f"{contrato}": self.menu_callback(x),
                    } for contrato in contratos
                ]
        except KeyError:
            store.put('contratos', contratos=[])
            contratos = store.get('contratos')['contratos']
            menu_items = []


        try:
            peatonales = store.get('accesos')['peatonales']
            vehiculares = store.get('accesos')['vehiculares']
            self.servidorLocal=store.get('servidor')['servidor']
            self.id_usuario_cargar = store.get('datos_usuario')['id_usuario']
            self.tamano_x=window_sizes[0]*0.9
            self.tamano_y=self.tamano_x*180/300
        except:
            pass
        try:
            for acceso in peatonales:
                listaPalabras = peatonales[acceso].split(" ")
                descripcionLista = ""
                descripcionPrueba = ""
                for indicePalabra in range(len(listaPalabras)):
                    descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                    if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                        descripcionLista = listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                        descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    
                    if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                btn = Button(
                            color =(1, 0, 0, 1),
                            text=descripcionLista,
                            #background_normal = 'acceso_principal.png',
                            #  background_down ='down.png',
                            size_hint = (None, None),
                            halign='center',
                            #width=1000,
                            #size_hint=(None, None),
                            #pos_hint = {'center_x': 0.5, 'center_y': 0.8},
                            font_size = self.fontSizeAccesos,
                            size=(self.tamano_x, self.tamano_y)
                            #color=(206 / 255, 203 / 255, 203 / 255, 1),
                        )
                if int(acceso) == 1: 
                    btn.bind(on_press=self.enviar_peticion_acceso1)
                if int(acceso) == 2:       
                    btn.bind(on_press=self.enviar_peticion_acceso2)
                if int(acceso) == 3:       
                    btn.bind(on_press=self.enviar_peticion_acceso3)
                if int(acceso) == 4:       
                    btn.bind(on_press=self.enviar_peticion_acceso4)
                if int(acceso) == 5:       
                    btn.bind(on_press=self.enviar_peticion_acceso5)
                if int(acceso) == 6:       
                    btn.bind(on_press=self.enviar_peticion_acceso6)
                if int(acceso) == 7:       
                    btn.bind(on_press=self.enviar_peticion_acceso7)
                if int(acceso) == 8:       
                    btn.bind(on_press=self.enviar_peticion_acceso8)
                if int(acceso) == 9:       
                    btn.bind(on_press=self.enviar_peticion_acceso9)
                if int(acceso) == 10:       
                    btn.bind(on_press=self.enviar_peticion_acceso10)
                if 'entrada' in peatonales[acceso].lower():
                    btn.color = (0, 1, 0, 1)
                    self.layout_entradas.add_widget(btn)
                else:
                    self.layout_salidas.add_widget(btn) 
        except TypeError:
            pass

        try:
            for acceso in vehiculares:
                listaPalabras = vehiculares[acceso].split(" ")
                descripcionLista = ""
                descripcionPrueba = ""
                for indicePalabra in range(len(listaPalabras)):
                    descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                    if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                        descripcionLista = listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                        descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    
                    if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                btn2 = Button(
                            color =(1, 0, 0, 1),
                            text=descripcionLista,
                            halign='center',
                            #background_normal = 'acceso_vehicular.png',
                            #  background_down ='down.png',
                            size_hint=(None, None),
                            size=(self.tamano_x, self.tamano_y),
                            font_size = self.fontSizeAccesos,
                            #size_hint = (.9, .3),
                            #pos_hint = {'center_x': 0.5, 'center_y': 0.45}
                        )
                if int(acceso) == 11:       
                    btn2.bind(on_press=self.enviar_peticion_acceso11)
                if int(acceso) == 12:       
                    btn2.bind(on_press=self.enviar_peticion_acceso12)
                if int(acceso) == 13:       
                    btn2.bind(on_press=self.enviar_peticion_acceso13)
                if int(acceso) == 14:       
                    btn2.bind(on_press=self.enviar_peticion_acceso14)
                if int(acceso) == 15:       
                    btn2.bind(on_press=self.enviar_peticion_acceso15)
                if int(acceso) == 16:       
                    btn2.bind(on_press=self.enviar_peticion_acceso16)
                if int(acceso) == 17:       
                    btn2.bind(on_press=self.enviar_peticion_acceso17)
                if int(acceso) == 18:       
                    btn2.bind(on_press=self.enviar_peticion_acceso18)
                if int(acceso) == 19:       
                    btn2.bind(on_press=self.enviar_peticion_acceso19)
                if int(acceso) == 20:       
                    btn2.bind(on_press=self.enviar_peticion_acceso20)
                

                if 'entrada' in vehiculares[acceso].lower():
                    btn2.color = (0, 1, 0, 1)
                    self.layout_entradas.add_widget(btn2)
                else:
                    self.layout_salidas.add_widget(btn2) 
        except TypeError:
            pass

        scrollview_entradas = ScrollView(bar_width='2dp', smooth_scroll_end=10, 
        size_hint=(.9, .9),
        pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        scrollview_entradas.add_widget(self.layout_entradas)

        scrollview_salidas = ScrollView(bar_width='2dp', smooth_scroll_end=10, 
        size_hint=(.9, .9),
        pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        scrollview_salidas.add_widget(self.layout_salidas)
        
        self.screen_entradas.add_widget(scrollview_entradas)
        self.screen_salidas.add_widget(scrollview_salidas)  

        boton_volver_inicio_salida = Builder.load_string(helper.boton_screen_inicio)
        boton_volver_inicio_salida.bind(on_press=self.volver_inicio)
        self.screen_entradas.add_widget(boton_volver_inicio_salida)
        boton_volver_inicio_entrada = Builder.load_string(helper.boton_screen_inicio)
        boton_volver_inicio_entrada.bind(on_press=self.volver_inicio)
        self.screen_salidas.add_widget(boton_volver_inicio_entrada)
        

        ################################################
        # A PARTIR DE AUQI ESTAN LAS COSAS DE LA SCREE #
        #        DONDE SE INTRODUCEN LOS DATOS         #
        ################################################
        # self.cerrar_dialogo = MDFlatButton(text='cerrar',
        #                                   on_release=self.cerrar_error)
        self.cerrar_dialogo = Builder.load_string(helper.boton_cerrar_dialogo)
        self.cerrar_dialogo.bind(on_release=self.cerrar_error)               
        self.dialogo = MDDialog(
            title='Error',
                     size_hint=(0.7,0.3),
                     buttons=[self.cerrar_dialogo])
        self.screen = Screen(name='datos')
        textoModoInternet = Label(
            text="Aperturas con internet",
            #halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            font_size="20sp"
        )
        self.menu = MDDropdownMenu(
                    items=menu_items,
                    width_mult=4
                )
        
        try:
            modoGuardado = store.get('cambiar_modo')['modoInternet']
        except KeyError:
            store.put('cambiar_modo', modoInternet=False)
            modoGuardado = store.get('cambiar_modo')['modoInternet']
        modoAperturaInternet = MDSwitch(
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            active=modoGuardado,
        )
        modoAperturaInternet.bind(active=self.cambiar_modo)
        self.screen.add_widget(textoModoInternet)
        self.screen.add_widget(modoAperturaInternet)
        boton_guardar = Builder.load_string(helper.guardar_button)
        boton_guardar.bind(on_press=self.guardar_usuario)
        self.screen.add_widget(boton_guardar)
        self.id_usuario = Builder.load_string(helper.id_usuario_input)
        self.screen.add_widget(self.id_usuario)
        self.sm.add_widget(self.screen)

        if len(contratos) >=2:
            self.lista = Builder.load_string(helper.lista_contratos)
            self.lista.bind(on_release=self.lista_contratos)
            self.screen.add_widget(self.lista)
            contrato = store.get('datos_usuario')['contrato']
            self.lista.set_item(contrato)

        boton_datos_screen = Builder.load_string(helper.boton_screen_datos)
        boton_datos_screen.bind(on_press=self.introducir_datos)
        root.add_widget(self.sm)
        root.add_widget(boton_datos_screen)
        if not self.id_usuario_cargar:
            self.sm.current = 'datos'
        else:
            threading.Thread(target=self.feedbacks).start()
            self.hilopuertaabierta.start()
            #self.startServicioFeedback(self.id_usuario_cargar)
        # else:
        #     self.id_usuario.text = 
        
        return root

    @mainthread
    def dialogo_feedback(self):
        self.dialogo.title='¡AVISO!'
        self.dialogo.text='PETICION RECIBIDA POR EL MODULO, ABRIENDO ACCESO'
        self.dialogo.open()

    @mainthread
    def popUpEspera(self, titulo, contenido):
        self.mensajePopUp = Popup(
            title=titulo,
            content=Label(text=contenido,font_size='30sp',halign='center',valign='middle'),
            size_hint=(.9, .6),
            auto_dismiss=False,
            title_align='center',
            title_size= '50sp',
        )
        self.mensajePopUp.open()
        #return mensajePopUp

    @mainthread
    def popUpAviso(self, titulo, contenido):
        self.AvisoPopUp = Popup(
            title=titulo,
            content=Label(text=contenido,font_size='25sp',halign='center',valign='middle'),
            size_hint=(.9, .6),
            auto_dismiss=True,
            on_dismiss=self.flagPopUpPtaABierta,
            title_align='center',
            title_size= '50sp',
        )
        self.AvisoPopUp.open()
        #return mensajePopUp

    def flagPopUpPtaABierta(self,obj):
        self.cerradoPopUpPtaAbierta=True

    @mainthread
    def cerrarPopUPEspera(self):
        self.mensajePopUp.dismiss()
        self.sm.current = 'inicio'
        self.cerrarpopup = False
    
    def popUpAperturaEsperar(self):
        self.popUpEspera('Procesando\nPeticion', 'Por favor espere\nmientras se procesa\nla peticion')
        self.cerrarpopup = True
        # time.sleep(3)
        # self.cerrarPopUPEspera()
    
    def popUpPuertaAbierta(self, acceso):
        self.popUpAviso('!PUERTA ABIERTA¡', f'Usted ha sido el ultimo\nen abrir el acceso\n"{acceso}",\npor favor verifique que\nel acceso se encuentra\ncerrado')
    
    def feedbacks(self):
        idd = store.get('datos_usuario')['id_usuario']
        aperturasjson = requests.get(url=f"{URL_API}aperturasusuarioapi/{idd}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
        cantidadAperturas = len(aperturasjson)
        feedbacksProcesados=0
        self.corriendofeedback = True
        while cantidadAperturas>feedbacksProcesados and not self.killThread:
            try:
                if self.cambiarDatosFeedback:
                    idd = store.get('datos_usuario')['id_usuario']
                    aperturasjson = requests.get(url=f"{URL_API}aperturasusuarioapi/{idd}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                    cantidadAperturas = len(aperturasjson)
                    self.cambiarDatosFeedback=False
                feedbacksProcesados=0
                aperturasjson = requests.get(url=f"{URL_API}aperturasusuarioapi/{idd}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                for apertura in aperturasjson:
                    #print(apertura['abriendo'])
                    #print(apertura['feedback'])
                    if apertura['abriendo'] and not apertura['feedback']:
                        requests.put(url=f"{URL_API}aperturasusuarioapi/{apertura['id']}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5)
                        self.dialogo_feedback()
                        #print("FEEDBACK ENVIADO!")
                        if self.cerrarpopup:
                            self.cerrarPopUPEspera()
                    elif apertura['abriendo'] and apertura['feedback']:
                        feedbacksProcesados+=1
            except Exception as e:
                print(f'{e} - fallo en feedback')
        self.corriendofeedback = False

    def puertaAbierta(self):
        peatonales = store.get('accesos')['peatonales']
        vehiculares = store.get('accesos')['vehiculares']
        contrato = store.get('datos_usuario')['contrato']
        cedula = store.get('datos_usuario')['cedula']
        numerosAccesosPeatonales=[ '1','2','3','4','5','6','7','8','9','10']
        # puertasabiertasjson = requests.get(url=f"{URL_API}puertasabiertasapi/{contrato}/{cedula}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
        while not self.killThread:
            try:
                if self.cerradoPopUpPtaAbierta:
                    if self.cambiarDatosPtaAbierta:
                        peatonales = store.get('accesos')['peatonales']
                        vehiculares = store.get('accesos')['vehiculares']
                        contrato = store.get('datos_usuario')['contrato']
                        cedula = store.get('datos_usuario')['cedula']
                        self.cambiarDatosPtaAbierta= False
                    puertasabiertasjson = requests.get(url=f"{URL_API}puertasabiertasapi/{contrato}/{cedula}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                    for puerta in puertasabiertasjson:
                        acceso=puerta['acceso']
                        # print(f"antes: {type(acceso)}")
                        # print(peatonales)
                        # print(vehiculares)
                        if acceso in numerosAccesosPeatonales:
                            accesoDescripcion = peatonales[acceso]
                        else:
                            accesoDescripcion = vehiculares[acceso]
            
                        self.popUpPuertaAbierta(accesoDescripcion)
                        self.cerradoPopUpPtaAbierta=False
            except Exception as e:
                print(f'{e} - fallo en puerta abierta')
            #time.sleep(5)
    
    # def conectarWifi(self):
    #     param = {}
    #     param['password'] = 'S3gur1c3l753'
    #     wifi.connect('Seguricel', param)

    #     # self.root.add_widget(Popup(
    #     #     title='xd',
    #     #     content=Label(text='alavergaxd'),
    #     #     size_hint=(.8, 1),
    #     #     auto_dismiss=True
    #     # ))


    # def startServicioFeedback(self, argumentt):
        # service = autoclass('org.test.seguricelApp.ServiceFeedback')
        # mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        # argument=argumentt
        # print(f"ARGUMENTO SERVICIO: {argument}")
        # service.start(mActivity, argument)

    # def stopServicioFeedback(self):
        # service = autoclass('org.test.seguricelApp.ServiceFeedback')
        # mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        # service.stop(mActivity)
        
    def menu_callback(self, text_item):
        self.contrato_seleccionado = text_item
        self.lista.set_item(text_item)
        if store.get('datos_usuario')['id_usuario'] != "":
            id_usuario_antiguo = store.get('datos_usuario')['id_usuario']
        if self.contrato_seleccionado != store.get('datos_usuario')['contrato']:
            accesosPeatonalesConDescripcion={}
            accesosVehicularesConDescripcion={}
            try:
                accesos_http = requests.post(url=f"{URL_API}dispositivosapimobile/{self.contrato_seleccionado}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                for dispositivo in accesos_http:
                    if dispositivo['descripcion'] == 'SERVIDOR LOCAL':
                        store.put('servidor', servidor=dispositivo['dispositivo'])
                        self.servidorLocal=dispositivo['dispositivo']
                    else:
                        if 'peatonal' in dispositivo['descripcion'].lower() and ('entrada' in dispositivo['descripcion'].lower() or 'salida' in dispositivo['descripcion'].lower()) and not ('telefono' in dispositivo['descripcion'].lower() or 'rfid' in dispositivo['descripcion'].lower() or 'huella' in dispositivo['descripcion'].lower()):
                            #accesosPeatonales=accesosPeatonales+1
                            descripcion=dispositivo['descripcion']
                            acceso=str(dispositivo['acceso'])
                            #print(descripcion)
                            for letra in descripcion:
                                if letra == '(':
                                    index = descripcion.index('(')
                                    accesosPeatonalesConDescripcion[acceso]=descripcion[:index]
                                    break
                        elif 'vehicular' in dispositivo['descripcion'].lower() and ('entrada' in dispositivo['descripcion'].lower() or 'salida' in dispositivo['descripcion'].lower()) and not ('telefono' in dispositivo['descripcion'].lower() or 'rfid' in dispositivo['descripcion'].lower() or 'huella' in dispositivo['descripcion'].lower()):
                            
                            descripcion=dispositivo['descripcion']
                            acceso=str(dispositivo['acceso'])
                            #print(descripcion)
                            for letra in descripcion:
                                if letra == '(':
                                    index = descripcion.index('(')
                                    accesosVehicularesConDescripcion[acceso]=descripcion[:index]
                                    break
                # print(accesosPeatonales)
                # print(accesosVehiculares)
                store.put('datos_usuario', contrato=self.contrato_seleccionado, id_usuario=id_usuario_antiguo)
                store.put('accesos', vehiculares=accesosVehicularesConDescripcion,peatonales=accesosPeatonalesConDescripcion)
                self.cambiarDatosPtaAbierta =  True
                #store.put('nombre_accesos', vehiculares=descripcion_vehicular,peatonales=descripcion_peatonal)
                #accesos=store.get('accesos')
                #print(accesos)
                window_sizes=Window.size
                self.tamano_x=window_sizes[0]*0.9
                self.tamano_y=self.tamano_x*180/300
                for acceso in accesosPeatonalesConDescripcion:
                    listaPalabras = accesosPeatonalesConDescripcion[acceso].split(" ")
                    descripcionLista = ""
                    descripcionPrueba = ""
                    for indicePalabra in range(len(listaPalabras)):
                        descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                        if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                            descripcionLista = listaPalabras[indicePalabra]

                        if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                            descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                        if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                            descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                        
                        if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                            descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    btn = Button(
                                color =(1, 0, 0, 1),
                                text=descripcionLista,
                                halign='center',
                                #background_normal = 'acceso_principal.png',
                                #  background_down ='down.png',
                                #size_hint = (None, None),
                                size_hint=(None, None),
                                size=(self.tamano_x, self.tamano_y),
                                #width=1000,
                                #size_hint=(None, None),
                                #pos_hint = {'center_x': 0.5, 'center_y': 0.8},
                                font_size = self.fontSizeAccesos,
                                #size=(300, 180)
                                #color=(206 / 255, 203 / 255, 203 / 255, 1),
                            )

                    if acceso == 1: 
                        btn.bind(on_press=self.enviar_peticion_acceso1)
                    if acceso == 2:       
                        btn.bind(on_press=self.enviar_peticion_acceso2)
                    if acceso == 3:       
                        btn.bind(on_press=self.enviar_peticion_acceso3)
                    if acceso == 4:       
                        btn.bind(on_press=self.enviar_peticion_acceso4)
                    if acceso == 5:       
                        btn.bind(on_press=self.enviar_peticion_acceso5)
                    if acceso == 6:       
                        btn.bind(on_press=self.enviar_peticion_acceso6)
                    if acceso == 7:       
                        btn.bind(on_press=self.enviar_peticion_acceso7)
                    if acceso == 8:       
                        btn.bind(on_press=self.enviar_peticion_acceso8)
                    if acceso == 9:       
                        btn.bind(on_press=self.enviar_peticion_acceso9)
                    if acceso == 10:       
                        btn.bind(on_press=self.enviar_peticion_acceso10)

                    if 'entrada' in accesosPeatonalesConDescripcion[acceso].lower():
                        btn.color = (0, 1, 0, 1)
                        self.layout_entradas.add_widget(btn)
                    else:
                        self.layout_salidas.add_widget(btn)

                for acceso in accesosVehicularesConDescripcion:
                    listaPalabras = accesosVehicularesConDescripcion[acceso].split(" ")
                    descripcionLista = ""
                    descripcionPrueba = ""
                    for indicePalabra in range(len(listaPalabras)):
                        descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                        if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                            descripcionLista = listaPalabras[indicePalabra]

                        if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                            descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                        if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                            descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                        
                        if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                            descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    btn2 = Button(
                                #  color =(1, 0, .65, 1),
                                text=descripcionLista,
                                halign='center',
                                #background_normal = 'acceso_vehicular.png',
                                #  background_down ='down.png',
                                #size_hint=(None, None),
                                #size=(300, 180),
                                size_hint=(None, None),
                                size=(self.tamano_x, self.tamano_y),
                                font_size=30,
                                color =(1, 0, 0, 1),
                                #size_hint = (.9, .3),
                                #pos_hint = {'center_x': 0.5, 'center_y': 0.45}
                            )
                    if acceso == 11:       
                        btn2.bind(on_press=self.enviar_peticion_acceso11)
                    if acceso == 12:       
                        btn2.bind(on_press=self.enviar_peticion_acceso12)
                    if acceso == 13:       
                        btn2.bind(on_press=self.enviar_peticion_acceso13)
                    if acceso == 14:       
                        btn2.bind(on_press=self.enviar_peticion_acceso14)
                    if acceso == 15:       
                        btn2.bind(on_press=self.enviar_peticion_acceso15)
                    if acceso == 16:       
                        btn2.bind(on_press=self.enviar_peticion_acceso16)
                    if acceso == 17:       
                        btn2.bind(on_press=self.enviar_peticion_acceso17)
                    if acceso == 18:       
                        btn2.bind(on_press=self.enviar_peticion_acceso18)
                    if acceso == 19:       
                        btn2.bind(on_press=self.enviar_peticion_acceso19)
                    if acceso == 20:       
                        btn2.bind(on_press=self.enviar_peticion_acceso20)
                    if 'entrada' in accesosVehicularesConDescripcion[acceso].lower():
                        btn2.color = (0, 1, 0, 1)
                        self.layout_entradas.add_widget(btn2)
                    else:
                        self.layout_salidas.add_widget(btn2)
                self.id_usuario_cargar = id_usuario_antiguo
                self.id_usuario.text = ""
                self.sm.current = 'inicio'
            except:
                self.dialogo.text='Fallo al conectar con el servidor'
                self.dialogo.open()
                self.sm.current = 'datos'
            
        self.menu.dismiss()

    def lista_contratos(self, caller):
        self.menu.caller = caller
        self.menu.open()

    def cambiar_modo(self, instance, value):
        store.put('cambiar_modo', modoInternet=value)

    def cambiar_entradas(self, instance):
        self.sm.current = 'entradas'
        self.layout_entradas.clear_widgets()
        self.layout_salidas.clear_widgets()
        try:
            peatonales = store.get('accesos')['peatonales']
            vehiculares = store.get('accesos')['vehiculares']
            self.id_usuario_cargar = store.get('datos_usuario')['id_usuario']
            window_sizes=Window.size
            self.tamano_x=window_sizes[0]*0.9
            self.tamano_y=self.tamano_x*180/300
        except:
            pass
        try:
            for acceso in peatonales:
                listaPalabras = peatonales[acceso].split(" ")
                descripcionLista = ""
                descripcionPrueba = ""
                for indicePalabra in range(len(listaPalabras)):
                    descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                    if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                        descripcionLista = listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                        descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    
                    if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                btn = Button(
                            color =(1, 0, 0, 1),
                            text=descripcionLista,
                            halign='center',
                            #background_normal = 'acceso_principal.png',
                            #  background_down ='down.png',
                            size_hint = (None, None),
                            #width=1000,
                            #size_hint=(None, None),
                            #pos_hint = {'center_x': 0.5, 'center_y': 0.8},
                            font_size = self.fontSizeAccesos,
                            size=(self.tamano_x, self.tamano_y)
                            #color=(206 / 255, 203 / 255, 203 / 255, 1),
                        )
                if int(acceso) == 1: 
                    btn.bind(on_press=self.enviar_peticion_acceso1)
                if int(acceso) == 2:       
                    btn.bind(on_press=self.enviar_peticion_acceso2)
                if int(acceso) == 3:       
                    btn.bind(on_press=self.enviar_peticion_acceso3)
                if int(acceso) == 4:       
                    btn.bind(on_press=self.enviar_peticion_acceso4)
                if int(acceso) == 5:       
                    btn.bind(on_press=self.enviar_peticion_acceso5)
                if int(acceso) == 6:       
                    btn.bind(on_press=self.enviar_peticion_acceso6)
                if int(acceso) == 7:       
                    btn.bind(on_press=self.enviar_peticion_acceso7)
                if int(acceso) == 8:       
                    btn.bind(on_press=self.enviar_peticion_acceso8)
                if int(acceso) == 9:       
                    btn.bind(on_press=self.enviar_peticion_acceso9)
                if int(acceso) == 10:       
                    btn.bind(on_press=self.enviar_peticion_acceso10)
                
                if 'entrada' in peatonales[acceso].lower():
                    btn.color = (0, 1, 0, 1)
                    self.layout_entradas.add_widget(btn)
                else:
                    self.layout_salidas.add_widget(btn) 
        except TypeError:
            pass

        try:
            for acceso in vehiculares:
                listaPalabras = vehiculares[acceso].split(" ")
                descripcionLista = ""
                descripcionPrueba = ""
                for indicePalabra in range(len(listaPalabras)):
                    descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                    if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                        descripcionLista = listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                        descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    
                    if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                btn2 = Button(
                            color =(1, 0, 0, 1),
                            text=descripcionLista,
                            halign='center',
                            #background_normal = 'acceso_vehicular.png',
                            #  background_down ='down.png',
                            size_hint=(None, None),
                            size=(self.tamano_x, self.tamano_y),
                            font_size = self.fontSizeAccesos,
                            #size_hint = (.9, .3),
                            #pos_hint = {'center_x': 0.5, 'center_y': 0.45}
                        )
                if int(acceso) == 11:       
                    btn2.bind(on_press=self.enviar_peticion_acceso11)
                if int(acceso) == 12:       
                    btn2.bind(on_press=self.enviar_peticion_acceso12)
                if int(acceso) == 13:       
                    btn2.bind(on_press=self.enviar_peticion_acceso13)
                if int(acceso) == 14:       
                    btn2.bind(on_press=self.enviar_peticion_acceso14)
                if int(acceso) == 15:       
                    btn2.bind(on_press=self.enviar_peticion_acceso15)
                if int(acceso) == 16:       
                    btn2.bind(on_press=self.enviar_peticion_acceso16)
                if int(acceso) == 17:       
                    btn2.bind(on_press=self.enviar_peticion_acceso17)
                if int(acceso) == 18:       
                    btn2.bind(on_press=self.enviar_peticion_acceso18)
                if int(acceso) == 19:       
                    btn2.bind(on_press=self.enviar_peticion_acceso19)
                if int(acceso) == 20:       
                    btn2.bind(on_press=self.enviar_peticion_acceso20)
                

                if 'entrada' in vehiculares[acceso].lower():
                    btn2.color = (0, 1, 0, 1)
                    self.layout_entradas.add_widget(btn2)
                else:
                    self.layout_salidas.add_widget(btn2) 
        except TypeError:
            pass
    
    def cambiar_salidas(self, instance):
        self.sm.current = 'salidas'
        self.layout_entradas.clear_widgets()
        self.layout_salidas.clear_widgets()
        try:
            peatonales = store.get('accesos')['peatonales']
            vehiculares = store.get('accesos')['vehiculares']
            self.id_usuario_cargar = store.get('datos_usuario')['id_usuario']
            window_sizes=Window.size
            self.tamano_x=window_sizes[0]*0.9
            self.tamano_y=self.tamano_x*180/300
        except:
            pass
        try:
            for acceso in peatonales:
                listaPalabras = peatonales[acceso].split(" ")
                descripcionLista = ""
                descripcionPrueba = ""
                for indicePalabra in range(len(listaPalabras)):
                    descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                    if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                        descripcionLista = listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                        descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    
                    if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                btn = Button(
                            color =(1, 0, 0, 1),
                            text=descripcionLista,
                            halign='center',
                            #background_normal = 'acceso_principal.png',
                            #  background_down ='down.png',
                            size_hint = (None, None),
                            #width=1000,
                            #size_hint=(None, None),
                            #pos_hint = {'center_x': 0.5, 'center_y': 0.8},
                            font_size = self.fontSizeAccesos,
                            size=(self.tamano_x, self.tamano_y)
                            #color=(206 / 255, 203 / 255, 203 / 255, 1),
                        )
                if int(acceso) == 1: 
                    btn.bind(on_press=self.enviar_peticion_acceso1)
                if int(acceso) == 2:       
                    btn.bind(on_press=self.enviar_peticion_acceso2)
                if int(acceso) == 3:       
                    btn.bind(on_press=self.enviar_peticion_acceso3)
                if int(acceso) == 4:       
                    btn.bind(on_press=self.enviar_peticion_acceso4)
                if int(acceso) == 5:       
                    btn.bind(on_press=self.enviar_peticion_acceso5)
                if int(acceso) == 6:       
                    btn.bind(on_press=self.enviar_peticion_acceso6)
                if int(acceso) == 7:       
                    btn.bind(on_press=self.enviar_peticion_acceso7)
                if int(acceso) == 8:       
                    btn.bind(on_press=self.enviar_peticion_acceso8)
                if int(acceso) == 9:       
                    btn.bind(on_press=self.enviar_peticion_acceso9)
                if int(acceso) == 10:       
                    btn.bind(on_press=self.enviar_peticion_acceso10)
                
                if 'entrada' in peatonales[acceso].lower():
                    btn.color = (0, 1, 0, 1)
                    self.layout_entradas.add_widget(btn)
                else:
                    self.layout_salidas.add_widget(btn) 
        except TypeError:
            pass

        try:
            for acceso in vehiculares:
                listaPalabras = vehiculares[acceso].split(" ")
                descripcionLista = ""
                descripcionPrueba = ""
                for indicePalabra in range(len(listaPalabras)):
                    descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                    if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                        descripcionLista = listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                        descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                    if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    
                    if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                        descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                btn2 = Button(
                            color =(1, 0, 0, 1),
                            text=descripcionLista,
                            halign='center',
                            #background_normal = 'acceso_vehicular.png',
                            #  background_down ='down.png',
                            size_hint=(None, None),
                            size=(self.tamano_x, self.tamano_y),
                            font_size = self.fontSizeAccesos,
                            #size_hint = (.9, .3),
                            #pos_hint = {'center_x': 0.5, 'center_y': 0.45}
                        )
                if int(acceso) == 11:       
                    btn2.bind(on_press=self.enviar_peticion_acceso11)
                if int(acceso) == 12:       
                    btn2.bind(on_press=self.enviar_peticion_acceso12)
                if int(acceso) == 13:       
                    btn2.bind(on_press=self.enviar_peticion_acceso13)
                if int(acceso) == 14:       
                    btn2.bind(on_press=self.enviar_peticion_acceso14)
                if int(acceso) == 15:       
                    btn2.bind(on_press=self.enviar_peticion_acceso15)
                if int(acceso) == 16:       
                    btn2.bind(on_press=self.enviar_peticion_acceso16)
                if int(acceso) == 17:       
                    btn2.bind(on_press=self.enviar_peticion_acceso17)
                if int(acceso) == 18:       
                    btn2.bind(on_press=self.enviar_peticion_acceso18)
                if int(acceso) == 19:       
                    btn2.bind(on_press=self.enviar_peticion_acceso19)
                if int(acceso) == 20:       
                    btn2.bind(on_press=self.enviar_peticion_acceso20)
                

                if 'entrada' in vehiculares[acceso].lower():
                    btn2.color = (0, 1, 0, 1)
                    self.layout_entradas.add_widget(btn2)
                else:
                    self.layout_salidas.add_widget(btn2) 
        except TypeError:
            pass

    def volver_inicio(self, instance):
        self.sm.current = 'inicio'

    def guardar_usuario(self, instance):
        if self.id_usuario.text:
            accesosPeatonales=0
            accesosVehiculares=0
            contrato=''
            accesosPeatonalesConDescripcion={}
            accesosVehicularesConDescripcion={}
            descripcion_peatonal=[]
            descripcion_vehicular=[]
            contratos=[]
            contrato=""
            try:
                contratos_json=store.get('contratos')['contratos']
                contratos_http = requests.get(url=f"{URL_API}dispositivosapimobile/{self.id_usuario.text}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                
                menu_items = [
                    {
                        "text": f"{contrato['contrato']}",
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=f"{contrato['contrato']}": self.menu_callback(x),
                    } for contrato in contratos_http
                ]
                if len(contratos_json) >= 2:
                    self.screen.remove_widget(self.lista)
                for contrato in contratos_http:
                    contratos.append(contrato['contrato'])
                if contratos:
                    contrato=contratos[0]
                    accesos_http = requests.post(url=f"{URL_API}dispositivosapimobile/{contrato}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                    #print(accesos_http)
                    for dispositivo in accesos_http:
                        if dispositivo['descripcion'] == 'SERVIDOR LOCAL':
                            store.put('servidor', servidor=dispositivo['dispositivo'])
                            self.servidorLocal=dispositivo['dispositivo']
                        else:
                            if 'peatonal' in dispositivo['descripcion'].lower() and ('entrada' in dispositivo['descripcion'].lower() or 'salida' in dispositivo['descripcion'].lower()) and not ('telefono' in dispositivo['descripcion'].lower() or 'rfid' in dispositivo['descripcion'].lower() or 'huella' in dispositivo['descripcion'].lower()):
                                #accesosPeatonales=accesosPeatonales+1
                                descripcion=dispositivo['descripcion']
                                acceso=str(dispositivo['acceso'])
                                #print(descripcion)
                                for letra in descripcion:
                                    if letra == '(':
                                        index = descripcion.index('(')
                                        accesosPeatonalesConDescripcion[acceso]=descripcion[:index]
                                        break
                            elif 'vehicular' in dispositivo['descripcion'].lower() and ('entrada' in dispositivo['descripcion'].lower() or 'salida' in dispositivo['descripcion'].lower()) and not ('telefono' in dispositivo['descripcion'].lower() or 'rfid' in dispositivo['descripcion'].lower() or 'huella' in dispositivo['descripcion'].lower()):
                            
                                descripcion=dispositivo['descripcion']
                                acceso=str(dispositivo['acceso'])
                                #print(descripcion)
                                for letra in descripcion:
                                    if letra == '(':
                                        index = descripcion.index('(')
                                        accesosVehicularesConDescripcion[acceso]=descripcion[:index]
                                        break
                    # print(accesosPeatonales)
                    # print(accesosVehiculares)
                    # try:
                        # self.stopServicioFeedback()
                    # except:
                        # pass
                    #print(f"{URL_API}usuarioindividualporidapi/{contrato}/{self.id_usuario.text}/")
                    informacionUsuario = requests.get(url=f"{URL_API}usuarioindividualporidapi/{contrato}/{self.id_usuario.text}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                    #print(informacionUsuario)
                    store.put('datos_usuario', contrato=contrato, id_usuario=self.id_usuario.text, cedula=informacionUsuario[0]['cedula'], beacon_uuid=informacionUsuario[0]['beacon_uuid'])
                store.put('contratos', contratos=contratos)
                store.put('accesos', vehiculares=accesosVehicularesConDescripcion,peatonales=accesosPeatonalesConDescripcion)
                if not self.hilopuertaabierta.is_alive():
                    self.hilopuertaabierta.start()
                self.cambiarDatosPtaAbierta = True
                self.cambiarDatosFeedback = True
                if not self.corriendofeedback:
                    threading.Thread(target=self.feedbacks).start()
                #self.startServicioFeedback(self.id_usuario.text)
                #store.put('nombre_accesos', vehiculares=descripcion_vehicular,peatonales=descripcion_peatonal)
                #accesos=store.get('accesos')
                #print(accesos)
                window_sizes=Window.size
                self.tamano_x=window_sizes[0]*0.9
                self.tamano_y=self.tamano_x*180/300
                for acceso in accesosPeatonalesConDescripcion:
                    listaPalabras = accesosPeatonalesConDescripcion[acceso].split(" ")
                    descripcionLista = ""
                    descripcionPrueba = ""
                    for indicePalabra in range(len(listaPalabras)):
                        descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                        if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                            descripcionLista = listaPalabras[indicePalabra]

                        if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                            descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                        if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                            descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                        
                        if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                            descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    btn = Button(
                                color =(1, 0, 0, 1),
                                text=descripcionLista,
                                halign='center',
                                #background_normal = 'acceso_principal.png',
                                #  background_down ='down.png',
                                #size_hint = (None, None),
                                size_hint=(None, None),
                                size=(self.tamano_x, self.tamano_y),
                                #width=1000,
                                #size_hint=(None, None),
                                #pos_hint = {'center_x': 0.5, 'center_y': 0.8},
                                font_size = self.fontSizeAccesos,
                                #size=(300, 180)
                                #color=(206 / 255, 203 / 255, 203 / 255, 1),
                            )

                    if acceso == 1: 
                        btn.bind(on_press=self.enviar_peticion_acceso1)
                    if acceso == 2:       
                        btn.bind(on_press=self.enviar_peticion_acceso2)
                    if acceso == 3:       
                        btn.bind(on_press=self.enviar_peticion_acceso3)
                    if acceso == 4:       
                        btn.bind(on_press=self.enviar_peticion_acceso4)
                    if acceso == 5:       
                        btn.bind(on_press=self.enviar_peticion_acceso5)
                    if acceso == 6:       
                        btn.bind(on_press=self.enviar_peticion_acceso6)
                    if acceso == 7:       
                        btn.bind(on_press=self.enviar_peticion_acceso7)
                    if acceso == 8:       
                        btn.bind(on_press=self.enviar_peticion_acceso8)
                    if acceso == 9:       
                        btn.bind(on_press=self.enviar_peticion_acceso9)
                    if acceso == 10:       
                        btn.bind(on_press=self.enviar_peticion_acceso10)

                    if 'entrada' in accesosPeatonalesConDescripcion[acceso].lower():
                        btn.color = (0, 1, 0, 1)
                        self.layout_entradas.add_widget(btn)
                    else:
                        self.layout_salidas.add_widget(btn)

                for acceso in accesosVehicularesConDescripcion:
                    listaPalabras = accesosVehicularesConDescripcion[acceso].split(" ")
                    descripcionLista = ""
                    descripcionPrueba = ""
                    for indicePalabra in range(len(listaPalabras)):
                        descripcionPrueba = descripcionLista + listaPalabras[indicePalabra]
                        if len(descripcionPrueba) / 10 < 1 and indicePalabra == 0:
                            descripcionLista = listaPalabras[indicePalabra]

                        if len(descripcionPrueba) / 10 < 1 and indicePalabra != 0:
                            descripcionLista = descripcionLista + " " + listaPalabras[indicePalabra]

                        if len(descripcionPrueba) / 10 >= 1 and len(descripcionPrueba) / 10 < 2:
                            descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                        
                        if len(descripcionPrueba) / 10 >= 2 and len(descripcionPrueba) / 10 < 3:
                            descripcionLista = descripcionLista + "\n" + listaPalabras[indicePalabra]
                    btn2 = Button(
                                #  color =(1, 0, .65, 1),
                                text=descripcionLista,
                                halign='center',
                                #background_normal = 'acceso_vehicular.png',
                                #  background_down ='down.png',
                                #size_hint=(None, None),
                                #size=(300, 180),
                                size_hint=(None, None),
                                size=(self.tamano_x, self.tamano_y),
                                font_size=30,
                                color =(1, 0, 0, 1),
                                #size_hint = (.9, .3),
                                #pos_hint = {'center_x': 0.5, 'center_y': 0.45}
                            )
                    if acceso == 11:       
                        btn2.bind(on_press=self.enviar_peticion_acceso11)
                    if acceso == 12:       
                        btn2.bind(on_press=self.enviar_peticion_acceso12)
                    if acceso == 13:       
                        btn2.bind(on_press=self.enviar_peticion_acceso13)
                    if acceso == 14:       
                        btn2.bind(on_press=self.enviar_peticion_acceso14)
                    if acceso == 15:       
                        btn2.bind(on_press=self.enviar_peticion_acceso15)
                    if acceso == 16:       
                        btn2.bind(on_press=self.enviar_peticion_acceso16)
                    if acceso == 17:       
                        btn2.bind(on_press=self.enviar_peticion_acceso17)
                    if acceso == 18:       
                        btn2.bind(on_press=self.enviar_peticion_acceso18)
                    if acceso == 19:       
                        btn2.bind(on_press=self.enviar_peticion_acceso19)
                    if acceso == 20:       
                        btn2.bind(on_press=self.enviar_peticion_acceso20)
                    if 'entrada' in accesosVehicularesConDescripcion[acceso].lower():
                        btn2.color = (0, 1, 0, 1)
                        self.layout_entradas.add_widget(btn2)
                    else:
                        self.layout_salidas.add_widget(btn2)
                
                #self.sm.add_widget(self.screen_inicio)
                
                if len(contratos_http) >= 2:
                    self.menu = MDDropdownMenu(
                    items=menu_items,
                    width_mult=4
                    )
                    self.lista = Builder.load_string(helper.lista_contratos)
                    self.lista.bind(on_release=self.lista_contratos)
                    self.screen.add_widget(self.lista)
                    self.lista.set_item(contrato)
                self.id_usuario_cargar = self.id_usuario.text
                self.id_usuario.text = ""
                self.sm.current = 'inicio'
            except Exception as e:
                print(f"{e} - hubo un error al agregar al usuario")
                self.id_usuario_cargar = "reconectando"
                self.dialogo.text='Fallo al conectar con el servidor'
                self.dialogo.open()
                self.sm.current = 'datos'
            
        elif self.id_usuario.text == '':
            self.dialogo.text ='Por favor introduzca su ID'
            self.dialogo.open()

    def cerrar_error(self, obj):
        self.dialogo.dismiss()

    def introducir_datos(self, obj):
        if self.sm.current == 'inicio' or not self.id_usuario_cargar:
            self.sm.current = 'datos'  
        elif self.sm.current == 'entradas' or self.sm.current == 'salidas' :
            self.sm.current = 'datos' 
        elif self.sm.current == 'datos':
            self.sm.current = 'inicio'
        else:
            self.sm.current = 'inicio'


    # def abrir_acceso(self, instance):
    #     requests.post(URL, 
    #     json={"contrato":CONTRATO,
    #         "acceso":"1",
    #             "id_usuario":ID_USUARIO})
    #     print('accion')

    def popUpIntentoAperturaInternet(self):
        self.cerrarPopUPEspera()
        content = GridLayout(cols=1)
        blayout = BoxLayout(spacing=5,orientation='horizontal')
        btnNo = Button(text='NO', size_hint = (.5, 0.7), font_size = "20sp")
        btnSi = Button(text='SI', size_hint = (.5, 0.7), font_size = "20sp")
        blayout.add_widget(btnSi)
        blayout.add_widget(btnNo)
        content.add_widget(Label(text='¿Desea intentarlo\npor internet?', 
                                 font_size='25sp',halign='center',valign='middle', size_hint=(1, .9)))
        content.add_widget(blayout)
        self.popUpIntento = Popup(
                title='No fue posible abrir por WIFI...',
                content=content,
                size_hint=(.9, .6),
                auto_dismiss=False,
                title_align='center',
                title_size= '40sp',
            )
        
        btnSi.bind(on_press=self.verificacionIntentoAperturaInternet)
        btnNo.bind(on_press=self.cerrarPopUpFalloWifi)
        self.popUpIntento.open()

    def cerrarPopUpFalloWifi(self, obj):
        self.popUpIntento.dismiss()
        self.popUpIntento=None

    def verificacionIntentoAperturaInternet(self, obj):
        self.cerrarPopUpFalloWifi('a')
        content = GridLayout(cols=1)
        blayout = BoxLayout(spacing=5,orientation='horizontal')
        btnNo = Button(text='NO', size_hint = (.5, 0.7), font_size = "20sp")
        btnSi = Button(text='SI', size_hint = (.5, 0.7), font_size = "20sp")
        blayout.add_widget(btnSi)
        blayout.add_widget(btnNo)
        content.add_widget(Label(text='¿Seguro que desea\nabrir por internet?', 
                                 font_size='30sp',halign='center',valign='middle', size_hint=(1, .9)))
        content.add_widget(blayout)
        self.popUpIntento = Popup(
                title='¡AVISO!',
                content=content,
                size_hint=(.9, .6),
                auto_dismiss=False,
                title_align='center',
                title_size= '50sp',
            )
        btnSi.bind(on_press=self.IntentarEnviarPeticionInternet)
        btnNo.bind(on_release=self.cerrarPopUpFalloWifi)
        self.popUpIntento.open()

    def IntentarEnviarPeticionInternet(self, obj):
        self.cerrarPopUpFalloWifi('a')
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            requests.post(url=f"{URL_API}apertura/", 
            json={"contrato":contrato,
                "acceso":self.accesoIntento,
                "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
            if not self.corriendofeedback:
                threading.Thread(target=self.feedbacks).start()
        except:
            self.cerrarPopUPEspera()
            self.dialogo.text='No fue posible enviar la peticion'
            self.dialogo.open()

    def enviar_peticion_acceso1(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/1/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='1'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"1",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
    
    def enviar_peticion_acceso2(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/2/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='2'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"2",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso3(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/3/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='3'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"3",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)

    def enviar_peticion_acceso4(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/4/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='4'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"4",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)

    def enviar_peticion_acceso5(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/5/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='5'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"5",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)

    def enviar_peticion_acceso6(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/6/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='6'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"6",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso7(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/7/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='7'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"7",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso8(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/8/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='8'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"8",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso9(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/9/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='9'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"9",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso10(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/10/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='10'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        print('khe')
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"10",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso11(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/11/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='11'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"11",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso12(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/12/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='12'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"12",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso13(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/13/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='13'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"13",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso14(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/14/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='14'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"14",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso15(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/15/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='15'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"15",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso16(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/16/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='16'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"16",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso17(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/17/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='17'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"17",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso18(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/18/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='18'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"18",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso19(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/19/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='19'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"19",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso20(self, obj):
        contrato=''
        usuario_id=''
        threading.Thread(target=self.popUpAperturaEsperar).start()
        self.sm.current = 'espera'
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            modoInternet = store.get('cambiar_modo')['modoInternet']
            if contrato and usuario_id:
                if not modoInternet:
                    try:
                        #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                        requests.post(url=f"{self.servidorLocal}:43157/{usuario_id}/20/seguricel_wifi_activo", timeout=3)
                        self.cerrarPopUPEspera()
                    except:
                        self.accesoIntento='20'
                        self.popUpIntentoAperturaInternet()
                        # self.dialogo.text='No fue posible enviar la peticion'
                        # self.dialogo.open()
                    finally:
                        pass
                        #self.cerrarPopUPEspera()
                else:
                    try:
                        requests.post(url=f"{URL_API}apertura/", 
                        json={"contrato":contrato,
                            "acceso":"20",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                        if not self.corriendofeedback:
                            threading.Thread(target=self.feedbacks).start()
                    except:
                        self.cerrarPopUPEspera()
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except Exception as e:
            self.dialogo.text=f'Hubo un error al intentar enviar la solicitud: {e}'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)

    
    

                
if __name__ == "__main__":
    app = seguricel_prototipo()
    app.run()
    app.killThread = True
