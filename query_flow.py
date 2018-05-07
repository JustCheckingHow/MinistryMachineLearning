from abstract_interface import DataSource, FilterContainer
from AllegroQuery import AllegroQuery
from filters.margin import MarginFilter
from filters.price import PriceFilter
from filters.sell_rate import SellRateFilter
import csv
import time
import numpy as np
from record import Record
from suspect import Suspect

class QueryFlow:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.construct_ds()
        self.treshold = 20

        self.filterContainer = FilterContainer()
        filters = [PriceFilter(40), MarginFilter(80), SellRateFilter(0)]
        for filter_specified in filters:
            self.filterContainer.addFilter(filter_specified)

    def construct_ds(self):
        self.ds = self.DataSourceConstructor(self.filterContainer, self.threshold)

    def run_worker(self, query):
        return self.ds.analyze(query)

    def save_worker(self, query, worker_id=0):
        return self.ds.dump_records(query, worker_id)

    def split_worker_jobs2(self, total_queries, query_params):
        with open('pickle_data.txt', 'w') as f:
            f.write(str((len(total_queries))))
        f = open('final_results' + str(time.time()) + '.csv', 'w')
        writer = csv.writer(f, delimiter=";", quotechar=' ')
        writer.writerow( ('nick', 'nip', 'email', 'phone') )

        nip_list = []
        for record in Record.read_pickle_folder("pickle_dumps"):
            weighted_average = np.zeros(record.length) #provide length filed
            df = record.parseDataFrame()
            for filter_specified in self.filterContainer.filter_array:
                current_filter_average_vector = filter_specified.filter(df)
                weighted_average = filter_specified.filter_weight*np.array(current_filter_average_vector)

            weighted_average[weighted_average > self.threshold] = 1
            weighted_average[weighted_average < self.threshold] = 0

            i = 0
            for w in weighted_average:
                if w == 1:
                    if (record.companyNip[i] != None):
                        nip = record.companyNip[i]
                        nip = nip.replace('-', '')
                        if nip in nip_list:
                            continue
                        else:
                            nip_list.append(nip)

                        s = Suspect(nip)
                        try:
                            writer.writerow( (record.userLogin[i], nip, s.getUserEmail(), s.getUserNumber()) )
                            f.flush()
                        except:
                            pass
                i += 1
        f.close()

    def split_worker_jobs(self, total_queries, query_params):
        with open('pickle_data.txt', 'w') as f:
            f.write(str(len(total_queries)))
        f = open('final_results' + str(time.time()) + '.csv', 'w')
        writer = csv.writer(f, delimiter=";", quotechar=' ')
        writer.writerow( ('nick', 'nip', 'email', 'phone') )

        nip_list = []
        for query in total_queries: #only query tab is variable

            try:
                built_query = self.DataSourceConstructor.Query(query, **query_params)
                record = self.save_worker(built_query)
            except:
                continue

            weighted_average = np.zeros(record.length) #provide length filed
            df = record.parseDataFrame()
            for filter_specified in self.filterContainer.filter_array:
                current_filter_average_vector = filter_specified.filter(df)
                weighted_average = filter_specified.filter_weight*np.array(current_filter_average_vector)
            weighted_average[weighted_average > self.threshold] = 1
            weighted_average[weighted_average < self.threshold] = 0

            i = 0
            for w in weighted_average:
                if w == 1:
                    if (record.companyNip[i] != None):
                        nip = record.companyNip[i]
                        nip = nip.replace('-', '')
                        if nip in nip_list:
                            continue
                        else:
                            nip_list.append(nip)

                        s = Suspect(nip)
                        try:
                            writer.writerow( (record.userLogin[i], nip, s.getUserEmail(), s.getUserNumber()) )
                            f.flush()
                        except:
                            pass
                i += 1
        f.close()

    def parse_categories(self, cat_file):
        categories_list = []
        with open(cat_file, "r") as f:
            line = f.readline()
            while line:
                if "catId" in line:
                    line = line.replace("catId = ", "").strip()
                    categories_list.append(int(line))
                line = f.readline()
        return categories_list

if __name__ == "__main__":
    sort = {'price' : "desc"}
    query_tab = {
                   'search': 'faktura vat marża',
                   'category': 0,
                   'offerType': 'buyNow',
                   'offerOptions': 'vatInvoice',
                   'description': 'true',
                   'condition': 'used'
                   }
    query_params = {
                   'maxPrice': 100000,
                   'minPrice': 1000,
                   'numberOfItems': 100,
                   'sortOptions': sort
                  }
    cat_file = "data_source/test.txt"

    test_filterContainer = FilterContainer()
    filters = [PriceFilter(0.6), PriceFilter(0.6), MarginFilter(0.8),
                SellRateFilter(0.3)]
    for filter_specified in filters:
        test_filterContainer.addFilter(filter_specified)

    param_dict = {
                    'workers' : 3,
                    'threshold': 0.8,
                    'DataSourceConstructor': AllegroQuery,
                    'filterContainer': test_filterContainer,
    }
    qf = QueryFlow(**param_dict)
    conditions = ['new', 'used']
    categories_list = qf.parse_categories(cat_file)
    print(categories_list)
    total_queries = []
    for condition in conditions:
        query_tab['condition'] = condition
        for cat in categories_list:
            query_tab['category'] = cat
            total_queries.append(dict(query_tab))

    print("TOTAL QUERIES {}".format(len(total_queries)))
    qf.split_worker_jobs(total_queries, query_params)
