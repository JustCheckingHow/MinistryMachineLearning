import pandas as pd
import pickle
import datetime
import os

"""
SEE THE SPECIFICATION OF THE FIELDS IN THE WEB API DOCS
SPECIFIC FIELDS TBD
"""


class Record:
    def __init__(self, **kwargs):
        self.dict_temp = kwargs
        minimum_list = ["userId", "quantity", "companyAddress", "price",
            "categoryName", "auctionDescription", "usedOrNew", "vatInvoice",
            "vatInvoiceMargin"]
        for required_entry in minimum_list:
            if not required_entry in kwargs.keys():
                print("LACKING KEY {}".format(required_entry))
                raise TypeError

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return str(self.__dict__['dict_temp'])

    def parseDataFrame(self):
        #parses into dataframe
        new_records = pd.DataFrame()
        return new_records.from_records(self.__dict__['dict_temp'])

    @staticmethod
    def pickle_read(path):
        with open(path, 'rb') as fs:
            try:
                while True:
                    return pickle.load(fs)
            except EOFError:
                pass

    @staticmethod
    def read_pickle_folder(directory):
        obj_array = []
        for filename in os.listdir(directory):
            obj = Record.pickle_read(os.path.join(directory, filename))
            obj_array.append(obj)
        return obj_array

    def pickle_dump(self, worker_id=0):
        print("SAVING")
        now = datetime.datetime.now()
        date_str = "./pickle_dumps/pickle_" + str(now.year) + "_" + str(now.day) + \
                    "_" + str(now.hour) + "_" + str(now.minute) \
                    + "_" + str(now.second) + "_worker_id_" + str(worker_id) + ".pickle"
        with open(date_str, 'wb') as f:
            pickle.dump(self, f)

if __name__ == "__main__":
    kwargs = {"userId":[1,2,3], "quantity":[1,2,3], "companyAddress":[1,2,3], "price":[1,2,3],
        "categoryName":[1,2,3], "auctionDescription":[1,2,3], "usedOrNew":[1,2,3], "vatInvoice": [1,2,3],
        "vatInvoiceMargin": ["name", "name2", "name2"]}
    new_record = Record(**kwargs)
    new_record.pickle_dump()

    directory = "./pickle_dumps"
    print(Record.read_pickle_folder(directory)[0])
