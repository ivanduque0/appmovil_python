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
URL='https://tesis-reconocimiento-facial.herokuapp.com/apertura/'
URL_CONTRATOS="https://tesis-reconocimiento-facial.herokuapp.com/agregarcontratosapi/"
#store = DictStore('datos_usuario')
store = JsonStore('datos_usuario.json')
# store.put('datos_usuario', contrato=CONTRATO, id_usuario=ID_USUARIO)

class seguricel_prototipo(MDApp):

    def build(self):
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
        screen_inicio = Screen(name='inicio')
        #screen_inicio.add_widget(boton_datos_screen)
        btn = Button(
                    #  color =(1, 0, .65, 1),
                     background_normal = 'acceso_principal.png',
                    #  background_down ='down.png',
                     size_hint = (.9, .3),
                     pos_hint = {'center_x': 0.5, 'center_y': 0.8}
                   )
        btn.bind(on_press=self.enviar_peticion_acceso1)
        screen_inicio.add_widget(btn)

        btn2 = Button(
                    #  color =(1, 0, .65, 1),
                     background_normal = 'acceso_vehicular.png',
                    #  background_down ='down.png',
                     size_hint = (.9, .3),
                     pos_hint = {'center_x': 0.5, 'center_y': 0.45}
                   )
        btn2.bind(on_press=self.enviar_peticion_acceso2)
        screen_inicio.add_widget(btn2)
        self.sm.add_widget(screen_inicio)

        ################################################
        # A PARTIR DE AUQI ESTAN LAS COSAS DE LA SCREE #
        #        DONDE SE INTRODUCEN LOS DATOS         #
        ################################################
        self.contrato_seleccionado = ''
        # self.cerrar_dialogo = MDFlatButton(text='cerrar',
        #                                   on_release=self.cerrar_error)
        self.cerrar_dialogo = Builder.load_string(helper.boton_cerrar_dialogo)
        self.cerrar_dialogo.bind(on_release=self.cerrar_error)               
        self.dialogo = MDDialog(
            title='Error',
                     size_hint=(0.7,0.3),
                     buttons=[self.cerrar_dialogo])
        screen = Screen(name='datos')

        self.lista = Builder.load_string(helper.lista_contratos)
        self.lista.bind(on_release=self.lista_contratos)
        screen.add_widget(self.lista)
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
        return root

    def menu_callback(self, text_item):
        self.contrato_seleccionado = text_item
        self.lista.set_item(text_item)
        self.menu.dismiss()

    def guardar_usuario(self, instance):
        if self.contrato_seleccionado and self.id_usuario.text:
            store.put('datos_usuario', contrato=self.contrato_seleccionado, id_usuario=self.id_usuario.text)
            self.sm.current = 'inicio'
        elif self.contrato_seleccionado == '':
            self.dialogo.text='Por favor seleccione un contrato'
            self.dialogo.open()
        elif self.id_usuario.text == '':
            self.dialogo.text ='Por favor introduzca su ID'
            self.dialogo.open()

    def lista_contratos(self, caller):
        self.menu.caller = caller
        self.menu.open()

    def cerrar_error(self, obj):
        self.dialogo.dismiss()

    def introducir_datos(self, obj):
        if self.sm.current == 'inicio':
            contratos_http = requests.get(url=URL_CONTRATOS).json()
            menu_items = [
                {
                    "text": f"{contrato['nombre']}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"{contrato['nombre']}": self.menu_callback(x),
                } for contrato in contratos_http
            ]
            self.menu = MDDropdownMenu(
                items=menu_items,
                width_mult=4
            )
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
        except:
            self.dialogo.text='Primero seleccione un contrato e ingrese un ID valido'
            self.dialogo.open()
        finally:
            if contrato and usuario_id:
                # print(contrato)
                # print(usuario_id)
                requests.post(URL, 
                json={"contrato":contrato,
                    "acceso":"1",
                    "id_usuario":usuario_id})
    
    def enviar_peticion_acceso2(self, obj):
        contrato=''
        usuario_id=''
        try:
            contrato = store.get('datos_usuario')['contrato']
            usuario_id = store.get('datos_usuario')['id_usuario']
        except:
            self.dialogo.text='Primero seleccione un contrato e ingrese un ID valido'
            self.dialogo.open()
        finally:
            if contrato and usuario_id:
                # print(contrato)
                # print(usuario_id)
                requests.post(URL, 
                json={"contrato":contrato,
                    "acceso":"2",
                    "id_usuario":usuario_id})

        

if __name__ == "__main__":
    app = seguricel_prototipo()
    app.run()
