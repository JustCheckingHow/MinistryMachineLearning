from abstract_interface import SuspectFilter
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Checks whether seller tries to sell new product with margin
class MarginFilter(SuspectFilter):

    def filter(self, record):
        # if item is sold on margin and is new, something is fishy
        tmp = np.zeros(record.shape[0])        
        try:
            tmp = record["itemName"].tolist()
            for i, el in enumerate(tmp):
                if "marża" in el:
                    tmp[i] = 1
                else:
                    tmp[i] = 0

            tmp2 = record["auctionDescription"].tolist()
            for i, el in enumerate(tmp):
                if "marża" in el:
                    tmp2[i] += 1
                else:
                    tmp2[i] = 0

            tmp_series = np.zeros(record.shape[0])
            tmp_series[record['vatInvoiceMargin'].values == 1] = 2
            tmp_series[record['usedOrNew'].values == "new"] = 2

            tmp = tmp + tmp2 + tmp_series

            tmp[tmp < 3] = 0
            tmp[tmp >= 3] = 1
        except:
            return tmp

        return tmp

    def getFilterDescription(self):
        return "Sprzedawany przedmiot jest nowy, ale sprzedawca oferuje fakturę na przedmioty używane"
