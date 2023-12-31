import logging
import random as rnd
import sys
import time

import pygame

from environment import Environment
from matchmaking import MatchMaking
from player import Player
from simple_player_rotate_shoot import SimplePlayerRotateShoot

TICKS_PER_SECOND = 20

class FPSCounter:
    
    def __init__(self):
        self.last_update = 0
        self.fps_counter = 0
        self.global_fps  = 0
    
    def tick(self):
        self.fps_counter += 1
        if self.last_update == 0:
            self.last_update = time.time()
            return
        
        current_time = time.time()
        delta_time = current_time - self.last_update
        if delta_time >= 1.0:
            self.global_fps = self.fps_counter
            self.fps_counter = 0
            self.last_update = current_time
    
    def get_fps(self):
        return self.global_fps


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

def render_text_right(display, text, position, font, color=(255, 255, 255)):
    # Create text surface.
    text_surface = font.render(text, False, color)
    
    # Update position to render text right.
    position_x = position[0] - text_surface.get_width()
    position_y = position[1]
    
    # Render text.
    display.blit(text_surface, (position_x, position_y))

def main():
    # Initialize logger for file output.
    #fmt_str = "%(asctime)s [%(levelname)-8.8s] %(message)s"
    fmt_str = "%(asctime)s %(filename)s:line %(lineno)-5.5s %(levelname)s %(message)s"
    datefmt_str = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=logging.DEBUG, format=fmt_str, datefmt=datefmt_str, filename="log.txt", filemode="w")
    
    # Add handler for stdout output.
    consolehandler = logging.StreamHandler(sys.stdout)
    consoleformatter = logging.Formatter(fmt="%(levelname)s %(message)s")
    consolehandler.setFormatter(consoleformatter)
    consolehandler.setLevel(logging.WARNING)
    
    logger = logging.getLogger()
    logger.addHandler(consolehandler)
    
    mm = MatchMaking(ticks_per_second=TICKS_PER_SECOND)
    
    for _ in range(25):
        mm.add_player(Player())
        mm.add_player(SimplePlayerRotateShoot())
    
    num_players = len(mm.players)
    
    logging.debug("Matchmaking created.")
    
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Courier New", 16)
    
    # Create window.
    window_dimensions = (1920, 1080)
    display = pygame.display.set_mode(window_dimensions, pygame.RESIZABLE | pygame.DOUBLEBUF)
    
    logging.debug("Pygame window created.")
    
    # Start render loop.
    update_options = {"auto_queue_idle_players": False}
    render_options = {"player_position_text": False, "match_text": False, "match_timer": True, "healthbars": True}
    fps = 60
    clock = pygame.time.Clock()
    fpscounter = FPSCounter()
    running = True
    logging.debug("Starting render loop.")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Adjust update options.
                if event.key == pygame.K_q:
                    update_options["auto_queue_idle_players"] = not update_options["auto_queue_idle_players"]
                    current_setting = "on" if update_options["auto_queue_idle_players"] else "off"
                    logging.debug(f"Switched auto-queue idle players to {current_setting}.")
                
                # Adjust render options.
                if event.key == pygame.K_p:
                    render_options["player_position_text"] = not render_options["player_position_text"]
                if event.key == pygame.K_m:
                    render_options["match_text"] = not render_options["match_text"]
                if event.key == pygame.K_t:
                    render_options["match_timer"] = not render_options["match_timer"]
                if event.key == pygame.K_h:
                    render_options["healthbars"] = not render_options["healthbars"]
                
                if event.key == pygame.K_SPACE:
                    player_ids = list(range(num_players))
                    rnd.shuffle(player_ids)
                    for i in player_ids:
                        mm.add_player_to_queue(i)
                
                if event.key == pygame.K_0:
                    print("Adding player 0 to queue")
                    mm.add_player_to_queue(0)
                if event.key == pygame.K_1:
                    print("Adding player 1 to queue")
                    mm.add_player_to_queue(1)
                if event.key == pygame.K_2:
                    print("Adding player 2 to queue")
                    mm.add_player_to_queue(2)
                if event.key == pygame.K_3:
                    print("Adding player 3 to queue")
                    mm.add_player_to_queue(3)
                if event.key == pygame.K_4:
                    print("Adding player 4 to queue")
                    mm.add_player_to_queue(4)
                if event.key == pygame.K_5:
                    print("Adding player 5 to queue")
                    mm.add_player_to_queue(5)
                if event.key == pygame.K_6:
                    print("Adding player 6 to queue")
                    mm.add_player_to_queue(6)
                if event.key == pygame.K_7:
                    print("Adding player 7 to queue")
                    mm.add_player_to_queue(7)
                if event.key == pygame.K_8:
                    print("Adding player 8 to queue")
                    mm.add_player_to_queue(8)
                if event.key == pygame.K_9:
                    print("Adding player 9 to queue")
                    mm.add_player_to_queue(9)
                
                if event.key == pygame.K_DOWN:
                    fps -= 10
                if event.key == pygame.K_UP:
                    fps += 10
            
            if event.type == pygame.VIDEORESIZE:
                window_dimensions = (event.w, event.h)
        
        display.fill((0, 0, 0))
        
        mm.update(update_options=update_options)
        mm.render(display, font, window_dimensions, render_options=render_options)
        
        fpscounter.tick()
        actual_fps = fpscounter.get_fps()
        render_text(display, text=f"fps: {actual_fps} (target: {fps})", position=(10, 10), font=font)
        
        # Render player distribution.
        total_players = mm.player_distribution["total"]
        in_queue = mm.player_distribution["in_queue"]
        in_game = mm.player_distribution["in_game"]
        idle = mm.player_distribution["idle"]
        
        render_text(display, f"Total players: {total_players}", (10, 30), font)
        render_text(display, f"In queue:      {in_queue}", (10, 50), font)
        render_text(display, f"In game:       {in_game}", (10, 70), font)
        render_text(display, f"Idle:          {idle}", (10, 90), font)
        
        # Render leaderboard.
        counter = 0
        render_text(display, "Leaderboard", (10, 120), font)
        leaderboard_sorted = sorted([(k, v) for k, v in mm.leaderboard.items()], key=lambda x: -x[1])
        max_name_length = max([len(v.get_name()) for v in mm.players.values()])
        for player_id, score in leaderboard_sorted:
            player = mm.players[player_id]
            player_name = player.get_name()
            player_name +=  " " * (max_name_length - len(player_name))
            player_score = str(int(score))
            player_score = " " * (5 - len(player_score)) + player_score
            player_type = str(type(player))[:-2].split(".")[1]
            player_color = player.get_color()
            render_text(display, f"    {player_name}: {player_score}  {player_type}", (10, 140 + 20 * counter), font, player_color)
            counter += 1
        
        # Render text "Press space to add all players to the queue".
        render_text_center(display, "Press space to add all players to the queue", (window_dimensions[0] / 2, 15), font)
        
        # Render rendering options to the right of the screen.
        lines_right_of_screen = []
        lines_right_of_screen.append("Render options")
        
        render_player_positions = " True" if render_options["player_position_text"] else "False"
        lines_right_of_screen.append(f"Render player positions (P): {render_player_positions}")
        
        render_match_text = " True" if render_options["match_text"] else "False"
        lines_right_of_screen.append(f"Render match text (M): {render_match_text}")
        
        render_match_timer = " True" if render_options["match_timer"] else "False"
        lines_right_of_screen.append(f"Render match timer (T): {render_match_timer}")
        
        render_healthbars = " True" if render_options["healthbars"] else "False"
        lines_right_of_screen.append(f"Render healthbars (H): {render_healthbars}")
        
        lines_right_of_screen.append("")
        lines_right_of_screen.append("Update options")
        
        auto_queue_idle_players_text = " True" if update_options["auto_queue_idle_players"] else "False"
        lines_right_of_screen.append(f"Auto-queue idle players (Q): {auto_queue_idle_players_text}")
        
        for index, line in enumerate(lines_right_of_screen):
            render_text_right(display, line, (window_dimensions[0] - 10, 10 + 20 * index), font)
        
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()
    mm.quit()
    
    logging.debug("Quit pygame and matchmaking.")

if __name__ == "__main__":
    main()
