import time

import pygame

from environment import Environment
from matchmaking import MatchMaking
from player import Player

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

def main():
    mm = MatchMaking(ticks_per_second=TICKS_PER_SECOND)
    """p1 = Player()
    p2 = Player()
    p3 = Player()
    p4 = Player()
    
    mm.add_player(p1)
    mm.add_player(p2)
    mm.add_player(p3)
    mm.add_player(p4)"""
    
    num_players = len([mm.add_player(Player()) for _ in range(20)])
    
    mm.add_player_to_queue(1)
    mm.add_player_to_queue(2)
    
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Courier New", 16)
    
    # Create window.
    window_dimensions = (1920, 1080)
    display = pygame.display.set_mode(window_dimensions, pygame.RESIZABLE)
    
    # Start render loop.
    fps = 60
    clock = pygame.time.Clock()
    fpscounter = FPSCounter()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_SPACE:
                    print("Space pressed")
                    mm.add_player_to_queue(0)
                    mm.add_player_to_queue(3)
                    
                    for i in range(num_players):
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
                display = pygame.display.set_mode(window_dimensions, pygame.RESIZABLE)
        
        display.fill((0, 0, 0))
        
        mm.update()
        mm.render(display, font, window_dimensions)
        
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
        for player_id, score in leaderboard_sorted:
            player_name = mm.players[player_id].get_name()
            player_color = mm.players[player_id].get_color()
            render_text(display, f"    {player_name}: {score}", (10, 140 + 20 * counter), font, player_color)
            counter += 1
        
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()
    mm.quit()

if __name__ == "__main__":
    main()
