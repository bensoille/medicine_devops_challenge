import unittest
import pytest
from mock import patch
from medicine import Medicine

class TestMedicine(unittest.TestCase):

  # Class should instantiate correctly when all is ok
  def test_instanciate_ok(self):
    classinst = Medicine()
    self.assertIsInstance(classinst, Medicine, "result is not an instance of Medicine class")


  # Instanciation should return None if KafkaConsumer is error
  @patch('kafka.KafkaConsumer.__init__', side_effect=Exception("Test error injection"))
  def test_setup_consumer_ko(self, mock_kafka_consumer):

    classinst = Medicine()
    prodRes = classinst.setup_consumer('kafkaservers')

    self.assertIsNone(
      prodRes,
      'Should return None if consumer is ko'
    )


  # Instanciation should return None if KafkaProducer is error
  @patch('kafka.KafkaProducer.__init__', side_effect=Exception("Test error injection"))
  def test_setup_producer_ko(self, mock_kafka_consumer):

    classinst = Medicine()
    prodRes = classinst.setup_producer('kafkaservers')

    self.assertIsNone(
      prodRes,
      'Should return None if producer is ko'
    )    

  # # Instanciation should return None if db connect is error
  # @patch('psycopg2.connect', side_effect=Exception("Test error"))
  # def test_setup_database_connection_ko(self, mock_kafka_consumer):

  #   classinst = Storage()
  #   prodRes = classinst.setup_database_connection('user', 'pass', 'host', 'port')

  #   self.assertIsNone(
  #     prodRes,
  #     'Should return None if connection to postgres db is ko'
  #   )      


if __name__ == '__main__':
    unittest.main()