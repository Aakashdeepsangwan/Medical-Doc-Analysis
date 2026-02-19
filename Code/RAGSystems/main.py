class Dog:
    def __init__(self, name, breed):
        self.name = name      # Instance variable
        self.breed = breed    # Instance variable
    
    def bark(self):
        return f"{self.name} says woof!"
    
    def describe(self):
        return f"{self.name} is a {self.breed}"


    def owner_name(self) :
        return "Akash"

    def dog_and_owner(self) :
        return f"{self.name} dog's owner is {self.owner_name()}"


# Creating instances - __init__ runs each time
my_dog = Dog("Toofan", "Border Collie")
other_dog = Dog("Max", "German Shepherd")

print(my_dog.dog_and_owner())

