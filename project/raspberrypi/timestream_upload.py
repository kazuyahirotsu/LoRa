import time
import boto3
from botocore.config import Config
import time
import logging
import random

# logging.basicConfig(format='%(asctime)s %(message)s',filename='solarpanel_voltage.log', encoding='utf-8', level=logging.DEBUG)

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('test.log',  encoding='utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s')) # or whatever
root_logger.addHandler(handler)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

session = boto3.Session()
write_client = session.client('timestream-write', region_name='us-west-2', config=Config(read_timeout=20, max_pool_connections = 5000, retries={'max_attempts': 10}))
DatabaseName='solarpanel_test'
TableName='solarpanel_test'
dimensions = [
        {'Name': 'Location', 'Value': 'Tokyo'},
]

def current_milli_time():
    return int(time.time() * 1000)

def read():

    dummy_value1 = 12+random.random()
    dummy_value2 = 12+random.random()
    dummy_value3 = 12+random.random()
    
    try:
        record = [{
            'Dimensions': dimensions,
            'MeasureName': 'dummy_value1',
            'MeasureValueType': 'DOUBLE',
            'MeasureValue': str(dummy_value1),
            'Time': str(current_milli_time()),
            'TimeUnit': 'MILLISECONDS'
        },
        {
            'Dimensions': dimensions,
            'MeasureName': 'dummy_value2',
            'MeasureValueType': 'DOUBLE',
            'MeasureValue': str(dummy_value2),
            'Time': str(current_milli_time()),
            'TimeUnit': 'MILLISECONDS'
        },
        {
            'Dimensions': dimensions,
            'MeasureName': 'dummy_value3',
            'MeasureValueType': 'DOUBLE',
            'MeasureValue': str(dummy_value3),
            'Time': str(current_milli_time()),
            'TimeUnit': 'MILLISECONDS'
        }]
        result = write_client.write_records(DatabaseName=DatabaseName,
                                            TableName=TableName,
                                            Records=record,
                                            CommonAttributes={})
        print(result)
        logging.info("aws success")
    except Exception as e:
        print(e)
        logging.info(e)

    try:
        logging.info("voltage = "+str(dummy_value1)+", "+str(dummy_value2)+", "+str(dummy_value3))
    except Exception as e:
        print(e)
        logging.info(e)


if __name__ == "__main__":
    while True:
        read()
        time.sleep(60)