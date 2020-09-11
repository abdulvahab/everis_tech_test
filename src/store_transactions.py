#!/usr/bin/python

import pandas as pd
import json
import os


class TransactionRecord:
    def __init__(self, csv_filepath, output_folder, product_id, VIP_WEIGHT):
        """
        This method will create a TransactionRecord object for given 
        config parameters and product_id
        """
        self.csv_filepath = csv_filepath
        self.VIP_WEIGHT = VIP_WEIGHT
        self.product_id = product_id
        self.df = pd.read_csv(self.csv_filepath)
        self.output_folder = output_folder
        self.output_file = f"{product_id}.json"
        self.output_filepath = os.path.join(
            self.output_folder,
            self.output_file
        )

    def get_product_transaction(self):
        """
        This method will generate response for given product_id based on 
        weather that product is in dataset or not
        """ 

        # check if that product_id has already been processed
        # don't use for data updated actily(live database)
        if os.path.exists(self.output_filepath):
            self.response = {
                "status": "File exists",
                "content": f"{self.output_file} file has alredy been generated",
                "message": f"The transaction record for product_id: {self.product_id} \
                            already exist at {self.output_filepath}",
            }
            # print(json.dumps(self.response, indent=4, sort_keys=True))
            return self.response

        self.transactions = self.df[self.df["PRODUCT_ID"] == self.product_id]

        # Check for invalid product_id (product_id) not in the dataset
        if self.transactions.empty:
            self.response = {
                    "status": "Failed",
                    "message": f"There is no transaction record for productid: {self.product_id} \
                                exist.Please check product id and try again",
            }
            return self.response

        # Create classification column based on value of MRP column
        self.transactions["CLASSIFICATION"] = self.transactions.apply(
            lambda x: "VIP" if x["MRP"] >= self.VIP_WEIGHT else "NO VIP",
            axis=1
            )
        self.response = {
            "status": "Success",
            "content": self.transactions
        }

        # For succeful response write data into json file
        self.for_json = list(self.transactions.T.to_dict().values())
        with open(self.output_filepath, "w") as output_file:
            json.dump(self.for_json, output_file)
        return self.response


if __name__ == "__main__":
    print("This script is intended to import as module in another scripts")
