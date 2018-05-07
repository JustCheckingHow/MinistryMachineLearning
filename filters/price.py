from abstract_interface import SuspectFilter
import numpy as np


# Checks whether price of item is too peculiar to be true
class PriceFilter(SuspectFilter):

    def filter(self, record):
        try:
            prices = np.array(record['price'].values)
            five_per_cent_highest, highest_plus_variance = self._get_basic_thresholds(np.unique(prices))
            suspects = np.zeros((len(prices), 1))
            suspects[prices > five_per_cent_highest] = 0.5
            suspects[prices > highest_plus_variance] = 1
            return suspects.ravel()
        except:
            suspects = np.zeros((len(prices), 1))
            return suspects

    def getFilterDescription(self):
        return "Filtr wykrył podejrzaną cenę sprzedawanego produktu"

    @staticmethod
    def _get_basic_thresholds(unique_prices):
        highest_av = np.average(unique_prices)
        var = np.std(unique_prices)
        highest_plus_var = highest_av + var * highest_av * 0.02
        return np.percentile(unique_prices, 95), highest_plus_var
