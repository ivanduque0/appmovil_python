from kivy.storage.dictstore import DictStore
from kivy.storage.jsonstore import JsonStore
import requests
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton, MDRectangleFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
import id_user_style
from kivy.lang import Builder
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
URL='https://tesis-reconocimiento-facial.herokuapp.com/apertura/'
CONTRATO="servidorarchpc"
ID_USUARIO="1262315361"
URL_CONTRATOS="https://tesis-reconocimiento-facial.herokuapp.com/agregarcontratosapi/"
#store = DictStore('datos_usuario')
store = JsonStore('datos_usuario.json')
# store.put('datos_usuario', contrato=CONTRATO, id_usuario=ID_USUARIO)


class seguricel_prototipo(MDApp):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.screen = Screen()
    #     lista = Builder.load_string(id_user_style.lista_contratos)
    #     self.screen.add_widget(lista)
    #     # lista = Builder.load_string(id_user_style.lista_contratos)
    #     # self.screen.add_widget(lista)
    #     boton_guardar = Builder.load_string(id_user_style.guardar_button)
    #     self.screen.add_widget(boton_guardar)
    #     id_usuario = Builder.load_string(id_user_style.id_usuario_input)
    #     self.screen.add_widget(id_usuario)
    #     menu_items = [
    #         {
    #             "text": f"Item {i}",
    #             "viewclass": "OneLineListItem",
    #             "on_release": lambda x=f"Item {i}": self.menu_callback(x),
    #         } for i in range(5)
    #     ]
    #     self.menu = MDDropdownMenu(
    #         caller=self.screen,
    #         items=menu_items,
    #         width_mult=4,
    #     )
    def build(self):
        # label = MDLabel(text="Hello world", halign="center", theme_text_color="Error",
        #                 font_style="Subtitle2")

        # label = MDLabel(text="Hello world", halign="center",theme_text_color="Custom",
        #                 text_color=(0,0,1,1))
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.theme_style = "Dark"
        self.contrato_seleccionado = ''
        self.cerrar_dialogo = MDFlatButton(text='cerrar',
                                          on_release=self.cerrar_error)
        self.dialogo = MDDialog(title='Error',
                     size_hint=(0.7,0.3),
                     buttons=[self.cerrar_dialogo])
        screen = Screen()
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
            width_mult=4,
        )

        self.lista = Builder.load_string(id_user_style.lista_contratos)
        self.lista.bind(on_release=self.lista_contratos)
        screen.add_widget(self.lista)
        boton_guardar = Builder.load_string(id_user_style.guardar_button)
        boton_guardar.bind(on_press=self.guardar_usuario)
        screen.add_widget(boton_guardar)
        self.id_usuario = Builder.load_string(id_user_style.id_usuario_input)
        screen.add_widget(self.id_usuario)
        
        return screen

    def menu_callback(self, text_item):
        self.contrato_seleccionado = text_item
        self.lista.set_item(text_item)
        self.menu.dismiss()

    def guardar_usuario(self, instance):
        if self.contrato_seleccionado and self.id_usuario.text:
            store.put('datos_usuario', contrato=self.contrato_seleccionado, id_usuario=self.id_usuario.text)
            print(self.id_usuario.text)
            print(self.contrato_seleccionado)
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

    # def abrir_acceso(self, instance):
    #     requests.post(URL, 
    #     json={"contrato":CONTRATO,
    #         "acceso":"1",
    #             "id_usuario":ID_USUARIO})
    #     print('accion')

        

if __name__ == "__main__":
    app = seguricel_prototipo()
    app.run()
