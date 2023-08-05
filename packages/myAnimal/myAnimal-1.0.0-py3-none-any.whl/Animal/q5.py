from abc import ABC, abstractmethod
from random import choice

class Animal(ABC):
    def __init__(self, name, age, color, isWild, energy=0):
        self.name = name
        self.age = age
        self.color = color
        self.isWild = isWild
        self.energy = energy


    @abstractmethod
    def move(self,mile):
        pass
       


    @abstractmethod
    def eat(self, calory):
        pass      


  

class Lion(Animal):
    def __init__(self, name, age, color, isWild, energy=0):
        super.__init__(name, age, color, isWild, energy=0)

    def move(self,mile):
        if self.energy > mile:
            self.energy += mile

        else:
            print("doesnt enough energy please eat sth...") 


    def eat(self, calory):
        self.energy += calory  

    def __add__(father, mother):
        wildList = [True, False]
        isWild = choice(wildList)

        return Lion(father.name, 0, mother.color, isWild) 


              
        
    



