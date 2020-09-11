#!/usr/bin/python

from src.store_transactions import TransactionRecord
from config import Config
import argparse
import json


def get_args():
    """
    This function parse commandline arguments
    """

    parser = argparse.ArgumentParser(
        prog="core.py",
        usage="python %(prog)s product_id"
        )
    parser.add_argument(
        "product_id",
        type=int,
        help="Provide product_id to get transaction record"
    )
    args = parser.parse_args()
    return args


def run(product_id):
    """
    This is a wrapper function which creates transaction record object
    and print out response based on the input
    args: product_id:int
    returns : prints response based on product id. Also Creates output 
    file for valid product id 
    """
    _config = Config()

    transaction_record = TransactionRecord(
        _config.csv_filepath,
        _config.output_folder,
        product_id,
        _config.VIP_WEIGHT
    )
    response = transaction_record.get_product_transaction()
    if response["status"] == "Success":
        # for successful response, convert dataframe into list of dictionary
        response["content"] = list(response["content"].T.to_dict().values())
    json_response = json.dumps(response, indent=4, sort_keys=True)
    print(json_response)


if __name__ == "__main__":
    product_id = get_args().product_id
    run(product_id)
