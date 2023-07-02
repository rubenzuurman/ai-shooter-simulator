import math
import multiprocessing as mp
import time

import pygame

from environment import Environment, rotate_point
from player import Player

import sys
import copy

ROOT8 = math.sqrt(8)

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
    
    def __init__(self, player_size=0.2, ticks_per_second=50):
        manager = mp.Manager()
        
        # Player objects.
        self.players = {}
        # Player ids and ranking scores.
        self.leaderboard = {}
        # Player ids in queue.
        self.queue = []
        # Environments containing matches (list of environments).
        self.matches = manager.dict()
        
        # Player size (the environment size is 2.0) and ticks per second.
        self.player_size = player_size
        self.ticks_per_second = ticks_per_second
        
        # Keep track of match number.
        self.match_number = 0
        
        # Keep track of player distribution.
        self.player_distribution = {"total": 0, "in_queue": 0, "in_game": 0, "idle": 0}
        
        # Dictionary containing status reports of the matches from the other process.
        self.status_dict = manager.dict()
        self.status_dict["running"] = True
        self.status_dict["ticks_per_second"] = ticks_per_second
        
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
        
        render_width = min(window_dimensions[0] * 0.8, window_dimensions[1] * 0.8)
        render_offset = [(window_dimensions[0] - render_width) / 2, 100]
        
        render_index = 0
        for key, status in self.status_dict.items():
            if key == "running" or key == "ticks_per_second":
                continue
            
            boundaries = [
                [(1, -1), (1, 1)],   # right
                [(1, 1), (-1, 1)],   # bottom
                [(-1, 1), (-1, -1)], # left
                [(-1, -1), (1, -1)], # top
            ]
            
            # Calculate render window position and dimensions.
            window_x, window_y, window_w, window_h = self.calculate_render_window_properties(render_offset, render_width, match_layout[0], render_index)
            
            ticks_per_second = status["ticks_per_second"]
            current_tick = status["current_tick"]
            current_time = status["current_time"]
            
            for line in boundaries:
                map_pos_flipped0 = [(line[0][0] + 1) / 2, (-line[0][1] + 1) / 2]
                map_pos_flipped1 = [(line[1][0] + 1) / 2, (-line[1][1] + 1) / 2]
                
                screen_x0 = window_x + map_pos_flipped0[0] * window_w
                screen_y0 = window_y + map_pos_flipped0[1] * window_h
                screen_x1 = window_x + map_pos_flipped1[0] * window_w
                screen_y1 = window_y + map_pos_flipped1[1] * window_h
                
                pygame.draw.line(display, (255, 255, 255), (screen_x0, screen_y0), (screen_x1, screen_y1))
            
            #pygame.draw.rect(display, (255, 255, 255), (window_x, window_y, \
            #    window_w, window_h), width=1)
            
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
                start_angle = player_data["rot"] - ((player_data["num_rays"] - 1) / 2) * player_data["ray_sep_angle"]
                ray_angles = [start_angle + i * player_data["ray_sep_angle"] for i in range(player_data["num_rays"])]
                for a in ray_angles:
                    line_start_x = screen_x
                    line_start_y = screen_y
                    line_end_x = line_start_x + math.cos(a) * (window_w / 2) * ROOT8
                    line_end_y = line_start_y - math.sin(a) * (window_w / 2) * ROOT8
                    
                    pygame.draw.line(display, (0, 255, 255), (line_start_x, line_start_y), (line_end_x, line_end_y))
                    
                    alpha = math.atan2(line_end_y - line_start_y, line_end_x - line_start_x)
                    """l1_start_rot = rotate_point(l1_start, math.pi / 2 - alpha)
                    l1_end_rot   = rotate_point(l1_end, math.pi / 2 - alpha)
                    
                    l2_start_rot = rotate_point(l2_start, math.pi / 2 - alpha)
                    l2_end_rot   = rotate_point(l2_end, math.pi / 2 - alpha)"""
                    
                    """for line in boundaries:
                        map_pos_flipped0 = [(line[0][0] + 1) / 2, (-line[0][1] + 1) / 2]
                        map_pos_flipped1 = [(line[1][0] + 1) / 2, (-line[1][1] + 1) / 2]
                        
                        map_pos_flipped0_rot = rotate_point(map_pos_flipped0, math.pi / 2 - alpha)
                        map_pos_flipped1_rot = rotate_point(map_pos_flipped1, math.pi / 2 - alpha)
                        
                        screen_x0 = window_x + map_pos_flipped0_rot[0] * window_w
                        screen_y0 = window_y + map_pos_flipped0_rot[1] * window_h
                        screen_x1 = window_x + map_pos_flipped1_rot[0] * window_w
                        screen_y1 = window_y + map_pos_flipped1_rot[1] * window_h
                        
                        pygame.draw.line(display, (0, 255, 0), (screen_x0, screen_y0), (screen_x1, screen_y1))"""
                
                fadetime = 0.25
                if time.time() - player_data["last_weapon_activation"] <= fadetime:
                    opacity = max(time.time() - player_data["last_weapon_activation"], 0) / fadetime
                    pygame.draw.line(display, (0, int(255 * opacity), 0), (screen_x, screen_y), (screen_x + math.cos(player_data["rot"]) * window_w / 2, screen_y - math.sin(player_data["rot"]) * window_w / 2), width=5)
                
                # Render position text.
                render_text_center(display, f"id:{player_id} {map_position[0]:.2f}, {map_position[1]:.2f}", (screen_x, screen_y - 30), font)
            
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
                        env = Environment(player_size=self.player_size, ticks_per_second=self.ticks_per_second)
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
                        
                        # Update player distribution.
                        self.player_distribution["in_game"] += 2
                        self.player_distribution["in_queue"] -= 2
                    
                    if match_created:
                        break
                if match_created:
                    break
            
            if match_created:
                print(f"Queue: {self.queue}")
                print(f"Matches: {self.matches}")
        
        # Update ranking system if any match has finished.
        matches_to_remove = []
        for index, match in self.matches.items():
            if match.is_finished():
                player_ids = [player.id for player in match.players]
                
                if self.status_dict[index]["outcome"] == "tie":
                    print(f"Match {index} between players {tuple(player_ids)} ended in '{self.status_dict[index]['outcome']}'.")
                    # do nothing
                elif self.status_dict[index]["outcome"] == "no tie":
                    winner_id = self.status_dict[index]["winner_id"]
                    loser_id  = self.status_dict[index]["loser_id"]
                    
                    print(f"Match {index} between players {tuple(player_ids)} ended in '{self.status_dict[index]['outcome']}' ({winner_id} won).")
                    
                    # Give points to winner.
                    self.leaderboard[winner_id] += 50
                    self.leaderboard[loser_id]  -= 50
                
                # Queue match to be removed.
                matches_to_remove.append(index)
        
        # Remove finished matches.
        for index in matches_to_remove:
            # Update player distribution.
            self.player_distribution["in_game"] -= len(self.matches[index].players)
            self.player_distribution["idle"] += len(self.matches[index].players)
            
            del self.matches[index]
            del self.status_dict[index]
            print(f"Removed match {index}.")
    
    def add_player(self, player):
        if not isinstance(player, Player):
            print(f"Player must be an instance of Player, not '{type(player)}'.")
            return
        
        # Add player to ranking system
        self.players[player.id]     = player
        self.leaderboard[player.id] = 1000
        
        # Update player distribution.
        self.player_distribution["total"] += 1
        self.player_distribution["idle"] += 1
        
        print(f"Leaderboard: {self.leaderboard}")
    
    def add_player_to_queue(self, player_id):
        # Check if the player exists
        player_exists = False
        for _, player in self.players.items():
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
        
        # Update player distribution.
        self.player_distribution["in_queue"] += 1
        self.player_distribution["idle"] -= 1
        
        print(f"Queue: {self.queue}")
    
    def quit(self):
        self.status_dict["running"] = False
        self.match_proc.join()

def handle_matches(matches_dict, status_dict):
    clock = pygame.time.Clock()
    
    while True:
        for index, match in matches_dict.items():
            # Run environment step.
            result = match.step()
            
            # Update static dict.
            status_dict[index] = result
            
            # Replace match in matches dict to write changes made by the step() function.
            matches_dict[index] = match
        
        # Tick clock (pygame clock is good enough for now).
        clock.tick(status_dict["ticks_per_second"])
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
