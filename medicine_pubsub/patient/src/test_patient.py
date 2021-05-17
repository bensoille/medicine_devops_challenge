import unittest
import pytest
from mock import patch
from patient import Patient

class TestPatient(unittest.TestCase):
  # ___________________________________________________
  # Class should instantiate correctly with no argument
  def test_instanciate_no_args_ok(self):
    classinst = Patient()

    self.assertIsInstance(
      classinst, 
      Patient, 
      "result is not an instance of Patient class"
      )

  # ___________________________________________________________
  # Class should instantiate correctly with patient_id argument
  def test_instanciate_patient_id_arg_ok(self):
    classinst = Patient(patient_id='test_id')

    self.assertIsInstance(
      classinst, 
      Patient, 
      "result is not an instance of Patient class"
      )    
    self.assertEqual(
      classinst.patient_id, 
      'test_id', 
      "Patient has not patient_id correcty set up"
      )    

  # ______________________________________________
  # Tabs order should be built with correct values
  def test_tabs_order_build_no_args(self):
    classinst = Patient(patient_id='test_id')
    # Quickly test instance again, as we are here
    self.assertIsInstance(classinst, Patient, "result is not an instance of Patient class")

    expected_order = {
      'patient_id': 'test_id',
      'tabs_count': 3,
      'order_timestamp_ns': 2
    }    
    got_order = classinst.build_tabs_order()

    # Test tabs_count
    self.assertIn(
      'tabs_count', 
      got_order, 
      "Tab order is missing tabs_count"
      )
    self.assertIsInstance(
      got_order['tabs_count'], 
      int, 
      "Tab order tabs_count is not a integer"
      )
    self.assertLessEqual(
      got_order['tabs_count'], 
      classinst.max_tabs_count, 
      "Tabs order tabs_count is out of scope"
      )
    # Force to known value for last check
    got_order['tabs_count'] = expected_order['tabs_count']

    # Test order_timestamp_ns
    self.assertIn(
      'order_timestamp_ns', 
      got_order, 
      "Tab order is missing order_timestamp_ns"
      )
    self.assertIsInstance(
      got_order['order_timestamp_ns'], 
      int, 
      "Tab order order_timestamp_ns is not a integer"
      )
    # Force to known value for last check
    got_order['order_timestamp_ns'] = expected_order['order_timestamp_ns']

    # Test order object, finally
    self.assertEqual(
      got_order, 
      expected_order, 
      "Tab order has not patient_id correcty set up"
      )    


if __name__ == '__main__':
    unittest.main()