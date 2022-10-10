from kivy.storage.jsonstore import JsonStore
import requests
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivymd.font_definitions import theme_font_styles
import helper
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.screenmanager import ScreenManager, Screen
URL='http://192.168.0.195:43157/'
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
        return root

    def guardar_usuario(self, instance):
        if self.id_usuario.text:
            store.put('datos_usuario', id_usuario=self.id_usuario.text)
            self.sm.current = 'inicio'
        elif self.id_usuario.text == '':
            self.dialogo.text ='Por favor introduzca su ID'
            self.dialogo.open()


    def cerrar_error(self, obj):
        self.dialogo.dismiss()

    def introducir_datos(self, obj):
        if self.sm.current == 'inicio':
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
        usuario_id=''
        try:
            usuario_id = store.get('datos_usuario')['id_usuario']
        except:
            self.dialogo.text='Primero ingrese un ID valido'
            self.dialogo.open()
        finally:
            if usuario_id:
                try:
                    requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                    requests.post(url=f"{URL}{usuario_id}/1/seguricel_wifi_activo", timeout=3)
                except:
                    self.dialogo.text='No fue posible conectar con el servidor'
                    self.dialogo.open()
                finally:
                    pass
    
    def enviar_peticion_acceso2(self, obj):
        usuario_id=''
        try:
            usuario_id = store.get('datos_usuario')['id_usuario']
        except:
            self.dialogo.text='Primero ingrese un ID valido'
            self.dialogo.open()
        finally:
            if usuario_id:
                try:
                    requests.get(url=f"{URL}seguricel_wifi_activo", timeout=3)
                    requests.post(url=f"{URL}{usuario_id}/2/seguricel_wifi_activo", timeout=3)
                except:
                    self.dialogo.text ='No fue posible conectar con el servidor'
                    self.dialogo.open()
                finally:
                    pass

if __name__ == "__main__":
    app = seguricel_prototipo()
    app.run()
