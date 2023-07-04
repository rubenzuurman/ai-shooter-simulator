import copy
import math
import multiprocessing as mp
import time

import pygame

from environment import Environment, rotate_point
from player import Player

# Start rating for every player.
START_RATING = 1000
# Rating difference when winning 90% of the time against an opponent (in the long run).
POINT_DIFF_90 = 100

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
        self.manager = mp.Manager()
        
        # Player objects.
        self.players = {}
        # Player ids and ranking scores.
        self.leaderboard = {}
        # Player ids in queue.
        self.queue = []
        # Environments containing matches (list of environments).
        self.matches = self.manager.dict()
        
        # Player size (the environment size is 2.0) and ticks per second.
        self.player_size = player_size
        self.ticks_per_second = ticks_per_second
        
        # Keep track of match number.
        self.match_number = 0
        
        # Keep track of render indices of matches (keys are the match numbers, values are the render indices).
        self.render_indices = {}
        
        # Keep track of player distribution.
        self.player_distribution = {"total": 0, "in_queue": 0, "in_game": 0, "idle": 0}
        
        # Dictionary containing status reports of the matches from the other process.
        self.status_dict = self.manager.dict()
        self.status_dict["running"] = True
        self.status_dict["ticks_per_second"] = ticks_per_second
        
        # List used to track the status dict entry removed bug matches.
        self.its_happening = []
        
        # Start process handling matches.
        self.match_proc = mp.Process(target=handle_matches, args=(self.matches, self.status_dict))
        self.match_proc.start()
    
    def render(self, display, font, window_dimensions, render_options={}):
        ## Fix up render options if necessary.
        # Replace non-bool values with False.
        for k, v in render_options.items():
            if not isinstance(v, bool):
                render_options[k] = False
        
        # Add required keys with default values if they were not present in 
        # the render options.
        required_keys = {"player_position_text": True, "match_text": True, \
            "match_timer": True, "healthbars": True}
        for key, default_value in required_keys.items():
            if not (key in render_options.keys()):
                render_options[key] = default_value
        
        # Get maximum render index from render indices.
        max_render_index = 0 if len(self.render_indices) == 0 else max([v for v in self.render_indices.values()]) + 1
        
        # Rendering of matches
        num_matches = len([k for k in self.status_dict.keys() if not isinstance(k, str)])
        counter = 1
        match_layout = None
        while match_layout is None:
            if counter * (counter - 1) >= max(max_render_index, num_matches):
                match_layout = (counter, counter - 1)
            elif counter * counter >= max(max_render_index, num_matches):
                match_layout = (counter, counter)
            counter += 1
        
        render_width = min(window_dimensions[0] * 0.85, window_dimensions[1] * 0.85)
        render_offset = [(window_dimensions[0] - render_width) / 2, 100]
        
        for key, status in self.status_dict.items():
            if key == "running" or key == "ticks_per_second":
                continue
            
            # Get render index from render indices dict.
            render_index = self.render_indices[key]
            
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
            
            for player_id, player_data in status.items():
                if not isinstance(player_id, int):
                    continue
                
                # Calculate screen position.
                map_position = player_data["pos"]
                map_position_flipped = [(map_position[0] + 1) / 2, (-map_position[1] + 1) / 2]
                screen_x = window_x + map_position_flipped[0] * window_w
                screen_y = window_y + map_position_flipped[1] * window_h
                
                # Render player.
                pygame.draw.circle(display, self.players[player_id].get_color(), (screen_x, screen_y), window_w / 2 * self.player_size / 2, width=2)
                
                # Render healthbar.
                if render_options["healthbars"]:
                    healthbar_green_width = (player_data["hp"] / 100) * 50
                    healthbar_start = screen_x - 25
                    healthbar_start_mid = screen_x - 25 + healthbar_green_width
                    pygame.draw.rect(display, (10, 150, 10), (healthbar_start, screen_y - 25, healthbar_green_width, 10))
                    pygame.draw.rect(display, (150, 10, 10), (healthbar_start_mid, screen_y - 25, 50 - healthbar_green_width, 10))
                
                # Render rays.
                start_angle = player_data["rot"] - ((player_data["num_rays"] - 1) / 2) * player_data["ray_sep_angle"]
                ray_angles = [start_angle + i * player_data["ray_sep_angle"] for i in range(player_data["num_rays"])]
                ray_intersect_distances = player_data["metadata"]["intersect_distances"]
                for a, r in zip(ray_angles, ray_intersect_distances):
                    line_start_x = screen_x
                    line_start_y = screen_y
                    line_end_x = line_start_x + math.cos(a) * r * (window_w / 2)
                    line_end_y = line_start_y - math.sin(a) * r * (window_w / 2)
                    
                    pygame.draw.line(display, self.players[player_id].get_color(), (line_start_x, line_start_y), (line_end_x, line_end_y))
                
                # Render laser if the weapon has been activated.
                laser_length = ray_intersect_distances[(len(ray_intersect_distances) - 1) // 2]
                fadetime = 0.25
                if time.time() - player_data["last_weapon_activation"] <= fadetime:
                    opacity = max(time.time() - player_data["last_weapon_activation"], 0.0) / fadetime
                    opacity = min(opacity, 1.0)
                    pygame.draw.line(display, (0, int(255 * opacity), 0), (screen_x, screen_y), (screen_x + math.cos(player_data["rot"]) * laser_length * window_w / 2, screen_y - math.sin(player_data["rot"]) * laser_length * window_w / 2), width=5)
                
                # Render position text.
                if render_options["player_position_text"]:
                    render_text_center(display, f"id:{player_id} {map_position[0]:.2f}, {map_position[1]:.2f}", (screen_x, screen_y - 30), font)
            
            # Render match number and participants.
            if render_options["match_text"]:
                player_ids = [k for k in status.keys() if isinstance(k, int)]
                render_match_text = True
                if window_w > 350:
                    current_font = pygame.font.SysFont("Courier New", 16)
                elif window_w > 250:
                    current_font = pygame.font.SysFont("Courier New", 14)
                elif window_w > 200:
                    current_font = pygame.font.SysFont("Courier New", 12)
                elif window_w > 160:
                    current_font = pygame.font.SysFont("Courier New", 8)
                else:
                    render_match_text = False
                if render_match_text:
                    render_text(display, f"Match {key}: {self.players[player_ids[0]].get_name()} vs {self.players[player_ids[1]].get_name()}", (window_x + 5, window_y + 5), current_font)
            
            # Render timer on the right of the match window.
            if render_options["match_timer"]:
                timer_width  = int(window_w * 0.03)
                timer_height = int(window_h * (1 - status["timer_percent"]))
                timer_x = window_x + window_w - timer_width
                timer_y = window_y + window_h - timer_height
                pygame.draw.rect(display, (100, 100, 255), (timer_x, timer_y, timer_width, timer_height))
    
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
    
    def update(self, update_options={}):
        ## Fix up update options if necessary.
        # Replace invalid values with False.
        for k, v in update_options.items():
            if not isinstance(v, bool):
                update_options[k] = False
        
        # Add required keys with default values if they were not present in 
        # the update options.
        required_keys = {"auto_queue_idle_players": False}
        for key, default_value in required_keys.items():
            if not (key in update_options.keys()):
                update_options[key] = default_value
        
        ## Handling of queue, creating new matches, and updating of ranking system
        # Check if any two players are no more than 100 ranking points apart.
        match_created = True
        while len(self.queue) > 1 and match_created:
            match_created = False
            for p1 in self.queue:
                for p2 in self.queue:
                    if p1 == p2:
                        continue
                    
                    p1_ranking = self.leaderboard[p1]
                    p2_ranking = self.leaderboard[p2]
                    if abs(p1_ranking - p2_ranking) <= 100:
                        # Create environment and add to matches dict.
                        env = Environment(player_size=self.player_size, ticks_per_second=self.ticks_per_second)
                        env.add_player(copy.deepcopy(self.players[p1]))
                        env.add_player(copy.deepcopy(self.players[p2]))
                        self.matches[self.match_number] = env
                        
                        # Add render index.
                        # Sort render indices.
                        render_indices = dict(sorted(self.render_indices.items(), key=lambda x: x[1]))
                        # Check if the zeroth index is free.
                        if not (0 in render_indices.values()):
                            self.render_indices[self.match_number] = 0
                        # Check all subsequent indices.
                        else:
                            for match_index, render_index in render_indices.items():
                                # Check if the next render index is present.
                                if not (render_index + 1 in render_indices.values()):
                                    self.render_indices[self.match_number] = render_index + 1
                                    break
                        
                        # Increment match number.
                        self.match_number += 1
                        
                        # Remove players from queue.
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
        
        # Update ranking system if any match has finished.
        matches_to_remove = []
        for index, match in self.matches.items():
            if match.is_finished():
                # Check if the outcome has already been processed.
                if match.outcome_processed:
                    print("[BUG] This is a rare bug where the status dict " \
                        "entry gets removed, but the match entry doesn't. " \
                        "The match is already finished and the outcome has " \
                        "been handled. Attempting to remove the match entry again...")
                    matches_to_remove.append(index)
                    continue
                
                # Get ids of all players in the match.
                player_ids = [player.id for player in match.players]
                
                if not (index in self.status_dict.keys()):
                    print(f"Unfortunately, {index} is in matches, but not in status dict (finished: {match.finished}, outcome processed: {match.outcome_processed}).")
                    self.its_happening.append(index)
                    self.its_happening = list(set(self.its_happening))
                    continue
                
                if self.status_dict[index]["outcome"] == "tie":
                    print(f"Match {index} between players {tuple(player_ids)} " \
                        f"ended in '{self.status_dict[index]['outcome']}'.")
                    # Do nothing as it's a tie.
                elif self.status_dict[index]["outcome"] == "no tie":
                    winner_id = self.status_dict[index]["winner_id"]
                    loser_id  = self.status_dict[index]["loser_id"]
                    
                    print(f"Match {index} between players {tuple(player_ids)} " \
                        f"ended in '{self.status_dict[index]['outcome']}' " \
                        f"({winner_id} won).")
                    
                    # Give points to winner (winner id is first and is thus a).
                    points = calculate_points_for_a(self.leaderboard[winner_id], \
                        self.leaderboard[loser_id], POINT_DIFF_90, a_win=True) * 10
                    self.leaderboard[winner_id] += points
                    self.leaderboard[loser_id]  -= points
                
                # Set outcome processed to true for the random occasional bug where the status dict gets removed, but the match doesn't.
                self.matches[index].outcome_processed = True
                print(f"outcome processed for number {index}", self.matches[index].outcome_processed)
                
                # Queue match to be removed.
                matches_to_remove.append(index)
                
                print(f"Finished match number {index}.")
        
        # Remove finished matches.
        for index in matches_to_remove:
            # Update player distribution.
            self.player_distribution["in_game"] -= len(self.matches[index].players)
            self.player_distribution["idle"] += len(self.matches[index].players)
            
            # Remove match.
            if index in self.matches.keys():
                del self.matches[index]
            if not (index in self.matches.keys()):
                print(f"Removed match number {index}.")
            
            if index in self.status_dict.keys():
                del self.status_dict[index]
            if not (index in self.status_dict.keys()):
                print(f"Removed status dict number {index}.")
            
            if index in self.render_indices.keys():
                del self.render_indices[index]
            if not (index in self.render_indices.keys()):
                print(f"Removed render index number {index}.")
        
        # Auto-queue idle players if this setting is enabled.
        if update_options["auto_queue_idle_players"]:
            # Get list of all player ids.
            all_players = list(self.players.keys())
            
            # Get list of players who are in queue.
            in_queue = self.queue
            
            # Get list of players who are in game.
            in_game = []
            for match in self.matches.values():
                in_game.extend([player.id for player in match.players])
            
            # Queue players who are not in queue nor in game.
            for player_id in all_players:
                if player_id in in_queue:
                    continue
                if player_id in in_game:
                    continue
                self.add_player_to_queue(player_id)
    
    def add_player(self, player):
        if not isinstance(player, Player):
            print(f"Player must be an instance of Player, not '{type(player)}'.")
            return
        
        # Add player to ranking system
        self.players[player.id]     = player
        self.leaderboard[player.id] = START_RATING
        
        # Update player distribution.
        self.player_distribution["total"] += 1
        self.player_distribution["idle"] += 1
    
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
        self.manager.shutdown()
        self.manager.join()

def handle_matches(matches_dict, status_dict):
    clock = pygame.time.Clock()
    
    while True:
        for index, match in matches_dict.items():
            # Run environment step.
            result = match.step()
            
            # Update static dict.
            if not (result is None):
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

def calculate_points_for_a(a, b, p90, a_win):
    """
    Function calculating the number of points to player a if player a wins 
    and is stronger/weaker, and if player a loses and is stronger/weaker.
    Example 1:
        If player a has 100 points more than player b, player a is expected 
        to win 90% of the time. If player a loses, 0.9 points are transfered 
        to player b, if player a wins, 0.1 points are transfered to player a.
    Example 2:
        If player a has 200 points less than player b, player a is expected 
        to lose 99% of the time. If player a loses, 0.01 points are 
        transfered to player b, if player a wins, 0.99 points are transfered 
        to player a.
    """
    # Calculate absolute difference.
    diff = abs(a - b)
    
    # Calculate points to transfer for a win when the player is stronger and 
    # a win when the player is weaker.
    strong_win_p = 1 / (10 ** (diff / p90))
    weak_win_p = 1 - strong_win_p
    
    # When diff is close to 0, strong_win_p equals 1, but weak_win_p 
    # equals 0. This prevents players from climbing past opponents with 
    # similar rating. This solution awards an equal amount of points on a win 
    # to both players, solving the issue.
    if diff < 5:
        strong_win_p = 0.5
        weak_win_p = 0.5
    
    # Transfer points to/from player a depending on if player a won and if 
    # player a was stronger or weaker than player b.
    if a > b:
        if a_win:
            # Strong win
            return strong_win_p
        else:
            # Strong lose
            return -weak_win_p
    else:
        if a_win:
            # Weak win
            return weak_win_p
        else:
            # Weak lose
            return -strong_win_p
