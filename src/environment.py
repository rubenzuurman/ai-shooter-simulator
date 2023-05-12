import math

import sys

class Environment:
    
    ENVIRONMENT_ID = 0
    
    def __init__(self, player_size, ticks_per_second, num_rays, ray_sep_angle):
        # Environment spans from -1 to +1.
        self.id = Environment.ENVIRONMENT_ID
        Environment.ENVIRONMENT_ID += 1
        
        self.players = []
        self.player_size = player_size
        self.ticks_per_second = ticks_per_second
        self.num_rays = num_rays
        self.ray_sep_angle = ray_sep_angle
        
        self.current_tick = 0
    
    def add_player(self, player):
        # Randomize position and rotation.
        player.randomize_position()
        player.randomize_rotation()
        self.players.append(player)
    
    def step(self):
        delta_time = 1 / self.ticks_per_second
        
        #print([player.position for player in self.players])
        
        ## For every player.
        for player in self.players:
            # Cast rays.
            start_angle = player.rotation - ((self.num_rays - 1) / 2) * self.ray_sep_angle
            ray_angles = [start_angle + i * self.ray_sep_angle for i in range(self.num_rays)]
            for ray_angle in ray_angles:
                # Calculate intersection between ray line and environment boundary.
                player_x = player.position[0]
                player_y = player.position[1]
                ray_end_x = player_x + math.cos(ray_angle) * 2
                ray_end_y = player_y + math.sin(ray_angle) * 2
                
                # Left boundary.
                ray_angle_mod = ray_angle % 2 * math.pi
                if ray_angle_mod > math.pi / 2 and ray_angle_mod < 3 * math.pi / 2:
                    continue
            
            # Get velocity and angular velocity from players by calling the 
            # update method.
            velocity, angular_velocity = player.update([0, 0, 0, 0, 0])
            
            # Check for collisions.
            vx = velocity * math.cos(player.rotation)
            vy = velocity * math.sin(player.rotation)
            new_x = player.position[0] + vx * delta_time
            new_y = player.position[1] + vy * delta_time
            if new_x < -1 + self.player_size / 2:
                new_x = -1 + self.player_size / 2
            if new_x > +1 - self.player_size / 2:
                new_x = +1 - self.player_size / 2
            if new_y < -1 + self.player_size / 2:
                new_y = -1 + self.player_size / 2
            if new_y > +1 - self.player_size / 2:
                new_y = +1 - self.player_size / 2
            
            # Update player positions and rotations.
            player.position = [new_x, new_y]
            player.rotation += angular_velocity * delta_time
        
        #print([player.position for player in self.players])
        #sys.stdout.flush()
        
        ## For every player.
        # Shoot bullets if necessary.
        
        # Update player health.
        
        ## End
        # Report back player positions and rotations and health and if the 
        # match is finished or not.
        
        self.current_tick += 1
        
        result = {}
        for player in self.players:
            result[player.id] = {"pos": player.position, "rot": player.rotation, "hp": player.health}
        result["ticks_per_second"] = self.ticks_per_second
        result["current_tick"] = self.current_tick
        result["current_time"] = self.current_tick / self.ticks_per_second
        return result, False