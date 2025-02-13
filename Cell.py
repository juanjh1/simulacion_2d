import enum
import random 

class Status (enum.Enum):
    LIVE = enum.auto()
    DEAD = enum.auto()


class Cell():
    
    __hp: int  = 0
    __damage: int = 0
    __hungry: int = 0
    __age: int = 0
    __status: Status 
    __hands: list  = [None, None]

    
    def __init__(self ):
        self.hp = 100
        self.damage = 10
        self.status = Status.LIVE
    @property
    def age(self):
        return self.__age
    @age.setter
    def age (self, new_age: int ):
        if new_age < 100 and new_age > 0 and (new_age + self.age ) < 100:
            self.__age = new_age
        
        if new_age < 100 or (new_age + self.age ) > 100 :
            self.__kill()
        
    @property
    def hungry (self):
        return self.__hungry
    
    @hungry.setter
    def hungry  (self, new_hungry : int ):
        if new_hungry <= 100 and (self.__hungry + new_hungry) <= 100 and new_hungry >= -100 :
            if new_hungry < 0:
                if (new_hungry + self.__hungry) < 0:
                    self.__hungry = 0
                else:
                    self.__hungry = new_hungry

            elif new_hungry > 0:
                self.__hungry = new_hungry
    
    @property
    def damage(self):
        return self.__damage
    @damage.setter
    def damage (self, new_damage : int  ):
        self.__damage = new_damage

    @property
    def status (self):
        
        return self.__status
    @status.setter
    def status (self, status: Status):
        if status in Status.__members__:
            self.__status = status
    
    @property
    def hp (self):
        return self.__hp
    
    @hp.setter
    def hp (self, hp):
        self.__hp =  hp
    
    def __kill(self):
        self.status = Status.DEAD
    
    def hands_are_free(self) -> bool:
        return self.__hands[0] == None or self.__hands[1] == None

    def take(self, element):
        
        if self.hands_are_free():

            if self.__hands[0] != None:
                self.__hands[0] = element
            else:
                self.__hands[1] = element
    def get_old(self):
        self.age = self.age + 1
        self.damage = self.damage + random.randint(1,10)

    def get_hungry(self):
        self.hungry = self.hungry - 1 
    
    def eat(self):
        eated = False
        temp_count = 0 
        if self.hands_are_free():
            while(temp_count < 2 and not eated):
                if (isinstance(self.__hands[temp_count], Eat)):
                    self.hungry = self.hungry - self.__hands[temp_count].nutrition
                    eated = True
                    
            


class Eat ():
    __nutrition: int 

    def __init__(self):
        self.nutrition = random.randint(1,100)
        pass
    @property
    def nutrition (self):
        return self.__nutrition
    @nutrition.setter
    def nutrition(self, nutrition):
        self.__nutrition = nutrition