from kivy.storage.jsonstore import JsonStore
import requests
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivymd.font_definitions import theme_font_styles
import helper
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.screenmanager import ScreenManager, Screen
URL_APERTURA='https://seguricel.up.railway.app/apertura/'
URL_CONFIG="https://seguricel.up.railway.app/dispositivosapimobile/"
URL_LOCAL='http://192.168.0.195:43157/'
#store = DictStore('datos_usuario')
store = JsonStore('datos_usuario.json')

# store.put('datos_usuario', contrato=CONTRATO, id_usuario=ID_USUARIO)

class seguricel_prototipo(MDApp):

    def build(self):
        peatonales=0
        vehiculares=0
        self.id_usuario_cargar=""
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.theme_style = "Dark"
        #self.theme_cls.theme_style = "Light"
        root = FloatLayout()
        self.sm = ScreenManager()

        ################################################
        # A PARTIR DE AUQI ESTAN LAS COSAS DE LA SCREEN#
        #                   DE INICIO                  #
        ################################################
        self.screen_inicio = Screen(name='inicio')
        #screen_inicio.add_widget(boton_datos_screen)
        try:
            peatonales = store.get('accesos')['peatonales']
            vehiculares = store.get('accesos')['vehiculares']
            self.id_usuario_cargar = store.get('datos_usuario')['id_usuario']
        except:
            pass
        for acceso in range(peatonales):
            btn = Button(
                        #  color =(1, 0, .65, 1),
                        #text="Tea and Coffee",
                        background_normal = 'acceso_principal.png',
                        #  background_down ='down.png',
                        size_hint = (.9, .3),
                        pos_hint = {'center_x': 0.5, 'center_y': 0.8},
                        font_size = 70,
                        #color=(206 / 255, 203 / 255, 203 / 255, 1),
                    )
            if acceso+1 == 1:       
                btn.bind(on_press=self.enviar_peticion_acceso1)
            if acceso+1 == 2:       
                btn.bind(on_press=self.enviar_peticion_acceso2)
            self.screen_inicio.add_widget(btn)

        for acceso in range(vehiculares):
            btn2 = Button(
                        #  color =(1, 0, .65, 1),
                        background_normal = 'acceso_vehicular.png',
                        #  background_down ='down.png',
                        size_hint = (.9, .3),
                        pos_hint = {'center_x': 0.5, 'center_y': 0.45}
                    )
            if acceso+3 == 3:       
                btn2.bind(on_press=self.enviar_peticion_acceso3)
            if acceso+3 == 4:       
                btn2.bind(on_press=self.enviar_peticion_acceso4)
            self.screen_inicio.add_widget(btn2)
        self.sm.add_widget(self.screen_inicio)

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
        screen = Screen(name='datos')

        boton_guardar = Builder.load_string(helper.guardar_button)
        boton_guardar.bind(on_press=self.guardar_usuario)
        screen.add_widget(boton_guardar)
        self.id_usuario = Builder.load_string(helper.id_usuario_input)
        screen.add_widget(self.id_usuario)
        self.sm.add_widget(screen)

        boton_datos_screen = Builder.load_string(helper.boton_screen_datos)
        boton_datos_screen.bind(on_press=self.introducir_datos)
        root.add_widget(self.sm)
        root.add_widget(boton_datos_screen)
        if not self.id_usuario_cargar:
            self.sm.current = 'datos'
        # else:
        #     self.id_usuario.text = self.id_usuario_cargar
        return root

    def guardar_usuario(self, instance):
        if self.id_usuario.text:
            accesosPeatonales=0
            accesosVehiculares=0
            contrato=''
            try:
                #contrato_http = requests.get(url=f"{URL_CONFIG}{self.id_usuario.text}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                accesos_http = requests.post(url=f"{URL_CONFIG}{self.id_usuario.text}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                for dispositivo in accesos_http:
                    if 'peatonal' in dispositivo['descripcion'].lower():
                        accesosPeatonales=accesosPeatonales+1
                        if contrato == '':
                            contrato= dispositivo['contrato']
                    elif 'vehicular' in dispositivo['descripcion'].lower():
                        accesosVehiculares=accesosVehiculares+1
                        if contrato == '':
                            contrato= dispositivo['contrato']
                store.put('datos_usuario', contrato=contrato, id_usuario=self.id_usuario.text)
                store.put('accesos', vehiculares=accesosVehiculares,peatonales=accesosPeatonales)
                
                for acceso in range(accesosPeatonales):
                    btn = Button(
                                #  color =(1, 0, .65, 1),
                                #text="Tea and Coffee",
                                background_normal = 'acceso_principal.png',
                                #  background_down ='down.png',
                                size_hint = (.9, .3),
                                pos_hint = {'center_x': 0.5, 'center_y': 0.8},
                                font_size = 70,
                                #color=(206 / 255, 203 / 255, 203 / 255, 1),
                            )
                    if acceso+1 == 1:       
                        btn.bind(on_press=self.enviar_peticion_acceso1)
                    if acceso+1 == 2:       
                        btn.bind(on_press=self.enviar_peticion_acceso2)
                    self.screen_inicio.add_widget(btn)

                for acceso in range(accesosVehiculares):
                    btn2 = Button(
                                #  color =(1, 0, .65, 1),
                                background_normal = 'acceso_vehicular.png',
                                #  background_down ='down.png',
                                size_hint = (.9, .3),
                                pos_hint = {'center_x': 0.5, 'center_y': 0.45}
                            )
                    if acceso+3 == 3:       
                        btn2.bind(on_press=self.enviar_peticion_acceso3)
                    if acceso+3 == 4:       
                        btn2.bind(on_press=self.enviar_peticion_acceso4)
                    self.screen_inicio.add_widget(btn2)
                #self.sm.add_widget(self.screen_inicio)
                self.id_usuario_cargar = self.id_usuario.text
                self.id_usuario.text = ""
                self.sm.current = 'datos'  
            except:
                self.dialogo.text='Fallo al conectar con el servidor'
                self.dialogo.open()
            self.sm.current = 'inicio'
        elif self.id_usuario.text == '':
            self.dialogo.text ='Por favor introduzca su ID'
            self.dialogo.open()


    def cerrar_error(self, obj):
        self.dialogo.dismiss()

    def introducir_datos(self, obj):
        if self.sm.current == 'inicio' or not self.id_usuario_cargar:
            self.sm.current = 'datos'  
        else:
            self.sm.current = 'inicio'


    # def abrir_acceso(self, instance):
    #     requests.post(URL, 
    #     json={"contrato":CONTRATO,
    #         "acceso":"1",
    #             "id_usuario":ID_USUARIO})
    #     print('accion')
    def enviar_peticion_acceso1(self, obj):
        contrato=''
        usuario_id=''
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            if contrato and usuario_id:
                try:
                    #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                    requests.post(url=f"{URL_LOCAL}{usuario_id}/1/seguricel_wifi_activo", timeout=3)
                except:
                    try:
                        requests.post(URL_APERTURA, 
                        json={"contrato":contrato,
                            "acceso":"1",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                    except:
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except:
            self.dialogo.text='Primero seleccione un contrato e ingrese un ID valido'
            self.dialogo.open()
    
    def enviar_peticion_acceso2(self, obj):
        contrato=''
        usuario_id=''
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            if contrato and usuario_id:
                try:
                    #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                    requests.post(url=f"{URL_LOCAL}{usuario_id}/2/seguricel_wifi_activo", timeout=3)
                except:
                    try:
                        requests.post(URL_APERTURA, 
                        json={"contrato":contrato,
                            "acceso":"2",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                    except:
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except:
            self.dialogo.text='Primero seleccione un contrato e ingrese un ID valido'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
    
    def enviar_peticion_acceso3(self, obj):
        contrato=''
        usuario_id=''
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            if contrato and usuario_id:
                try:
                    #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                    requests.post(url=f"{URL_LOCAL}{usuario_id}/2/seguricel_wifi_activo", timeout=3)
                except:
                    try:
                        requests.post(URL_APERTURA, 
                        json={"contrato":contrato,
                            "acceso":"2",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                    except:
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except:
            self.dialogo.text='Primero seleccione un contrato e ingrese un ID valido'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)

    def enviar_peticion_acceso4(self, obj):
        contrato=''
        usuario_id=''
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
            if contrato and usuario_id:
                try:
                    #requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                    requests.post(url=f"{URL_LOCAL}{usuario_id}/2/seguricel_wifi_activo", timeout=3)
                except:
                    try:
                        requests.post(URL_APERTURA, 
                        json={"contrato":contrato,
                            "acceso":"2",
                            "id_usuario":usuario_id},auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=3)
                    except:
                        self.dialogo.text='No fue posible enviar la peticion'
                        self.dialogo.open()
        except:
            self.dialogo.text='Primero seleccione un contrato e ingrese un ID valido'
            self.dialogo.open()
            
                # print(contrato)
                # print(usuario_id)
                
if __name__ == "__main__":
    app = seguricel_prototipo()
    app.run()
