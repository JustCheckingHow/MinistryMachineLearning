#kod do wszukiwnia itemów w Pythonie 2.7, wymaga instalacji modulu suds
from suds.client import Client
from suds.plugin import MessagePlugin
#from abstract_interface import DataSource
from record import Record

import time

_ALLEGRO_USER_NAME_ = ""
_ALLEGRO_USER_PASSWORD_ = ""

class AllegroQuery(Record):
    def __init__(self, filterContainer, threshold):
        DataSource.__init__(self, filterContainer, threshold)
        self.webAPI = ''
        self.userLogin = ''
        self.userPassword = ''
        self.countryId = 1 #POLAND
        self.createConnection()
        self.filterContainer = filterContainer
        self.threshold = threshold

    def createFilter(self, tablica, minPrice=None, maxPrice=None):
        rangeUp = len(tablica)
        filter_query = self.client.factory.create('ArrayOfFilteroptionstype')
        for i in range(0, rangeUp):
            filterr = self.client.factory.create('FilterOptionsType')
            filterr.filterId = list(tablica.keys())[i]
            #print(filtr.filterId)
            filterAOS = self.client.factory.create('ArrayOfString')
            filterAOS.item = list(tablica.values())[i]
            filterr.filterValueId = filterAOS
            filter_query.item.append(filterr)

        price_filter = self.client.factory.create('FilterOptionsType')

        if minPrice != None and maxPrice != None:
            price_filter.filterId = "price"
            price_filter.filterValueRange.rangeValueMin = minPrice
            price_filter.filterValueRange.rangeValueMax = maxPrice
        else:
            if minPrice != None:
                price_filter.filterId = "price"
                price_filter.filterValueRange.rangeValueMin = minPrice

            if maxPrice != None:
                price_filter.filterId = "price"
                price_filter.filterValueRange.rangeValueMax = maxPrice

        filter_query.item.append(price_filter)

        return filter_query
    
    def createSort(self, tablica):

        if(tablica != None):
            sort_query = self.client.factory.create('SortOptionsType')
            sort_query.sortType = list(tablica.keys())[0]
            sort_query.sortOrder = list(tablica.values())[0]

            return sort_query

    def createConnection(self):
        try:
            url = 'https://webapi.allegro.pl/service.php?wsdl'
            self.client = Client(url, location='https://webapi.allegro.pl/service.php', timeout=60000)
        except:
            print("No internet connection!")

    def sendQuery(self, query):

        try:
            filter_query = self.createFilter(query.filterOptions, query.minPrice, query.maxPrice)
            sort_query = self.createSort(query.sortOptions)
            result = self.client.service.doGetItemsList(webapiKey=self.webAPI, filterOptions=filter_query, sortOptions=sort_query,
                                    countryId=self.countryId, resultSize=query.numberOfItems)

            itemId = []
            itemName = []
            offertId = []
            userId = []
            quantity = []
            boughtItem = []
            price = []
            companyAddress = []
            categoryName = []
            usedOrNew = []
            vatInvoice = []
            vatInvoiceMargin = []
            companyNip = []
            auctionDescription = []
            userLogin = []

            resultSys = self.client.service.doQuerySysStatus(sysvar=3, countryId=self.countryId,
                        webapiKey = self.webAPI)
            verKey = resultSys.verKey
            
            resultLogin = self.client.service.doLogin(userLogin=_ALLEGRO_USER_NAME_, userPassword=_ALLEGRO_USER_PASSWORD_, countryCode=self.countryId, webapiKey=self.webAPI,
                         localVersion=verKey)
            ssessionHandle = resultLogin.sessionHandlePart

            for item in result.itemsList[0]:
                itemId.append(item.itemId)
                itemName.append(item.itemTitle)
                userId.append(item.sellerInfo.userId)
                userLogin.append(item.sellerInfo.userLogin)
                quantity.append(item.leftCount + item.bidsCount)
                boughtItem.append(item.bidsCount)
                price.append(item.priceInfo[0][0].priceValue)

                usedOrNew.append(item.conditionInfo)

                for cat in result.categoriesList.categoriesTree[0]:
                    if cat.categoryId == item.categoryId:
                        categoryName.append(cat.categoryName)
                        break
                else:
                    categoryName.append("NO CAT")

                a = self.client.factory.create('ArrayOfLong')
                a.item = [item.itemId]
                resultItem = self.client.service.doGetItemsInfo(sessionHandle=ssessionHandle,
                             getDesc = 1, getCompanyInfo = 1, itemsIdArray = a)

                itemInfo = resultItem[0][0][0]
                offertId.append(itemInfo[0].itId)
                auctionDescription.append(itemInfo[0].itDescription)
                vatInvoice.append(itemInfo[0].itVatInvoice)
                vatInvoiceMargin.append(itemInfo[0].itVatMarginInvoice)

                address = ""
                if itemInfo.itemCompanyInfo.companyFirstName != None:
                    address += itemInfo.itemCompanyInfo.companyFirstName + " "
                if itemInfo.itemCompanyInfo.companyLastName  != None:
                    address += itemInfo.itemCompanyInfo.companyLastName + " "
                if itemInfo.itemCompanyInfo.companyName != None:
                    address += itemInfo.itemCompanyInfo.companyName  + "\n"
                if itemInfo.itemCompanyInfo.companyAddress != None:
                    address += itemInfo.itemCompanyInfo.companyAddress + "\n"
                if itemInfo.itemCompanyInfo.companyPostcode  != None:
                    address += itemInfo.itemCompanyInfo.companyPostcode + " "
                if itemInfo.itemCompanyInfo.companyCity != None:
                    address += itemInfo.itemCompanyInfo.companyCity + " "
                companyAddress.append(address)

                companyNip.append(itemInfo.itemCompanyInfo.companyNip)

            kwargs = {
                "userId": userId,
                "itemName" : itemName,
                "itemId": itemId,
                "boughtItem": boughtItem,
                "quantity": quantity,
                "companyAddress": companyAddress,
                "price": price,
                "categoryName": categoryName,
                "companyAddress": companyAddress,
                "auctionDescription": auctionDescription,
                "usedOrNew": usedOrNew,
                "vatInvoice": vatInvoice,
                "vatInvoiceMargin": vatInvoiceMargin,
                "offertId": offertId,
                "companyNip": companyNip,
                "userLogin": userLogin,
                "length": len(userId)
            }
            return Record(**kwargs)

        except Exception as e:
            print(e)

            kwargs = {
                "userId": [],
                "itemName" : [],
                "itemId": [],
                "boughtItem": [],
                "quantity": [],
                "companyAddress": [],
                "price": [],
                "categoryName": [],
                "companyAddress": [],
                "auctionDescription": [],
                "usedOrNew": [],
                "vatInvoice": [],
                "vatInvoiceMargin": [],
                "offertId": [],
                "userLogin": [],
                "companyNip": [],
                "length": len(userId)
            }
            return Record(**kwargs)

    def sendItemQuery(self, query):
        try:
            filter_query = self.createFilter(query.filterOptions)
            result = self.client.service.doGetItemsInfo(webapiKey = self.webAPI, filterOptions = filter_querry,
                                        countryId = self.countryId, resultSize=query.numberOfItems)
        except Exception as e:
            print(e)

    class Query:
        def __init__(self, filterOptionsDict, **kwargs):
            self.filterOptions = filterOptionsDict
            for k, v in kwargs.items():
                setattr(self, k, v)

if __name__ == "__main__":
    filterOptions = {
               'search': 'samsung galaxy',
               'offerType': 'buyNow',
               'offerOptions': 'vatInvoice',
               'description': 'true'
              }
    sort = {'price' : "asc"}

    q = AllegroQuery.Query(filterOptions, sort, 5, 1000, 1000000)
    allQuery = AllegroQuery(None, 0.5)
    allQuery.sendQuery(q)
