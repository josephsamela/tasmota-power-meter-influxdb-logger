import time
from requests import request
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

devices = [
    {
        "name": "Server Rack",
        "ip": "192.168.1.31"
    },
    {
        "name": "Furnace",
        "ip": "192.168.1.32"
    },
    {
        "name": "Dehumidifer",
        "ip": "192.168.1.33"
    },
    {
        "name": "3D Printer",
        "ip": "192.168.1.34"
    }
]

def log_data(write_api, bucket, org, data, name):
    write_api.write(
        bucket=bucket, 
        org=org, 
        record=influxdb_client.Point(name) \
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

def get_data(ip):
    rsp = request(
        method='GET',
        url=f'http://{ip}/cm?cmnd=Status%208'
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
        for device in devices:
            try:
                data = get_data(device['ip'])
                log_data(write_api, bucket, org, data, device['name'])
            except:
                print(f'ERROR: Cannot connect to device or log data. {device["name"]} ({device["ip"]})')
        time.sleep(10)


if __name__ == '__main__':
    main()
