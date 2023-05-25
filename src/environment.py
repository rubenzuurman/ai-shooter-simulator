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
                #ray_angle_mod = ray_angle % 2 * math.pi
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
    
    return True, -1

def test_cast_ray():
    tests = []
    # L1 vertical up
    ## L2 vertical x diff y1&&y2 < l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-1, -5), (-1, -8)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 && y2<ly1"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-1, 1), (-1, -8)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 && y2<ly1 y1 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-1, -8), (-1, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 && y2<ly1 reverse y2 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-1, 1), (-1, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 && y2<ly1 reverse y1 eq y2 eq"
    })
    
    ## L2 vertical x diff y1^y2 < l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-2, 5), (-2, -3)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 ^  y2<ly1 y1>"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-2, -2), (-2, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 ^  y2<ly1 y2>"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-2, 5), (-2, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 ^  y2<ly1 y1> y2 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-2, 1), (-2, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1<ly1 ^  y2<ly1 y2> y1 eq"
    })
    
    ## L2 vertical x diff y1&&y2 > l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 6), (-3, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 3), (-3, 7)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 reverse"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 1), (-3, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 y1 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 3), (-3, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 y2 eq reverse"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-3, 1), (-3, 1)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 y1 eq y2 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(-5, 4), (-5, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x diff y1>ly1 && y2>ly1 y1 eq y2 eq 2"
    })
    
    ## L2 vertical x same y1&&y2 < l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, -5), (2, -8)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 && y2<ly1"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, -8)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 && y2<ly1 y1 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, 1)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 && y2<ly1 reverse y1 eq y2 eq"
    })
    
    ## L2 vertical x same y1^y2 < l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 5), (2, -3)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 ^  y2<ly1 y1>"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, -2), (2, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 ^  y2<ly1 y2>"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 5), (2, 1)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 ^  y2<ly1 y1> y2 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1<ly1 ^  y2<ly1 y2> y1 eq"
    })
    
    ## L2 vertical x same y1&&y2 > l1y
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 6), (2, 4)], 
        "out": [True, 3], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 3), (2, 7)], 
        "out": [True, 2], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 reverse"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 3), (2, 1)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y2 eq reverse"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 1), (2, 1)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq"
    })
    tests.append({
        "l1": [(-15, 24), math.pi / 2], 
        "l2": [(-15, 24), (-15, 24)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq 2"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 3), (2, 3)], 
        "out": [True, 2], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq x"
    })
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(2, 7.5), (2, 7.5)], 
        "out": [True, 6.5], 
        "name": "L1 vertical up, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq x 2"
    })
    
    ## L2 not vertical
    tests.append({
        "l1": [(2, 1), math.pi / 2], 
        "l2": [(5, -2), (1, 10)], 
        "out": [True, 6], 
        "name": "L1 vertical up, l2 not vertical test 1 normal"
    })
    tests.append({
        "l1": [(5, -2), math.pi / 2], 
        "l2": [(3, -5), (2, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical up, l2 not vertical test 2 normal"
    })
    tests.append({
        "l1": [(2, -3), math.pi / 2], 
        "l2": [(-10, -3), (8, 9)], 
        "out": [True, 8], 
        "name": "L1 vertical up, l2 not vertical test 3 normal"
    })
    tests.append({
        "l1": [(5, 3.5), math.pi / 2], 
        "l2": [(-4, 2), (8, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 not vertical test 4 l2 through p1"
    })
    tests.append({
        "l1": [(5, 3.5), math.pi / 2], 
        "l2": [(5, 3.5), (5, 3.5)], 
        "out": [True, 0], 
        "name": "L1 vertical up, l2 not vertical test 4 l2 eq p1"
    })
    
    
    # L1 vertical down
    ## L2 vertical x diff y1&&y2 > l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(2, 3), (2, 7)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 && y2>ly1"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(2, 2), (2, 3)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 && y2>ly1 y1 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(2, 7), (2, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 && y2>ly1 reverse y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(2, 2), (2, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 && y2>ly1 reverse y1 eq y2 eq"
    })
    
    ## L2 vertical x diff y1^y2 > l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(1, -5), (1, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 ^  y2>ly1 y1<"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(1, 7), (-2, -3)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 ^  y2>ly1 y2<"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(5, -4), (5, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 ^  y2>ly1 y1< y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-2, 2), (-2, -6)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1>ly1 ^  y2>ly1 y2< y1 eq"
    })
    
    ## L2 vertical x diff y1&&y2 < l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-3, 1), (-3, -4)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-3, 2), (-3, -5)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1 y1 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-3, -4), (-3, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1 y2 eq reverse"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(-3, 2), (-3, 2)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1 y1 eq y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(11, -14), (11, -14)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x diff y1<ly1 && y2<ly1 y1 eq y2 eq"
    })
    
    ## L2 vertical x same y1&&y2 > l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 3), (3, 5)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 7), (3, 2.5)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 reverse"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, 4)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 y1 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 6.5), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 reverse y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 reverse y1 eq y2 eq"
    })
    
    ## L2 vertical x same y1^y2 > l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -4), (3, 5)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 ^  y2>ly1 y1<"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 4), (3, -3)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 ^  y2>ly1 y2<"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -9), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 ^  y2>ly1 y1< y2 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, -6)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 ^  y2>ly1 y2< y1 eq"
    })
    
    ## L2 vertical x same y1&&y2 < l1y
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -8), (3, -4.5)], 
        "out": [True, 6.5], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -5), (3, -10)], 
        "out": [True, 7], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 reverse"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, -4)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 y1 eq"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -6), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 y2 eq reverse"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, 2), (3, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 y1 eq y2 eq"
    })
    tests.append({
        "l1": [(-10, 25), 3 * math.pi / 2], 
        "l2": [(-10, 25), (-10, 25)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 vertical x same y1<ly1 && y2<ly1 y1 eq y2 eq 2"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -4), (3, -4)], 
        "out": [True, 6], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq x"
    })
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(3, -6.5), (3, -6.5)], 
        "out": [True, 8.5], 
        "name": "L1 vertical down, l2 vertical x same y1>ly1 && y2>ly1 y1 eq y2 eq x 2"
    })
    
    ## L2 not vertical
    tests.append({
        "l1": [(3, 2), 3 * math.pi / 2], 
        "l2": [(6, 3.5), (-8, -7)], 
        "out": [True, 0.75], 
        "name": "L1 vertical down, l2 not vertical test 1 normal"
    })
    tests.append({
        "l1": [(5, -2), 3 * math.pi / 2], 
        "l2": [(-8, 6), (12, 4)], 
        "out": [False, 0], 
        "name": "L1 vertical down, l2 not vertical test 2 normal"
    })
    tests.append({
        "l1": [(-4, 0), 3 * math.pi / 2], 
        "l2": [(6, 1.5), (-10.5, -6)], 
        "out": [True, 3.04545454545], 
        "name": "L1 vertical down, l2 not vertical test 3 normal"
    })
    tests.append({
        "l1": [(-2, 3), 3 * math.pi / 2], 
        "l2": [(-5, 4), (1, 2)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 not vertical test 4 l2 through p1"
    })
    tests.append({
        "l1": [(2, -4), 3 * math.pi / 2], 
        "l2": [(2, -4), (2, -4)], 
        "out": [True, 0], 
        "name": "L1 vertical down, l2 not vertical test 4 l2 eq p1"
    })
    
    # L1 not vertical
    ## L2 vertical TODO: check all of these, intersect with l1 direction is also intersection.
    tests.append({
        "l1": [(3, 2), 2.456], 
        "l2": [(-6, 12), (-6, 4)], 
        "out": [True, 11.6272466696], 
        "name": "L1 not vertical, l2 vertical test 1"
    })
    tests.append({
        "l1": [(3, 2), 2.456], 
        "l2": [(4, 12), (4, 4)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 2 no intersect"
    })
    tests.append({
        "l1": [(3, 2), 4], 
        "l2": [(4, 12), (4, 4)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 3 no intersect"
    })
    tests.append({
        "l1": [(3, 2), 4], 
        "l2": [(4, 12), (4, 2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 4 no intersect"
    })
    tests.append({
        "l1": [(3, 2), 4], 
        "l2": [(2, 12), (2, -2)], 
        "out": [True, 1.52988565647], 
        "name": "L1 not vertical, l2 vertical test 5"
    })
    tests.append({
        "l1": [(3, 2), 4], 
        "l2": [(2.5, 12), (2.5, -2)], 
        "out": [True, 0.764942828233], 
        "name": "L1 not vertical, l2 vertical test 6"
    })
    tests.append({
        "l1": [(3, 2), 5], 
        "l2": [(2.5, 12), (2.5, -2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 7 no intersect"
    })
    tests.append({
        "l1": [(4, 1), 5], 
        "l2": [(4.1, 12), (4.1, -2)], 
        "out": [True, 0.352532008582], 
        "name": "L1 not vertical, l2 vertical test 8"
    })
    tests.append({
        "l1": [(4, 1), 5], 
        "l2": [(4.1, 12), (4.1, 0.7)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 vertical test 9 no intersect"
    })
    tests.append({
        "l1": [(4, 1), 1], 
        "l2": [(4.1, 12), (4.1, 0.7)], 
        "out": [True, 0.185081571768], 
        "name": "L1 not vertical, l2 vertical test 10"
    })
    tests.append({
        "l1": [(4, 1), 3.5], 
        "l2": [(4, 12), (4, 0.9)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 vertical test 11 touches p1"
    })
    tests.append({
        "l1": [(4, 1), 3.5], 
        "l2": [(4, 12), (4, 1)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 vertical test 12 l2 end on p1"
    })
    tests.append({
        "l1": [(4, 1), 3.5], 
        "l2": [(4, 1), (4, 12)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 vertical test 13 l2 start on p1"
    })
    tests.append({
        "l1": [(4, 1), 3.5], 
        "l2": [(4, 1), (4, 1)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 vertical test 14 l2 start and end on p1"
    })
    
    ## L2 not vertical
    # Both horizontal
    tests.append({
        "l1": [(4, 1), 0], 
        "l2": [(3, 2), (5, 2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 1 both horizontal no intersect"
    })
    tests.append({
        "l1": [(4, 1), math.pi], 
        "l2": [(10, -2), (-3, -2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 2 both horizontal no intersect 2"
    })
    tests.append({
        "l1": [(2, 2), 0], 
        "l2": [(-3, 2), (1, 2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 3 both horizontal intersect l2 before p1"
    })
    tests.append({
        "l1": [(2, 2), math.pi], 
        "l2": [(4, 2), (6, 2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 4 both horizontal intersect l2 before p1 other way"
    })
    tests.append({
        "l1": [(2, 2), 0], 
        "l2": [(4, 2), (6, 2)], 
        "out": [True, 2], 
        "name": "L1 not vertical, l2 not vertical test 5 both horizontal intersect l2 after p1"
    })
    tests.append({
        "l1": [(2, 2), math.pi], 
        "l2": [(-3, 2), (1, 2)], 
        "out": [True, 1], 
        "name": "L1 not vertical, l2 not vertical test 6 both horizontal intersect l2 after p1 other way"
    })
    tests.append({
        "l1": [(2, 3), 0], 
        "l2": [(-5, 3), (10, 3)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 not vertical test 7 both horizontal intersect l2 around p1"
    })
    tests.append({
        "l1": [(2, 3), 0], 
        "l2": [(2, 3), (10, 3)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 not vertical test 8 both horizontal intersect l2 around p1 l2 start on p1"
    })
    tests.append({
        "l1": [(2, 3), 0], 
        "l2": [(-5, 3), (2, 3)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 not vertical test 9 both horizontal intersect l2 around p1 l2 end on p1"
    })
    tests.append({
        "l1": [(2, 3), 0], 
        "l2": [(2, 3), (2, 3)], 
        "out": [True, 0], 
        "name": "L1 not vertical, l2 not vertical test 10 both horizontal intersect l2 around p1 l2 start and end on p1"
    })
    
    # l1 not horizontal
    tests.append({
        "l1": [(2, 3), 0.5], 
        "l2": [(2, 5), (5, 5)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 11 l1 not horizontal q1 no intersect"
    })
    tests.append({
        "l1": [(2, 3), 0.5], 
        "l2": [(2, 5), (5.7, 5)], 
        "out": [True, 4.17165928587], 
        "name": "L1 not vertical, l2 not vertical test 12 l1 not horizontal q1 intersect"
    })
    
    tests.append({
        "l1": [(2, 3), 2], 
        "l2": [(2, 5), (7, 5)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 13 l1 not horizontal q2 no intersect"
    })
    tests.append({
        "l1": [(2, 3), 2], 
        "l2": [(-2, 5), (7, 5)], 
        "out": [True, 2.19950034059], 
        "name": "L1 not vertical, l2 not vertical test 14 l1 not horizontal q2 intersect"
    })
    
    tests.append({
        "l1": [(2, 3), 4.5], 
        "l2": [(1.5, -1), (6, -1)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 15 l1 not horizontal q3 no intersect"
    })
    tests.append({
        "l1": [(2, 3), 4.5], 
        "l2": [(1, -1), (6, -1)], 
        "out": [True, 4.09194553469], 
        "name": "L1 not vertical, l2 not vertical test 16 l1 not horizontal q3 intersect"
    })
    
    tests.append({
        "l1": [(2, 3), 5.5], 
        "l2": [(1, -1), (6, -1)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 17 l1 not horizontal q4 no intersect"
    })
    tests.append({
        "l1": [(2, 3), 5.5], 
        "l2": [(1, -1), (6.5, -1)], 
        "out": [True, 5.66941371745], 
        "name": "L1 not vertical, l2 not vertical test 18 l1 not horizontal q4 intersect"
    })
    
    # l2 not horizontal
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(1, 5), (3, 3.5)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 19 l2 not horizontal l1 right test 1 no intersect"
    })
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(3, 6), (-2, 1)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 20 l2 not horizontal l1 right test 2 no intersect"
    })
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(1, -3), (8, 6)], 
        "out": [True, 4.66666666667], 
        "name": "L1 not vertical, l2 not vertical test 21 l2 not horizontal l1 right test 3 intersect"
    })
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(7, -3), (-2.5, 7.5)], 
        "out": [True, 0.571428571429], 
        "name": "L1 not vertical, l2 not vertical test 22 l2 not horizontal l1 right test 4 intersect"
    })
    tests.append({
        "l1": [(1, 3), 0], 
        "l2": [(0, -3), (10, 8)], 
        "out": [True, 4.45454545455], 
        "name": "L1 not vertical, l2 not vertical test 23 l2 not horizontal l1 right test 5 intersect"
    })
    
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(0, -3), (10, 8)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 19 l2 not horizontal l1 left test 1 no intersect"
    })
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(-1, 6), (5, -2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 20 l2 not horizontal l1 left test 2 no intersect"
    })
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(-1, 6), (4, -3)], 
        "out": [True, 0.333333333333], 
        "name": "L1 not vertical, l2 not vertical test 21 l2 not horizontal l1 left test 3 intersect"
    })
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(2, 6), (-3, -4.5)], 
        "out": [True, 0.428571428571], 
        "name": "L1 not vertical, l2 not vertical test 22 l2 not horizontal l1 left test 4 intersect"
    })
    tests.append({
        "l1": [(1, 3), math.pi], 
        "l2": [(5, 4), (-10, 2.25)], 
        "out": [True, 4.57142857143], 
        "name": "L1 not vertical, l2 not vertical test 23 l2 not horizontal l1 left test 5 intersect"
    })
    
    # Both not horizontal but parallel
    tests.append({
        "l1": [(1, 3), math.pi / 4], 
        "l2": [(5, 4), (-1, -2)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 24 both not horizontal but parallel"
    })
    tests.append({
        "l1": [(1, 3), 5 * math.pi / 8], 
        "l2": [(1, 1), (1 + 5 * math.cos(5 * math.pi / 8), 1 + 5 * math.sin(5 * math.pi / 8))], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 25 both not horizontal but parallel 2"
    })
    tests.append({
        "l1": [(1, 3), 1.234], 
        "l2": [(1, 1), (1 + 10 * math.cos(1.234), 1 + 10 * math.sin(1.234))], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 26 both not horizontal but parallel 3"
    })
    
    # Both not horizontal but not quite parallel
    tests.append({
        "l1": [(1, 3), math.pi / 4 - 0.001], 
        "l2": [(5, 6), (-1, 0)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 27 both not horizontal but not quite parallel"
    })
    tests.append({
        "l1": [(1, 3), 5 * math.pi / 8 - 0.02], 
        "l2": [(1, 1), (1 + 6 * math.cos(5 * math.pi / 8), 1 + 6 * math.sin(5 * math.pi / 8))], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 28 both not horizontal but not quite parallel 2"
    })
    tests.append({
        "l1": [(1, 3), 1.234 - 0.2], 
        "l2": [(1, 1), (1 + 3 * math.cos(1.234), 1 + 3 * math.sin(1.234))], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 29 both not horizontal but not quite parallel 3"
    })
    
    # Both not horizontal not parallel
    tests.append({
        "l1": [(1, 3), 1.234 - 0.2], 
        "l2": [(1, 2), (1 + 3 * math.cos(1.234), 2 + 3 * math.sin(1.234))], 
        "out": [True, 1.66339266735], 
        "name": "L1 not vertical, l2 not vertical test 30 both not horizontal but not parallel 1 intersect"
    })
    tests.append({
        "l1": [(-1, 2.5), 4.613], 
        "l2": [(2, -0.5), (-3, -2)], 
        "out": [True, 4.04020584779], 
        "name": "L1 not vertical, l2 not vertical test 31 both not horizontal but not parallel 2 intersect"
    })
    tests.append({
        "l1": [(3.2, 4.6), 3.65], 
        "l2": [(0.5, -1.5), (-4, 1.8)], 
        "out": [True, 7.16713212629], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 3 intersect"
    })
    tests.append({
        "l1": [(3.2, 4.6), 3.65], 
        "l2": [(2, 3.9), (-4, 0.6)], 
        "out": [True, 6.29905891177], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 4 intersect"
    })
    
    tests.append({
        "l1": [(3.2, 4.6), 3.64], 
        "l2": [(2, 3.9), (-4, 0.6)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 5 no intersect"
    })
    tests.append({
        "l1": [(1.6, -2.1), 2.9], 
        "l2": [(2.3, 5.23), (-4.7, 1.4)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 6 no intersect"
    })
    tests.append({
        "l1": [(3.2, -2.9), 5.4], 
        "l2": [(4, -2), (-2, 4.3)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 7 no intersect"
    })
    
    tests.append({
        "l1": [(-2.4, 1.3), 1.456], 
        "l2": [(-1, -2.3), (2.8, 4.5)], 
        "out": [False, 0], 
        "name": "L1 not vertical, l2 not vertical test 32 both not horizontal but not parallel 8 no intersect"
    })
    
    test_id = 1
    succeeded = 0
    failed = 0
    total_tests = 0
    
    # Run normal tests.
    print("Normal tests:")
    for test in tests:
        result = cast_ray(test["l1"], test["l2"])
        test_result = test_cast_ray_check_result(result, test["out"])
        pass_string = "passed"
        if not test_result:
            if test_id < 100:
                pass_string = f"failed\t\tname: {test['name']}"
            else:
                pass_string = f"failed\tname: {test['name']}"
            pass_string += f" (expected {test['out']}, got {result})"
            failed += 1
        else:
            succeeded += 1
        if not test_result:
            print(f"Test #{test_id} {pass_string}")
        total_tests += 1
        test_id += 1
    print()
    
    # Run tests with points in l2 reversed.
    print("Test with l2 reversed:")
    for test in tests:
        result = cast_ray(test["l1"], (test["l2"][1], test["l2"][0]))
        test_result = test_cast_ray_check_result(result, test["out"])
        pass_string = "passed"
        if not test_result:
            if test_id < 100:
                pass_string = f"failed\t\tname: {test['name']}"
            else:
                pass_string = f"failed\tname: {test['name']}"
            pass_string += f" (expected {test['out']}, got {result})"
            failed += 1
        else:
            succeeded += 1
        if not test_result:
            print(f"Test #{test_id} {pass_string}")
        total_tests += 1
        test_id += 1
    print()
    
    print(f"Result: {succeeded}/{total_tests} passed ({succeeded / total_tests * 100:.2f}%)")

def test_cast_ray_check_result(result, expected_output):
    result = list(result)
    expected_output = list(expected_output)
    if not result[0] == expected_output[0]:
        return False
    if expected_output[1] == 0:
        if not (result[1] >= -0.000000001 and result[1] <= 0.000000001):
            return False
    else:
        if not (result[1] >= expected_output[1] * 0.999999999 \
            and result[1] <= expected_output[1] * 1.000000001):
            return False
    return True
