
id_usuario_input = """
MDTextField:
    hint_text: "Introducir ID"
    pos_hint:{'center_x': 0.5, 'center_y': 0.57}
    size_hint:(0.5, 0.11)
    width:"20sp"
"""

guardar_button = """
MDFillRoundFlatButton:
    text:"Guardar datos"
    pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    size_hint:(0.5,0.01)
    width:"100sp"
"""

lista_contratos = """

MDDropDownItem:
    id: drop_item
    text: 'seleccione contrato'
    pos_hint: {'center_x': 0.5, 'center_y': 0.8}
"""
    
boton_cerrar_dialogo = """
MDFlatButton
    text: 'Cerrar' 
"""

boton_screen_datos = """
MDIconButton:
    icon: "logo_seguricel.png"
    pos_hint: {'center_x': 0.87, 'center_y': 0.08}
    icon_size: "50sp"
    size_hint:(0.20,0.1)
"""

boton_screen_inicio = """
MDIconButton:
    icon: "atras.png"
    pos_hint: {'center_x': 0.13, 'center_y': 0.08}
    icon_size: "50sp"
    size_hint:(0.20,0.1)
"""