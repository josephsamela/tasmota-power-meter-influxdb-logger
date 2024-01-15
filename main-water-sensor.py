import time
from requests import request
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

devices = [
    {
        "name": "Basement Leak Sensor",
        "ip": "192.168.1.16"
    }
]

def log_data(write_api, bucket, org, data, name):

    match data['currentState']:
        case 'DRY':
            m = 0
        case 'WET':
            m = 1

    write_api.write(
        bucket=bucket, 
        org=org, 
        record=influxdb_client.Point(name)
            .field('State', m)
    )

def get_data(ip):
    rsp = request(
        method='GET',
        url=f'http://{ip}/status'
    )
    return rsp.json()

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
            except Exception as e:
                print(f'ERROR: Cannot connect to device or log data. {device["name"]} ({device["ip"]}) {e}')
        time.sleep(10)

if __name__ == '__main__':
    main()
