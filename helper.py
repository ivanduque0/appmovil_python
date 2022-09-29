
id_usuario_input = """
MDTextField:
    hint_text: "Introducir ID"
    pos_hint:{'center_x': 0.5, 'center_y': 0.57}
    size_hint:(0.5, 0.1)
    width:200
"""

guardar_button = """
MDFillRoundFlatButton:
    text:"Guardar datos"
    pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    size_hint:(0.5,0.01)
    width:200
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
    pos_hint: {'x': 0.85, 'y': 0.05}
    icon_size: "50sp"
"""