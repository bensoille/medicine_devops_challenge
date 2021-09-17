import os, json, uuid
import time, threading, signal
from random import randint

from walrus import Database  # A subclass of the redis-py Redis client.
db = Database(host='redis-cluster-medicine')

#  ____       _   _            _   
# |  _ \ __ _| |_(_) ___ _ __ | |_ 
# | |_) / _` | __| |/ _ \ '_ \| __|
# |  __/ (_| | |_| |  __/ | | | |_ 
# |_|   \__,_|\__|_|\___|_| |_|\__|
#  _        _                    _            
# | |_  ___| |_ __  ___ _ _   __| |__ _ ______
# | ' \/ -_) | '_ \/ -_) '_| / _| / _` (_-<_-<
# |_||_\___|_| .__/\___|_|   \__|_\__,_/__/__/
#            |_|                              
class Patient:
  """
  Handles tools for tabs order crafting and forwarding to Kafka topic
  """

  def __init__(self, patient_id=None, max_tabs_count=None, period=None):
    """
    Constructor sets up properties from needed arguments :
    patient_id: str
      The patient name to write in order payload
      Defaults to computed uuid
    max_tabs_count: int
      The maximum number of tabs to order at once
      Defaults to 30 tabs
    period: int
      The time between 2 orders, in seconds
      Defaults to 1 second
    """
    if not patient_id:
      patient_id = uuid.uuid4().__str__()
    if max_tabs_count is None:
      max_tabs_count=30
    if period is None:
      period=1

    self.period         = period
    self.patient_id     = patient_id
    self.max_tabs_count = max_tabs_count

    self.ticker = threading.Event()


  def setup_producer(self, kafka_servers_string):
    """
    Sets up Kafka producer, and keeps its reference in self property
    kafka_servers_string: str
      The kafka servers string, to connect to

    Returns a ref to producer, or None on error
    """
    try:
      self.producer = db
    except Exception as e:
      print(e.__str__())
      self.send_error_to_DLQ({'step':'medicine.setup_producer', 'error':'Could not instanciate Medicine helper redis producer'})
      return None

    return self.producer


  def build_tabs_order(self):
    """
    Computes tabs order to be published

    RETURNS order as dict():
    patient_id: str the patient name
    tabs_count: int random between 1 and configured max_tabs_count
    order_timestamp_ns: int the timestamp of original order in nanoseconds
    """
    rand_number = randint(1, self.max_tabs_count)
    now_ts_ns = time.time_ns()

    built_order = {
      'step'      : 'creating_tab',
      'patient_id': self.patient_id,
      'tabs_count': rand_number,
      'order_timestamp_ns': now_ts_ns
    }

    return built_order


  def start_periodic_requests(self):
    """
    Starts periodic requests loop, using config values from env variables.
    See method stop_periodic_requests for loop stop

    Returns None on error, is blocking otherwise
    """
    while not self.ticker.wait(self.period):
      #-----------------------------------------
      order = instance.build_tabs_order()
      #-----------------------------------------

      if(order is None):
        self.send_error_to_DLQ({'step':'patient.start_periodic_requests', 'error':'Could not build order'})
        # TODO should quit or not ?? Not specified
        return self.stop_periodic_requests()
        
      try:
        # Actually send out our tabs order to orders topic
        xaddreturn = self.producer.xadd('tabsorders', order)
        
        print(order['patient_id'] + ' / '  + str(order['order_timestamp_ns']) + ' : Sent order to Redis stream (' + str(order['tabs_count']) + ' tabs) - ' + str(xaddreturn))
      except Exception as e:
        self.send_error_to_DLQ({'step':'patient.start_periodic_requests', 'error':'Could not push order to Redis stream', 'order':order})
        return self.stop_periodic_requests()


  def stop_periodic_requests(self):
    """
    Stops periodic requests loop, previously started with start_periodic_requests

    Returns None
    """    
    self.ticker.clear()
    return None
    

  def send_error_to_DLQ(self, error_jsonizable_object):
    """
    Sends a message to DLQ topic
      error_jsonizable_object : any json serializable object

    Returns a reference to send result, None otherwise
    """
    try:
      sendRes = self.producer.xadd('tabsdlq', error_jsonizable_object)
      print('Sent message to DLQ : ' + error_jsonizable_object['error'])
      return sendRes
    except:
      return self.stop_periodic_requests()


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
    # Check that we got our env vars set
    ORBITAL_PATIENT_ID            = os.environ.get("ORBITAL_PATIENT_ID")
    ORBITAL_MAX_TABS_COUNT        = os.environ.get("ORBITAL_MAX_TABS_COUNT")
    ORBITAL_ORDER_PERIOD_SECONDS  = os.environ.get("ORBITAL_ORDER_PERIOD_SECONDS")
    MEDECINEPUBSUB_KAFKA_SERVERS  = os.environ.get('MEDECINEPUBSUB_KAFKA_SERVERS', "medicine-pubsub-kafka-bootstrap:9092")

    # And then instantiate with provided values
    # (defaults are applied if not provided)
    instance = Patient(ORBITAL_PATIENT_ID, ORBITAL_MAX_TABS_COUNT, ORBITAL_ORDER_PERIOD_SECONDS)

    if(instance is None):
      raise RuntimeError("Could not instanciate Medicine tool")

    # Prepare producer to Kafka
    print("setup producer")
    producer = instance.setup_producer(MEDECINEPUBSUB_KAFKA_SERVERS)
    if(producer is None):
      raise RuntimeError("Could not instanciate Medicine tool's kafka producer")

    # Actually start ininite loop
    instance.start_periodic_requests()

  except ProgramKilled :
    # Caught system interrupt, stop loop
    print("Killing, please wait for clean shutdown")
    instance.stop_periodic_requests()
    # Wait a couple of seconds and exit with success return code
    time.sleep(instance.period)
    exit(0)

  except Exception as e:
    # No need to wait for clean shutdown, error was internal
    # Pod would be restarted, let's issue some error return code
    exit(1)
