import os, json, hashlib
import time, signal
import concurrent.futures

from kafka import KafkaProducer, KafkaConsumer

#  __  __          _ _      _            
# |  \/  | ___  __| (_) ___(_)_ __   ___ 
# | |\/| |/ _ \/ _` | |/ __| | '_ \ / _ \
# | |  | |  __/ (_| | | (__| | | | |  __/
# |_|  |_|\___|\__,_|_|\___|_|_| |_|\___|     
#  _        _                    _            
# | |_  ___| |_ __  ___ _ _   __| |__ _ ______
# | ' \/ -_) | '_ \/ -_) '_| / _| / _` (_-<_-<
# |_||_\___|_| .__/\___|_|   \__|_\__,_/__/__/
#            |_|                              
class Medicine:
  """
  Handles tools for tabs production and forwarding to Kafka deliveries topic
  """

  def __init__(self):
    """
    Quite empty constructor
    """
    pass


  def setup_consumer(self, kafka_servers_string):
    """
    Sets up Kafka consumer, and keeps its reference in self property
    kafka_servers_string: str
      The kafka servers string, to connect to

    Returns a ref to consumer, or None on error
    """
    try:
      # Special case for external Kafka service use :
      # If container has been built with Kafka cert 
      # files and use external Kafka service with custom servers string provided
      if os.path.isfile('medicine_pubsub/certs/service.cert'):
        self.consumer = KafkaConsumer(
          'tabs.orders',
          auto_offset_reset='earliest',
          group_id='tabs_makers',
          max_poll_records=1,
          enable_auto_commit=False,
          bootstrap_servers=kafka_servers_string,
          value_deserializer=lambda v: json.loads(v.decode('utf-8')),
          security_protocol='SSL',
          ssl_check_hostname=True,
          ssl_cafile='medicine_pubsub/certs/ca.pem',
          ssl_certfile='medicine_pubsub/certs/service.cert',
          ssl_keyfile='medicine_pubsub/certs/service.key'
        ) 
      else:
        self.consumer = KafkaConsumer(
          'tabs.orders',
          auto_offset_reset='earliest',
          group_id='tabs_makers',
          enable_auto_commit=False,
          bootstrap_servers=kafka_servers_string,
          value_deserializer=lambda v: json.loads(v.decode('utf-8')),
          max_poll_records=1
        )
    except Exception as e:
      print(e.__str__())
      self.send_error_to_DLQ({'step':'storage.setup_consumer', 'error':'Could not instanciate Medicine helper kafka consumer'})
      return None

    return self.consumer


  def setup_producer(self, kafka_servers_string):
    """
    Sets up Kafka producer, and keeps its reference in self property
    kafka_servers_string: str
      The kafka servers string, to connect to

    Returns a ref to producer, or None on error
    """
    try:
      # Special case for external Kafka service use :
      # If container has been built with Kafka cert 
      # files and use external Kafka service with custom servers string provided      
      if os.path.isfile('medicine_pubsub/certs/service.cert'):
        self.producer = KafkaProducer(
          bootstrap_servers=kafka_servers_string,
          value_serializer=lambda v: json.dumps(v).encode('utf-8'),
          security_protocol='SSL',
          ssl_check_hostname=True,
          ssl_cafile='medicine_pubsub/certs/ca.pem',
          ssl_certfile='medicine_pubsub/certs/service.cert',
          ssl_keyfile='medicine_pubsub/certs/service.key'
        ) 
      else:
        self.producer = KafkaProducer(
          bootstrap_servers=kafka_servers_string,
          value_serializer=lambda v: json.dumps(v).encode('utf-8')
        ) 

    except Exception as e:
      print(e.__str__())
      self.send_error_to_DLQ({'step':'storage.setup_producer', 'error':'Could not instanciate Medicine helper kafka producer'})
      return None

    return self.producer


  def make_and_publish_tab(self, messagein, medicineProducer=None):
    """
    Publishes unique tab_item to Kafka deliveries topic
      messagein: object
        the tabs_order json object
      medicineProducer: KafkaProducer
        the prepared Kafka publisher to deliveries topic
    """

    # Prepare tab_item object to be returned
    tab_item = {
      "patient_id":             messagein['patient_id'],
      "order_timestamp_ns":     messagein['order_timestamp_ns'],
      "order_tabs_count":       messagein['tabs_count'],
      "seq_in_order":           messagein['seq_number']
    }

    # Compute some kind of dummy proof of work
    will_be_hashed_for_pow = messagein['patient_id'] + str(messagein['order_timestamp_ns']) + str(messagein['seq_number'])
    m = hashlib.sha256()
    m.update(will_be_hashed_for_pow.encode())
    tab_item["tab_pow"] = m.hexdigest()

    # Simulate some 2s processing
    time.sleep(2)

    # Add delivery nanotime to tab_item object
    tab_item["delivery_timestamp_ns"] = time.time_ns()

    # Finally send produced tab_item to deliveries topic
    if(medicineProducer is not None):
      medicineProducer.send('tabs.deliveries', tab_item)
      
    return(tab_item)


  def check_tabs_order(self, tabs_order):
    """
    Checks received tabs_order structure
      tabs_order: dict
        the order issued by patient, received via Kafka
      
    RETURNS true if order is correct, false otherwise
    """
    if('patient_id' not in tabs_order):
      return False
    if('tabs_count' not in tabs_order):
      return False
    if('order_timestamp_ns' not in tabs_order):
      return False
                 
    return True

  def send_error_to_DLQ(self, error_jsonizable_object):
    """
    Sends a message to DLQ topic
      error_jsonizable_object : any json serializable object

    Returns a reference to send result, None otherwise
    """
    try:
      sendRes = self.producer.send('tabs.dlq', error_jsonizable_object)
      print('Sent message to DLQ : ' + error_jsonizable_object['error'])
      return sendRes
    except:
      return None


#     _      _                 
#  __(_)__ _| |_ ___ _ _ _ __  
# (_-< / _` |  _/ -_) '_| '  \ 
# /__/_\__, |\__\___|_| |_|_|_|
#      |___/                   
# Custom system signal handling for sys kill interrutions
class ProgramKilled(Exception):
    pass

def signal_handler(signum, frame):
    raise ProgramKilled

#                  _       
#  _ __ ___   __ _(_)_ __  
# | '_ ` _ \ / _` | | '_ \ 
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|

if(__name__) == '__main__':

  # Catch system calls and allow clean shutdown
  signal.signal(signal.SIGTERM, signal_handler)
  signal.signal(signal.SIGINT, signal_handler)

  try:

    # Use given Kafka servers, defaults to locally deployed server
    MEDECINEPUBSUB_KAFKA_SERVERS = os.environ.get('MEDECINEPUBSUB_KAFKA_SERVERS', "medicine-pubsub-kafka-bootstrap:9092")

    medicine = Medicine()

    # Fetch one unique message and disconnect from service
    medicineConsumer = medicine.setup_consumer(MEDECINEPUBSUB_KAFKA_SERVERS)
    for message in medicineConsumer:
      medicineConsumer.commit()
      tabs_order = message.value
      break
    print(tabs_order)
    medicineConsumer.close()

    # Check received payload
    if(medicine.check_tabs_order(tabs_order) is False):
      # Received payload is incorrect : just exit with non-error code
      # as we do not need to restart job
      exit(0)

    # Prepare Kafka producer for tabs delivery topic
    medicineProducer = medicine.setup_producer(MEDECINEPUBSUB_KAFKA_SERVERS)
    print("Making " + str(tabs_order['tabs_count']) + " tabs")

    # Now create as many tabs factories as needed :
    # workers count is the number of requested tabs in fetched tabs order
    with concurrent.futures.ThreadPoolExecutor(max_workers=tabs_order['tabs_count']) as executor:
      try:
        futures = []
        # Instanciate as many times as wanted workers
        for i in range(tabs_order['tabs_count']):
          # Record this tab order seq number
          tabItem_request = tabs_order.copy()
          tabItem_request["seq_number"] = i+1

          # Actually start tab factory and deliver
          # in parallel
          print('Setting up worker #',i)
          futures.append(executor.submit(medicine.make_and_publish_tab, tabItem_request, medicineProducer))

        for future in concurrent.futures.as_completed(futures):
            print(future.result())

        # Exit job properly when done
        exit(0)

      except ProgramKilled:
        # Caught system interrupt, stop loop
        print("Killing, please wait for clean shutdown")
        executor.shutdown(wait=False)

        time.sleep(1)
        exit(0)

  except Exception as error:
    print(error)
    time.sleep(2)
    # No need to wait for clean shutdown, error was internal
    exit(1)