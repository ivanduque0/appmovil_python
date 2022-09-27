
id_usuario_input = """
MDTextField:
    hint_text: "Introduzca su ID"
    pos_hint:{'center_x': 0.5, 'center_y': 0.57}
    size_hint_x:None
    width:200
"""

guardar_button = """
MDFillRoundFlatButton:
    text:"Guardar datos"
    pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    size_hint_x:None
    width:200
"""

lista_contratos = """

MDDropDownItem:
    id: drop_item
    text: 'seleccione contrato'
    pos_hint: {'center_x': 0.5, 'center_y': 0.8}
    dropdown_bg: [0, 1, 1, 1]  
    on_release: app.menu.open()
    
"""

#MDRectangleFlatButton MDRoundFlatButton: