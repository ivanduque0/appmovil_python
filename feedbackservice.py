from os import environ
import requests
from plyer import notification
URL_APERTURAS="https://webseguricel.up.railway.app/aperturasusuarioapi/"
argument = environ.get('PYTHON_SERVICE_ARGUMENT', '')

def main():
    while True:
        print(f"ARGUMENT: {argument}")
        try:
            aperturasjson = requests.get(url=f"{URL_APERTURAS}{argument}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
            for apertura in aperturasjson:
                if apertura['abriendo'] and not apertura['feedback']:
                    requests.put(url=f"{URL_APERTURAS}{apertura['id']}/",auth=('mobile_access', 'S3gur1c3l_mobile@'), timeout=5).json()
                    notification.notify("Apertura realizada!", "Abriendo acceso")
        except Exception as e:
            print(f'{e} - fallo en feedback')

if __name__ == '__main__':
    main()