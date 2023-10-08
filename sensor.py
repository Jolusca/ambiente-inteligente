class Sensor:
        def __init__(self, on:bool, temp:float):
            self.on = on
            self.temp = temp

        def toString(self):
            return self.on + ', '+ self.temp
        
