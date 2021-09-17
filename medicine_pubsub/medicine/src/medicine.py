import os, json, hashlib
import time, signal
import concurrent.futures

from walrus import Database  # A subclass of the redis-py Redis client.
db = Database(host='redis-cluster-medicine')

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
      self.producer.xadd('tabsorders', {'step': 'connecting_consumer'})
      cg = db.consumer_group('cgtabsmaker', ['tabsorders'])
      cg_created = cg.create()
      print(cg_created)
      if('tabsorders' in cg_created.keys() and cg_created['tabsorders'] == True):
        print('Creating consumer group in redis')
        cg.set_id('$')
      else:
        print('No need to create consumer group in redis')


      self.consumer = cg

    except Exception as e:
      print(e.__str__())
      self.send_error_to_DLQ({'step':'storage.setup_consumer', 'error':'Could not instanciate Medicine helper redis consumer'})
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
      self.producer = db

    except Exception as e:
      print(e.__str__())
      self.send_error_to_DLQ({'step':'storage.setup_producer', 'error':'Could not instanciate Medicine helper redis producer'})
      return None

    return self.producer


  def make_and_publish_tab(self, messagein, medicineProducer=None, messageId=None):
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
      medicineProducer.xadd('tabsdeliveries', tab_item)
      if(messageId is not None) :
        self.consumer.tabsorders.ack(messageId)
      
    return(tab_item)


  def check_tabs_order(self, tabs_order):
    """
    Checks received tabs_order structure
      tabs_order: dict
        the order issued by patient, received via Kafka
      
    RETURNS true if order is correct, false otherwise
    """
    if('step' not in tabs_order):
      return False
    # Message is about a consumer connecting, ignore these
    if( tabs_order['step']== 'connecting_consumer'):
      return False

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
      sendRes = self.producer.xadd('tabsdlq', error_jsonizable_object)
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

    # Prepare Kafka producer for tabs delivery topic
    medicineProducer = medicine.setup_producer(MEDECINEPUBSUB_KAFKA_SERVERS)

    # Fetch messages
    medicineConsumer = medicine.setup_consumer(MEDECINEPUBSUB_KAFKA_SERVERS)
    countProcessed=0

    while True:
      futures = []
      messages_to_process = medicineConsumer.read(count=100)
      if(len(messages_to_process) == 0):
        print('No message to process, sleeping 2 seconds')
        time.sleep(2)
        continue 
      else:
        print('{} messages to process'.format(len(messages_to_process)))

      # print(messages_to_process)

      # Get messages list at position 1) of first stream's (0) messages
      # messages_to_process is a list of (stream key, messages) tuples, where messages is a list of (message id, data) 2-tuples.
      for streamId, messagesFromStream in messages_to_process:
        # print(streamId, messagesFromStream)
        for messageId, messageData in messagesFromStream :
          if type(messageId) is bytes :
            messageId = messageId.decode()
            tempMessData = {}
            for datakey in messageData.keys():
              tempMessData[datakey.decode()] = messageData[datakey].decode()
            messageData = tempMessData

          # print(str(messageId), str(messageData))
          countProcessed += 1

          # Check received payload
          if(medicine.check_tabs_order(messageData) is False):
            # Received payload is incorrect : just warn and continue
            print("Error when checkin tabs order, skipping (step {messageData['step']})")
            medicineConsumer.tabsorders.ack(messageId)
            continue                  

          tabs_order = messageData
          tabs_order['tabs_count'] = int(tabs_order['tabs_count']) if(type(tabs_order['tabs_count']) is not int) else tabs_order['tabs_count']

          print("Making {} tabs".format(str(tabs_order['tabs_count'])))
          countProcessed += 1
          print('Processed ' + str(countProcessed) + ' messages')
          # Now create as many tabs factories as needed :
          # workers count is the number of requested tabs in fetched tabs order
          # with concurrent.futures.ThreadPoolExecutor(max_workers=tabs_order['tabs_count']) as executor:
          executor = concurrent.futures.ThreadPoolExecutor(max_workers=tabs_order['tabs_count'])
          try:
            
            # Instanciate as many times as wanted workers
            for i in range(tabs_order['tabs_count']):
              # Record this tab order seq number
              tabItem_request = tabs_order.copy()
              tabItem_request["seq_number"] = i+1

              # Actually start tab factory and deliver
              # in parallel
              print('Setting up worker #',i)
              futures.append(executor.submit(medicine.make_and_publish_tab, tabItem_request, medicineProducer, messageId))

      
            # Exit job properly when done
            #exit(0)

          except ProgramKilled:
            # Caught system interrupt, stop loop
            print("Killing, please wait for clean shutdown")
            executor.shutdown(wait=False)

            time.sleep(2)
            #medicineConsumer.close()
            exit(0)
      results_collector = []
      for future in concurrent.futures.as_completed(futures):
        results_collector.append(future.result()['tab_pow'][-5:])

      print("et voilà : {}".format(','.join(results_collector)))

  except Exception as error:
    print(error)
    time.sleep(2)
    # No need to wait for clean shutdown, error was internal
    exit(1)