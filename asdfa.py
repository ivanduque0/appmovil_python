ka = {1:'uno', 2:'dos', "tr":'tres', 4:"cuatro"}

for k in ka:
    print(ka[k])


descripcion = '1111111111 22222 3333333333 4444444444444444444 4'

listaPalabras = descripcion.split(" ")
print(listaPalabras)
armarString = ""
armarStringPrueba = ''
multiplos=0
for indicePalabra in range(len(listaPalabras)):

    armarStringPrueba = armarString + listaPalabras[indicePalabra]
    print(indicePalabra)
    print(len(armarStringPrueba) / 20)

    if len(armarStringPrueba) / 20 < 1 and indicePalabra == 0:
        armarString = listaPalabras[indicePalabra]

    if len(armarStringPrueba) / 20 < 1 and indicePalabra != 0:
        armarString = armarString + " " + listaPalabras[indicePalabra]

    if len(armarStringPrueba) / 20 >= 1 and len(armarStringPrueba) / 20 < 2:
        armarString = armarString + "\n" + listaPalabras[indicePalabra]
    
    if len(armarStringPrueba) / 20 >= 2 and len(armarStringPrueba) / 20 < 3:
        armarString = armarString + "\n" + listaPalabras[indicePalabra]

print(armarString)
print()
# for ka in range(3):
#     print(ka)
