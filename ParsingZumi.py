import requests
from bs4 import BeautifulSoup
class ZumiParser:
    @staticmethod
    def getTempAddres(NIP):
        try:
            req = 'http://www.zumi.pl/namapie.html?query=' + NIP
            r = requests.get(req)
            data = r.text
            soup = BeautifulSoup(data)

            x = soup.find_all(id="searchList")[0]
            x = x.find_all(class_="link")[0]
            x = x['href']
        except:
            return False

        return x

    @staticmethod
    def getNumber(tempAddress):
        try:
            req = 'http://www.zumi.pl'+tempAddress
            r = requests.get(req)
            soup = BeautifulSoup(r.text)
            x = soup.find_all("span", class_="phoneFull")[0]
            x = x.find_all("a")[0]
            return x.get_text()
        except:
            return "-"


    @staticmethod
    def getMail(tempAddress):
        try:
            req = 'http://www.zumi.pl'+tempAddress
            r = requests.get(req)
            soup = BeautifulSoup(r.text)
            x = soup.find_all(id="teleDataBox")[0]
            x = x.find_all("a")[2]
            return x.get_text()
        except:
            return "-"


if __name__ == "__main__":
    x = ZumiParser.getTempAddres("9271821297")
    print(ZumiParser.getNumber(x))
    print(ZumiParser.getMail(x))
