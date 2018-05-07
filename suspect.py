from record import Record
from ParsingZumi import ZumiParser

class Suspect:
    def __init__(self, nipNumber):
        self.nip = nipNumber

    def getUserEmail(self):
        """
        is void type and sends the user id
        """

        temp = ZumiParser.getTempAddres(self.nip)
        mail = ZumiParser.getMail(temp)
        return mail

    def getUserNumber(self):
        temp = ZumiParser.getTempAddres(self.nip)
        number = ZumiParser.getNumber(temp)
        return number

    def getUserNip(self):
        pass
