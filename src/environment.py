import math

import sys

ROOT8 = math.sqrt(8)

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
        
        boundaries = [
            [(1, -1), (1, 1)],   # right
            [(1, 1), (-1, 1)],   # bottom
            [(-1, 1), (-1, -1)], # left
            [(-1, -1), (1, -1)], # top
        ]
        
        """
        Remove later:
            1. Get list of intersections for each ray.
            2. Get closest intersection for each ray.
            3. Set distances for each ray in neural network input.
            4. Set types of objects intersected with in neural network input.
                E.g. wall=+1, enemy=-1, else=0
            5. Get neural network output.
            6. Update player properties.
        """
        
        ## For every player.
        for player in self.players:
            # Cast rays.
            start_angle = player.rotation - ((self.num_rays - 1) / 2) * self.ray_sep_angle
            ray_angles = [start_angle + i * self.ray_sep_angle for i in range(self.num_rays)]
            for ray_angle in ray_angles:
                # Calculate intersection between ray line and environment boundary.
                player_x = player.position[0]
                player_y = player.position[1]
                ray_end_x = player_x + math.cos(ray_angle) * ROOT8
                ray_end_y = player_y + math.sin(ray_angle) * ROOT8
                
                # Left boundary.
                intersections = []
                for line in boundaries:
                    intersects, intersect_distance = cast_ray(l1=[(player_x, player_y), ray_angle], l2=line)
                    if intersects:
                        intersections.append(intersect_distance)
                if len(intersections) > 0:
                    print(player.id, intersections)
                    sys.stdout.flush()
            
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

def rotate_point(point, alpha):
    x, y = point
    new_x = x * math.cos(alpha) - y * math.sin(alpha)
    new_y = x * math.sin(alpha) + y * math.cos(alpha)
    return (new_x, new_y)

def close_enough(v1, v2, tolerance=1e-12):
    return abs(v1 - v2) <= tolerance

def cast_ray(l1, l2):
    # l1: (origin, direction)
    # l2: (start, end)
    # Rotate l1 and l2 so that l1 is vertical.
    rotate_angle = math.pi / 2 - l1[1]
    l1_new = [rotate_point(l1[0], rotate_angle), l1[1] + rotate_angle]
    l2_new = [rotate_point(l2[0], rotate_angle), \
        rotate_point(l2[1], rotate_angle)]
    l2_start = l2_new[0]
    l2_end   = l2_new[1]
    
    # Check if both points of l2 are on the left or on the right of l1.
    if l2_start[0] < l1_new[0][0] and l2_end[0] < l1_new[0][0] \
        and not close_enough(l2_start[0], l1_new[0][0]) \
        and not close_enough(l2_end[0], l1_new[0][0]):
        return False, 0
    if l2_start[0] > l1_new[0][0] and l2_end[0] > l1_new[0][0] \
        and not close_enough(l2_start[0], l1_new[0][0]) \
        and not close_enough(l2_end[0], l1_new[0][0]):
        return False, 0
    
    # Check if both points of l2 are below l1.
    if l2_start[1] < l1_new[0][1] and l2_end[1] < l1_new[0][1]:
        return False, 0
    
    # Check if both points of l2 are on l1 x.
    if close_enough(l2_start[0], l1_new[0][0]) and close_enough(l2_end[0], l1_new[0][0]):
        # Check if either of the points are on or below l1y.
        if l2_start[1] <= l1_new[0][1] or l2_end[1] <= l1_new[0][1]:
            return True, 0
        elif close_enough(l2_start[1], l1_new[0][1]) or close_enough(l2_end[1], l1_new[0][1]):
            return True, 0
        else:
            distance = min(l2_start[1], l2_end[1]) - l1_new[0][1]
            return True, distance
    
    # Check if either point of l2 is on l1.
    if close_enough(l2_start[0], l1_new[0][0]):
        # Check if the point of l2 is below l1 y.
        if l2_start[1] < l1_new[0][1]:
            return False, 0
        else:
            distance = l2_start[1] - l1_new[0][1]
            return True, distance
    if close_enough(l2_end[0], l1_new[0][0]):
        # Check if the point of l2 is below l1 y.
        if l2_end[1] < l1_new[0][1]:
            return False, 0
        else:
            distance = l2_end[1] - l1_new[0][1]
            return True, distance
    
    # Check if l2 is vertical.
    if close_enough(l2_start[0], l2_end[0]):
        # We already know that both points of l2 do not lie on l1.
        return False, 0
    
    # Calculate line coefficients for l2 and calculate point of intersection.
    a = (l2_end[1] - l2_start[1]) / (l2_end[0] - l2_start[0])
    b = l2_start[1] - a * l2_start[0]
    y = a * l1_new[0][0] + b
    if y < l1_new[0][1]:
        return False, 0
    else:
        return True, y - l1_new[0][1]

def cast_ray_circle(l1, c):
    # l1: (origin, direction)
    # c : (origin, radius)
    # Move line and circle so that the line starts at the origin.
    l1_start = l1[0]
    l1_translate = [(l1_start[0] - l1_start[0], l1_start[1] - l1_start[1]), l1[1]]
    c_start = c[0]
    c_translate = [(c_start[0] - l1_start[0], c_start[1] - l1_start[1]), c[1]]
    
    # Rotate line and circle so that the line is vertical.
    rotate_angle = math.pi / 2 - l1[1]
    l1_new = [rotate_point(l1_translate[0], rotate_angle), l1[1] + rotate_angle]
    c_new = [rotate_point(c_translate[0], rotate_angle), c_translate[1]]
    
    # Check if circle is completely 'behind' the line.
    if c_new[0][1] < -c_new[1]:
        return False, 0
    
    # Check if circle x is less than -radius or greater than +radius.
    if c_new[0][0] < -c_new[1]:
        return False, 0
    if c_new[0][0] > c_new[1]:
        return False, 0
    
    # Check if line start is in the circle.
    circle_dist_from_origin_sq = c_new[0][0] * c_new[0][0] + c_new[0][1] * c_new[0][1]
    if circle_dist_from_origin_sq < c_new[1] * c_new[1]:
        return True, 0
    
    # There is an intersection here, calculate intersection point and return distance.
    x = 0
    y_pos = c_new[0][1] + math.sqrt(c_new[1] ** 2 - (x - c_new[0][0]) ** 2)
    y_neg = c_new[0][1] - math.sqrt(c_new[1] ** 2 - (x - c_new[0][0]) ** 2)
    return True, min(y_neg, y_pos)
