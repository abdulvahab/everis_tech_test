import os


class Config:
    def __init__(self):
        self.csv_filepath = os.path.join(
            os.getcwd(),
            "data",
            "store_transactions.csv"
        )
        self.output_folder = os.path.join(os.getcwd(), "data", "output")
        self.VIP_WEIGHT = 100
