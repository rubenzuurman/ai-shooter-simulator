import math
import random as rnd

class Player:
    
    PLAYER_ID = 0
    
    def __init__(self):
        self.id = Player.PLAYER_ID
        Player.PLAYER_ID += 1
        
        self.position = [0, 0] # x, y
        self.rotation = 0 # angle
        self.health   = rnd.randint(0, 100)
    
    def update(self, input_array):
        ns = math.cos(self.rotation)
        ew = math.sin(self.rotation)
        
        # Return velocity and angular velocity
        return 0.1, 0
    
    def randomize_position(self):
        self.position = [rnd.randint(0, 2000) / 1000 - 1, rnd.randint(0, 2000) / 1000 - 1]
    
    def randomize_rotation(self):
        self.rotation = rnd.randint(0, int(2 * math.pi * 1000)) / 1000
    
    def __str__(self):
        return f"Player[id: {self.id}, hp: {self.health}, x: {self.position[0]:.2f}, y: {self.position[1]:.2f}, n/s: {self.rotation[0]:.2f}, e/w: {self.rotation[1]:.2f}]"