import time
from requests import request
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def log_data(write_api, bucket, org, data):
    write_api.write(
        bucket=bucket, 
        org=org, 
        record=influxdb_client.Point("tasmota-power-meter") \
            .field("Timestamp", data["Time"]) \
            .field("Power", data["ENERGY"]["Power"]) \
            .field("Voltage", data["ENERGY"]["Voltage"]) \
            .field("Current", data["ENERGY"]["Current"]) \
            .field("Apparent Power", data["ENERGY"]["ApparentPower"]) \
            .field("Reactive Power", data["ENERGY"]["ReactivePower"]) \
            .field("Power Factor", data["ENERGY"]["Factor"]) \
            .field("Temperature", data["ESP32"]["Temperature"]) \
            .field("Temperature Unit", data["TempUnit"])
    )

def get_data():
    rsp = request(
        method='GET',
        url='http://192.168.1.45/cm?cmnd=Status%208'
    )
    return rsp.json()['StatusSNS']

def main():
    bucket = "< bucket >"
    org    = "< org >"
    token  = "< token >"
    url    = "< url >"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)

    while True:
        data = get_data()
        log_data(write_api, bucket, org, data)
        time.sleep(10)


if __name__ == '__main__':
    main()
