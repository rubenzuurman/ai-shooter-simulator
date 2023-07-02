import math
import random as rnd
import time

DEFAULT_NUM_RAYS = 5
DEFAULT_RAY_SEP_ANGLE = 0.1

# Maximum player health (also start player health)
MAX_HEALTH = 100
# Bullet damage, max player health is 100
BULLET_DAMAGE = 50
# Weapon cooldown in seconds
WEAPON_COOLDOWN = 1.0

class Player:
    
    PLAYER_ID = 0
    
    def __init__(self, num_rays=DEFAULT_NUM_RAYS, ray_sep_angle=DEFAULT_RAY_SEP_ANGLE, initial_health=MAX_HEALTH, bullet_damage=BULLET_DAMAGE, weapon_cooldown=WEAPON_COOLDOWN):
        # Set player id.
        self.id = Player.PLAYER_ID
        Player.PLAYER_ID += 1
        
        # Set other player properties.
        self.position = [0, 0] # x, y
        self.rotation = 0 # angle
        self.health   = initial_health
        self.bullet_damage = bullet_damage
        self.weapon_cooldown = weapon_cooldown
        
        self.last_weapon_activation = 0
        
        # Set player name and color.
        self.name = get_random_name()
        self.color = get_random_color()
        
        # Player metadata, used to keep track of intersect distances for now.
        self.metadata = {"intersect_distances": []}
        
        # Number of rays and ray separation angle.
        # Make sure number of rays is always odd.
        self.num_rays = num_rays if num_rays % 2 == 1 else num_rays + 1
        self.ray_sep_angle = ray_sep_angle
    
    def update(self, input_array):
        ns = math.cos(self.rotation)
        ew = math.sin(self.rotation)
        
        # Return velocity, angular velocity, and activate weapon output 
        # (probably (at least currently) active when value is greater than 0).
        return 0.1, 0, 0.5
    
    def use_weapon(self):
        self.last_weapon_activation = time.time()
    
    def can_use_weapon(self):
        return time.time() - self.last_weapon_activation > self.weapon_cooldown
    
    def remove_health(self, amount):
        self.health -= amount
    
    def get_metadata(self):
        return self.metadata
    
    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color
    
    def randomize_position(self):
        self.position = [rnd.randint(0, 2000) / 1000 - 1, rnd.randint(0, 2000) / 1000 - 1]
    
    def randomize_rotation(self):
        self.rotation = rnd.randint(0, int(2 * math.pi * 1000)) / 1000
    
    def __str__(self):
        return f"Player[id: {self.id}, hp: {self.health}, x: {self.position[0]:.2f}, y: {self.position[1]:.2f}, n/s: {self.rotation[0]:.2f}, e/w: {self.rotation[1]:.2f}]"

def get_random_name():
    with open("doc/random_names.txt", "r") as file:
        lines = file.readlines()
    
    return lines[rnd.randint(0, len(lines) - 1)].strip()

def get_random_color():
    with open("doc/random_colors.txt", "r") as file:
        lines = file.readlines()
    
    random_color = lines[rnd.randint(0, len(lines) - 1)].strip()
    color_rgb_str = random_color[1:-1].split(",")
    return tuple(map(int, color_rgb_str))
