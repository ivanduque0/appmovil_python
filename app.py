from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import requests

URL='https://tesis-reconocimiento-facial.herokuapp.com/apertura/'
CONTRATO="servidorarchpc"
ID_USUARIO="1262315361"
class seguricel_prototipo(App):
    def build(self):
        btn = Button(
                     color =(1, 0, .65, 1),
                     background_normal = 'acceso_principal.png',
                     background_down ='down.png',
                     size_hint = (.3, .3),
                     pos_hint = {"x":0.35, "y":0.3}
                   )
        btn.bind(on_press=self.abrir_acceso)
    
        return btn

    def abrir_acceso(self, instance):
        requests.post(URL, 
        json={"contrato":CONTRATO,
            "acceso":"1",
                "id_usuario":ID_USUARIO
})

     
        
        

if __name__ == "__main__":
    app = seguricel_prototipo()
    app.run()
