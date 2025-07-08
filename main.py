import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WHITE
from player import Player
from level import Level

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Run and Jump Adventure')
    clock = pygame.time.Clock()

    player = Player(120, 440)
    level = Level()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update(level.platforms)

        screen.fill(WHITE)
        level.draw(screen)
        player.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main() 