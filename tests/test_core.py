import unittest
import os
from config import Config
from src.store_transactions import TransactionRecord

test_config = Config()


class TestApp(unittest.TestCase):
    # set up some test parameters to be used
    test_store_id1 = "YR4226"
    test_product_id = 46988220
    test_unavailable_product_id = 123
    test_csv_file_path = test_config.csv_filepath
    test_output_folder = test_config.output_folder
    test_VIP_WEIGHT = test_config.VIP_WEIGHT
    
    # Create a valid object with known output for testing
    test_transaction = TransactionRecord(
        test_csv_file_path,
        test_output_folder,
        test_product_id,
        test_VIP_WEIGHT
    )
    response = test_transaction.get_product_transaction()

    # Create a non-valid object with known output for testing
    test_unavailable_transaction = TransactionRecord(
        test_csv_file_path,
        test_output_folder,
        test_unavailable_product_id,
        test_VIP_WEIGHT
    )

    def test_config(self):
        """
        This function test if config parameters parsed correctely
        """
        self.assertEqual(
            self.test_transaction.csv_filepath,
            self.test_csv_file_path
        )
        self.assertEqual(
            self.test_transaction.output_folder,
            self.test_output_folder
        )
        self.assertEqual(
            self.test_transaction.VIP_WEIGHT,
            self.test_VIP_WEIGHT
        )

    def test_read_csv(self):
        """
        This function test if data from csv file read correctely
        """
        self.assertEqual(
            self.test_transaction.df.iloc[0, :]["PRODUCT_ID"],
            12254943
        )

    def test_error_hanling_for_unavilable_id(self):
        """
        This function test error handling if request product_id does not
        exists in the data
        """
        response = self.test_unavailable_transaction.get_product_transaction()
        self.assertEqual(
            response["status"],
            "Failed"
        )

    def test_output_file_generation(self):
        """
        This function test if output file generates correctely for valid product id 
        """
           
        self.assertEqual(
            self.response["status"],
            "Success"
        )
        self.assertTrue(os.path.exists(self.test_transaction.output_filepath))

    def test_classification_value(self):
        """
        This function test if correct CLASSIFICATION value added based on MRP
        """
        transactions = self.response["content"]
        vip_transaction = transactions[transactions["MRP"] >= self.test_transaction.VIP_WEIGHT].iloc[0, :]
      
        self.assertEqual(
             vip_transaction["CLASSIFICATION"],
             "VIP"
        )

    def test_output_file_exist_functionality(self):
        """
        This function test error handling for case when product id requested 
        is already requested before and output file exists in output folder
        This functionality need to remove when working with live data
        """
        response = self.test_transaction.get_product_transaction()
        self.assertEqual(
            response["status"],
            "File exists"
        )
        self.assertEqual(
            response["content"],
            f"{self.test_transaction.output_file} file has alredy been generated"
        )

    def test_remove_output_file_generated(self):
        """
        This function remove previousely generated output files for test case,
        so that it's ready for next run
        """
        os.remove(self.test_transaction.output_filepath)
        self.assertFalse(os.path.exists(self.test_transaction.output_filepath))


if __name__ == "__main__":
    unittest.main()
