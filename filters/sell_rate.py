from abstract_interface import SuspectFilter
import numpy as np

class SellRateFilter(SuspectFilter):

    def __init__(self, weight):
        SuspectFilter.__init__(self, weight)

    def filter(self, record):
        res = np.zeros(record.shape[0])
        try:
            prices = np.array(record['price'].values)
            quantities = np.array(record['quantity'].values)

            res = prices * prices * quantities
            res = res / np.max(res)
        except:
            pass

        return res

    def getFilterDescription(self):
        return "Sprzedano dużo drogich produktów"
