from query_flow import QueryFlow
from abstract_interface import DataSource, FilterContainer
from AllegroQuery import AllegroQuery
from filters.margin import MarginFilter
from filters.price import PriceFilter
from filters.sell_rate import SellRateFilter
import time

if __name__ == "__main__":

    sort = {'price' : "desc"} # TODO set sorting by date
    query_tab = {
               'category': 0,
               'offerType': 'buyNow',
               'offerOptions': 'vatInvoice',
               'condition': 'used',
               'description': 'true',
               'maxPrice': 100000,
               'minPrice': 1000,
               'itemsReturn': 1000,
               'sort': sort
              }
    cat_file = "data_source/test.txt"

    test_filterContainer = FilterContainer()
    filters = [PriceFilter(0.6), PriceFilter(0.6), MarginFilter(0.8), SellRateFilter(0.3)]
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
    total_queries = []
    for condition in conditions:
        for cat in categories_list:
            query_tab['category'] = cat
            query_tab['condition'] = condition
            total_queries.append(query_tab)

    print("TOTAL QUERIES {}".format(len(total_queries)))

    while True:
        qf.split_worker_jobs(total_queries)
        time.sleep(15*60)