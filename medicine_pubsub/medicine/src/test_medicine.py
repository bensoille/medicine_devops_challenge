import unittest
import pytest
from mock import patch
from medicine import Medicine

class TestMedicine(unittest.TestCase):
  # _________________________________________________
  # Class should instantiate correctly when all is ok
  def test_instanciate_ok(self):
    classinst = Medicine()
    self.assertIsInstance(classinst, Medicine, "result is not an instance of Medicine class")

  # __________________________________________________________
  # Instanciation should return None if KafkaConsumer is error
  @patch('kafka.KafkaConsumer.__init__', side_effect=Exception("Test error injection"))
  def test_setup_consumer_ko(self, mock_kafka_consumer):

    classinst = Medicine()
    prodRes = classinst.setup_consumer('kafkaservers')

    self.assertIsNone(
      prodRes,
      'Should return None if consumer is ko'
    )

  # __________________________________________________________
  # Instanciation should return None if KafkaProducer is error
  @patch('kafka.KafkaProducer.__init__', side_effect=Exception("Test error injection"))
  def test_setup_producer_ko(self, mock_kafka_consumer):

    classinst = Medicine()
    prodRes = classinst.setup_producer('kafkaservers')

    self.assertIsNone(
      prodRes,
      'Should return None if producer is ko'
    )    

  # ___________________________________________________
  # received tab_order should pass if format is correct
  def test_check_tabs_order_ok(self):
    classinst = Medicine()

    # Order is missing elements
    correct_order = {'patient_id': 'fakeid', 'tabs_count':3, 'order_timestamp_ns':3, }
    self.assertTrue(
      classinst.check_tabs_order(correct_order), 
      "Check of correct order structure should succeed"
      )

  # _________________________________________________________
  # received tab_order should not pass if format is incorrect
  def test_check_tabs_order_ko(self):
    classinst = Medicine()

    # Order is missing elements
    fake_order = {'order_timestamp_ns':3}
    self.assertFalse(
      classinst.check_tabs_order(fake_order), 
      "Check of wrong order structure should fail"
      )  

  # ______________________________________________
  # Tabs order should be built with correct values
  def test_tabs_item_build_no_args(self):
    classinst = Medicine()
    # Quickly test instance again, as we are here
    self.assertIsInstance(classinst, Medicine, "result is not an instance of Medicine class")

    test_tab_order = {
      'patient_id': 'test_id',
      'tabs_count': 3,
      'seq_number': 3,
      'order_timestamp_ns': 2
    }  

    expected_tab_item = {
      'patient_id': 'test_id',
      'order_timestamp_ns': 2,
      'order_tabs_count': 3,
      'seq_in_order': 3,
      'tab_pow': 'df56gd63',
      'delivery_timestamp_ns': 3      
    }    
    got_tab_item = classinst.make_and_publish_tab(test_tab_order)

    # Test patient_id
    self.assertIn(
      'patient_id', 
      got_tab_item, 
      "Tab item is missing patient_id"
      )
    self.assertIsInstance(
      got_tab_item['patient_id'], 
      str, 
      "patient_id is not a string"
      )

    # Test tabs_count
    self.assertIn(
      'order_tabs_count', 
      got_tab_item, 
      "Tab item is missing order_tabs_count"
      )
    self.assertIsInstance(
      got_tab_item['order_tabs_count'], 
      int, 
      "order_tabs_count is not a integer"
      )

    # Test order_timestamp_ns
    self.assertIn(
      'order_timestamp_ns', 
      got_tab_item, 
      "Tab item is missing order_timestamp_ns"
      )
    self.assertIsInstance(
      got_tab_item['order_timestamp_ns'], 
      int, 
      "Tab order order_timestamp_ns is not a integer"
      )

    # Test delivery_timestamp_ns
    self.assertIn(
      'delivery_timestamp_ns', 
      got_tab_item, 
      "Tab item is missing delivery_timestamp_ns"
      )
    self.assertIsInstance(
      got_tab_item['delivery_timestamp_ns'], 
      int, 
      "Tab order delivery_timestamp_ns is not a integer"
      )
    # Force to known value for last check
    got_tab_item['delivery_timestamp_ns'] = expected_tab_item['delivery_timestamp_ns']

    # Test seq_in_order
    self.assertIn(
      'seq_in_order', 
      got_tab_item, 
      "Tab item is missing seq_in_order"
      )
    self.assertIsInstance(
      got_tab_item['seq_in_order'], 
      int, 
      "seq_in_order is not a integer"
      )          

    # Test tab_pow
    self.assertIn(
      'tab_pow', 
      got_tab_item, 
      "Tab item is missing tab_pow"
      )
    self.assertIsInstance(
      got_tab_item['tab_pow'], 
      str, 
      "tab_pow is not a integer"
      )          
    # Force to known value for last check
    got_tab_item['tab_pow'] = expected_tab_item['tab_pow']

    # Test order object, finally
    self.assertEqual(
      got_tab_item, 
      expected_tab_item, 
      "Tab order has not patient_id correcty set up"
      )   


if __name__ == '__main__':
    unittest.main()