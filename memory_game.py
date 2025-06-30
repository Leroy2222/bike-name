import pygame
import random
import sys
import time
from pygame import mixer

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CARD_SIZE = 100
CARD_PADDING = 20
GRID_ROWS = 4
GRID_COLS = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Load sounds
MATCH_SOUND = mixer.Sound('sounds/match.wav')
NO_MATCH_SOUND = mixer.Sound('sounds/no_match.wav')
ELEVATOR_SOUND = mixer.Sound('sounds/elevator.wav')

# Hotel-themed card images
CARD_IMAGES = [
    pygame.image.load('images/lobby.png'),
    pygame.image.load('images/elevator.png'),
    pygame.image.load('images/stairwell.png'),
    pygame.image.load('images/security.png'),
    pygame.image.load('images/30th_floor.png'),
    pygame.image.load('images/roof.png'),
    pygame.image.load('images/garage.png'),
    pygame.image.load('images/helicopter.png')
]

# Create a list of cards (doubled for pairs)
ALL_CARDS = CARD_IMAGES * 2
random.shuffle(ALL_CARDS)

# Game state
class Card:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
        self.revealed = False
        self.matched = False
        self.flipping = False
        self.flip_start_time = 0

cards = []
selected_cards = []
matched_cards = set()
start_time = time.time()

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Die Hard Hotel Memory Game")
font = pygame.font.Font(None, 36)

# Calculate grid positions
def create_cards():
    positions = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (CARD_SIZE + CARD_PADDING) + CARD_PADDING
            y = row * (CARD_SIZE + CARD_PADDING) + CARD_PADDING
            positions.append((x, y))
    
    # Create card objects
    for i, pos in enumerate(positions):
        cards.append(Card(ALL_CARDS[i], pos[0], pos[1]))

def draw_card(card):
    # Draw back of card
    if not card.revealed and not card.matched:
        pygame.draw.rect(screen, BLUE, card.rect)
        pygame.draw.rect(screen, BLACK, card.rect, 2)
        
    # Draw front of card
    if card.revealed or card.matched:
        screen.blit(card.image, card.rect.topleft)
        pygame.draw.rect(screen, BLACK, card.rect, 2)

def flip_card(card):
    card.revealed = True
    card.flipping = True
    card.flip_start_time = pygame.time.get_ticks()

def check_match():
    if len(selected_cards) == 2:
        card1 = cards[selected_cards[0]]
        card2 = cards[selected_cards[1]]
        
        if card1.image == card2.image:
            card1.matched = True
            card2.matched = True
            matched_cards.update(selected_cards)
            MATCH_SOUND.play()
            return True
        else:
            NO_MATCH_SOUND.play()
            pygame.time.wait(1000)  # Wait a second before hiding
            card1.revealed = False
            card2.revealed = False
            selected_cards.clear()
            return False
    return None

def draw_timer():
    elapsed_time = int(time.time() - start_time)
    timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
    screen.blit(timer_text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 40))

def draw_score():
    score_text = font.render(f"Matches: {len(matched_cards)//2}", True, BLACK)
    screen.blit(score_text, (10, WINDOW_HEIGHT - 40))

def draw_animation():
    for card in cards:
        if card.flipping:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - card.flip_start_time
            
            # Simple flip animation
            if elapsed < 200:
                angle = (elapsed / 200) * 180
                rotated_image = pygame.transform.rotate(card.image, angle)
                rotated_rect = rotated_image.get_rect(center=card.rect.center)
                screen.blit(rotated_image, rotated_rect.topleft)
            else:
                card.flipping = False

def main():
    clock = pygame.time.Clock()
    running = True
    create_cards()
    
    # Play background music
    mixer.music.load('sounds/background_music.mp3')
    mixer.music.play(-1)  # Loop forever
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(selected_cards) < 2:  # Only allow 2 cards to be selected at a time
                    mouse_pos = pygame.mouse.get_pos()
                    for i, card in enumerate(cards):
                        if card.rect.collidepoint(mouse_pos):
                            if not card.matched and not card.revealed:
                                selected_cards.append(i)
                                flip_card(card)
                                match_result = check_match()
                                if match_result is not None:
                                    if match_result:
                                        print("Match!")
                                    else:
                                        print("No match!")
                                        selected_cards.clear()
                                break
        
        # Fill the screen
        screen.fill(WHITE)
        
        # Draw all cards
        for card in cards:
            draw_card(card)
        
        # Draw animations
        draw_animation()
        
        # Draw timer and score
        draw_timer()
        draw_score()
        
        # Check for game completion
        if len(matched_cards) == len(cards):
            game_over_text = font.render("Congratulations! You found all pairs!", True, GREEN)
            screen.blit(game_over_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))
            
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
