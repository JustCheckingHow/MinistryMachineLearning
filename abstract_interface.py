from abc import ABC, abstractmethod
import numpy as np

class DataSource(ABC):
    def __init__(self, filterContainer, threshold):
        """
        @param filterContainer object of type FilterContainer
        @pararm threshold decides about the minimum level of fraud probability
        """
        pass

    def analyze(self, query):
        """
        analysis based on filter container
        sennds users from records to suspcectclass
        launches email sending procedure
        @returns true if detected fraud
        """

        rec = self.sendQuery(query)
        rec_length = rec.length
        rec = rec.parseDataFrame() ## LATER REMOVE LENGTH
        weighted_average = np.zeros(rec_length) #provide length filed
        for filter_specified in self.filterContainer.filter_array:
            current_filter_average_vector = filter_specified.filter(rec)
            weighted_average = filter_specified.filter_weight*np.array(current_filter_average_vector)
        weighted_average[weighted_average > self.threshold] = 1
        weighted_average[weighted_average < self.threshold] = 0
        return weighted_average

    def dump_records(self, query, worker_id=0):
        rec = self.sendQuery(query)
        rec.pickle_dump(worker_id)
        return rec

    @abstractmethod
    def sendQuery(self, query):
        """
        @param of query to be searched
        @return record type
        """
        pass

class FilterContainer:
    def __init__(self):
        self.filter_array = []


    def addFilter(self, user_filter):
        """
        @param accepts filters
        @return
        """
        self.filter_array.append(user_filter)


class SuspectFilter(ABC):
    def __init__(self, weight):
        self.filter_weight = weight
        pass

    @abstractmethod
    def filter(self, record):
        """
        specified operation on record that confirms or denies probablity
        of record containing a fraud
        @param record - result of Result.getDataFrame()
        @return bool or probablity (float <0,1>) vector for each entry
        """
        pass

    @abstractmethod
    def getFilterDescription(self):
        return ""

    "TODO: GETTER"
