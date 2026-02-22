from class1 import Engine   # Import the class from the other file

class Car:
    def __init__(self, engine):   # Accept instance from outside
        self.engine = engine
    
    def drive(self):
        return self.engine.start()


# Example: use Engine (from class1) inside Car (class2)
if __name__ == "__main__":
    engine = Engine()      # Create instance of class from class1.py
    car = Car(engine)
    print(car.drive())     # Vroom!