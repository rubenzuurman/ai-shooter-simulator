import math
import multiprocessing as mp
import time

import pygame

from environment import Environment
from player import Player

import sys
import copy

class MatchMaking:
    """
    Functionalities:
        Add player to ranking system.
        Add player to matchmaking queue.
        Match players in queue based on ranking, create environment, and start match.
        Update ranking when a match is done.
        
        Serialization and deserialization.
    
    Start ranking points: 1000
    Difference in points at 90% winrate: 100
    """
    
    def __init__(self, player_size=0.2, ticks_per_second=50, num_rays=5, \
        ray_sep_angle=0.1):
        # Player objects.
        self.players = []
        # Player ids and ranking scores.
        self.leaderboard = {}
        # Player ids in queue.
        self.queue = []
        # Environments containing matches (list of environments).
        manager = mp.Manager()
        self.matches = manager.dict()
        
        # Player size (the environment size is 2.0), ticks per second, number 
        # of rays, and ray separation angle.
        self.player_size = player_size
        self.ticks_per_second = ticks_per_second
        # Make sure number of rays is always odd
        self.num_rays = num_rays if num_rays % 2 == 1 else num_rays + 1
        self.ray_sep_angle = ray_sep_angle
        
        # Keep track of match number.
        self.match_number = 0
        
        # Dictionary containing status reports of the matches from the other process.
        self.status_dict = manager.dict()
        self.status_dict["running"] = True
        
        # Start process handling matches.
        self.match_proc = mp.Process(target=handle_matches, args=(self.matches, self.status_dict))
        self.match_proc.start()
    
    def render(self, display, font, window_dimensions):
        # Rendering of matches
        num_matches = len(self.status_dict) - 1
        counter = 1
        match_layout = None
        while match_layout is None:
            if counter * (counter - 1) >= num_matches:
                match_layout = (counter, counter - 1)
            elif counter * counter >= num_matches:
                match_layout = (counter, counter)
            counter += 1
        
        render_width = window_dimensions[0] * 0.8
        render_offset = [(window_dimensions[0] - render_width) / 2, 50]
        
        render_index = 0
        for key, status in self.status_dict.items():
            if key == "running":
                continue
            
            # Calculate render window position and dimensions.
            window_x, window_y, window_w, window_h = self.calculate_render_window_properties(render_offset, render_width, match_layout[0], render_index)
            
            ticks_per_second = status["ticks_per_second"]
            current_tick = status["current_tick"]
            current_time = status["current_time"]
            
            pygame.draw.rect(display, (255, 255, 255), (window_x, window_y, \
                window_w, window_h), width=1)
            
            for player_id, player_data in status.items():
                if not isinstance(player_id, int):
                    continue
                
                # Calculate screen position.
                map_position = player_data["pos"]
                map_position_flipped = [(map_position[0] + 1) / 2, (-map_position[1] + 1) / 2]
                screen_x = window_x + map_position_flipped[0] * window_w
                screen_y = window_y + map_position_flipped[1] * window_h
                
                # Render player.
                pygame.draw.circle(display, (0, 100, 0), (screen_x, screen_y), window_w / 2 * self.player_size / 2, width=2)
                
                # Render healthbar.
                healthbar_green_width = (player_data["hp"] / 100) * 50
                healthbar_start = screen_x - 25
                healthbar_start_mid = screen_x - 25 + healthbar_green_width
                pygame.draw.rect(display, (10, 150, 10), (healthbar_start, screen_y - 25, healthbar_green_width, 10))
                pygame.draw.rect(display, (150, 10, 10), (healthbar_start_mid, screen_y - 25, 50 - healthbar_green_width, 10))
                
                # Render rays.
                start_angle = player_data["rot"] - ((self.num_rays - 1) / 2) * self.ray_sep_angle
                ray_angles = [start_angle + i * self.ray_sep_angle for i in range(self.num_rays)]
                for a in ray_angles:
                    line_start_x = screen_x
                    line_start_y = screen_y
                    line_end_x = line_start_x + math.cos(a) * 100
                    line_end_y = line_start_y - math.sin(a) * 100
                    pygame.draw.line(display, (0, 255, 255), (line_start_x, line_start_y), (line_end_x, line_end_y))
                
                # Render position text.
                render_text_center(display, f"{map_position[0]:.2f}, {map_position[1]:.2f}", (screen_x, screen_y - 30), font)
            
            render_index += 1
    
    def calculate_render_window_properties(self, offset, available_width, number_of_columns, render_index):
        # Assuming 5% spacing between windows.
        render_width = available_width / (1.05 * number_of_columns + 0.05)
        margin_width = 0.05 * render_width
        
        layout_x = render_index % number_of_columns
        layout_y = render_index // number_of_columns
        
        render_x = margin_width
        render_x += layout_x * (render_width + margin_width)
        render_y = margin_width
        render_y += layout_y * (render_width + margin_width)
        
        return [offset[0] + render_x, offset[1] + render_y, render_width, render_width]
    
    def update(self):
        ## Handling of queue, creating new matches, and updating of ranking system
        # Check if any two players are no more than 400 ranking points apart.
        match_created = True
        while len(self.queue) > 1 and match_created:
            match_created = False
            for p1 in self.queue:
                for p2 in self.queue:
                    if p1 == p2:
                        continue
                    
                    p1_ranking = self.leaderboard[p1]
                    p2_ranking = self.leaderboard[p2]
                    if abs(p1_ranking - p2_ranking) <= 400:
                        env = Environment(player_size=self.player_size, ticks_per_second=self.ticks_per_second, num_rays=self.num_rays, ray_sep_angle=self.ray_sep_angle)
                        env.add_player(copy.deepcopy(self.players[p1]))
                        env.add_player(copy.deepcopy(self.players[p2]))
                        self.matches[self.match_number] = env
                        self.match_number += 1
                        indices_to_remove = []
                        for index, q in enumerate(self.queue):
                            if q == p1 or q == p2:
                                indices_to_remove.append(index)
                        for index in reversed(indices_to_remove):
                            del self.queue[index]
                        match_created = True
                    
                    if match_created:
                        break
                if match_created:
                    break
            
            if match_created:
                print(f"Queue: {self.queue}")
                print(f"Matches: {self.matches}")
        
        # Update ranking system if any match has finished.
        for index, match in self.matches.items():
            match.step()
    
    def add_player(self, player):
        if not isinstance(player, Player):
            print(f"Player must be an instance of Player, not '{type(player)}'.")
            return
        
        # Add player to ranking system
        self.players.append(player)
        self.leaderboard[player.id] = 1000
        
        print(f"Leaderboard: {self.leaderboard}")
    
    def add_player_to_queue(self, player_id):
        # Check if the player exists
        player_exists = False
        for player in self.players:
            if player.id == player_id:
                player_exists = True
                break
        if not player_exists:
            print(f"Player with id '{player_id}' does not exist.")
            return
        
        # Check if the player is not already in the queue
        if player_id in self.queue:
            print(f"Player with id '{player_id}' is already in the queue.")
            return
        
        # Check if the player is not in a match
        for index, match in self.matches.items():
            if player_id in [player.id for player in match.players]:
                print(f"Player with id '{player_id}' is in a match.")
                return
        
        # Add player to queue
        self.queue.append(player_id)
        
        print(f"Queue: {self.queue}")
    
    def quit(self):
        self.status_dict["running"] = False
        self.match_proc.join()

def handle_matches(matches_dict, status_dict):
    while True:
        for index, match in matches_dict.items():
            #if index in status_dict.keys():
            #    print("before", status_dict[index])
            result, finished = match.step()
            status_dict[index] = result
            #print("after ", status_dict[index])
            #print("result", result)
            matches_dict[index] = match
        
        #print()
        #sys.stdout.flush()
        
        time.sleep(0.1)
        if not status_dict["running"]:
            break

def render_text(display, text, position, font, color=(255, 255, 255)):
    text_surface = font.render(text, False, color)
    display.blit(text_surface, position)

def render_text_center(display, text, position, font, color=(255, 255, 255)):
    # Create text surface.
    text_surface = font.render(text, False, color)
    
    # Update position to center the text.
    position_x = position[0] - text_surface.get_width() / 2
    position_y = position[1] - text_surface.get_height() / 2
    
    # Render text.
    display.blit(text_surface, (position_x, position_y))
