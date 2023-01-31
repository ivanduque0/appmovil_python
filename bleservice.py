"""Service to advertise data, while not stopped."""
import time
from os import environ

from able import BluetoothDispatcher
from able.advertising import (
    Advertiser,
    AdvertiseData,
    ServiceUUID,
    Interval,
    TXPower,
)


def main():
    uuid = environ.get(
        "PYTHON_SERVICE_ARGUMENT",
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )
    advertiser = Advertiser(
        ble=BluetoothDispatcher(),
        data=AdvertiseData(ServiceUUID(uuid)),
        interval=Interval.MIN,
        tx_power=TXPower.MAX,
    )
    advertiser.start()
    print('inicio!')
    #t1=time.perf_counter()
    while True:
        time.sleep(0xDEAD)
        # time.sleep(60)
    print('termino cuenta!')


if __name__ == "__main__":
    main()
    print('termino bluetooth!')