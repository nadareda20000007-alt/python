from abc import ABC , abstractmethod
import time
class Sensor():
    def __init__(self , name , unit) :
        self.name = name 
        self.unit = unit
        self.__reading = None

    @abstractmethod
    def read(self):
        pass

    def report(self):
        self.__reading = self.read()
        print(f"{self.name}: {self.__reading}".rjust(100))


    def getReading (self):
        return self.__reading