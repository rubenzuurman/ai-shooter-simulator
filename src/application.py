import time

import pygame

from environment import Environment
from matchmaking import MatchMaking
from player import Player

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
    """p1 = Player()
    p2 = Player()
    
    env = Environment(ticks=20, num_rays=6, rays_sep=1)
    env.add_player(p1)
    env.add_player(p2)
    
    env.step()
    
    return"""
    
    """from environment import test_function
    
    test_function()
    
    return"""
    
    mm = MatchMaking(ticks_per_second=10, num_rays=1)
    p1 = Player()
    p2 = Player()
    p3 = Player()
    p4 = Player()
    
    mm.add_player(p1)
    mm.add_player(p2)
    mm.add_player(p3)
    mm.add_player(p4)
    
    mm.add_player_to_queue(1)
    mm.add_player_to_queue(2)
    
    
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Courier New", 16)
    
    # Create window.
    window_dimensions = (800, 800)
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
        
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()
    mm.quit()

if __name__ == "__main__":
    main()