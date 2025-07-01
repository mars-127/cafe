import pygame
import random
import sys
import os
import asyncio
import platform
from pygame.locals import *
from PIL import Image

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cafe Order Rush")
logo = pygame.image.load(r"/workspaces/cafe/images/logo.png")
pygame.display.set_icon(logo)
clock = pygame.time.Clock()

# Load images (placeholder code - in a real game you'd have actual image files)
def create_placeholder_surface(color, width, height):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    return surf

# Load pixel font
pygame.font.init()
font_path = r"/workspaces/cafe/images/Grand9K Pixel.ttf"
font_small = pygame.font.Font(font_path, 12)
font = pygame.font.Font(font_path, 24)
font_large = pygame.font.Font(font_path, 36)


# Create placeholder images
background_img = pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/background.jpg").convert(), (640,480))
customer_neutral_img = pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/OK.png").convert_alpha(), (190,250))
customer_happy_img = pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/HAPPY.png").convert_alpha(), (190,250))
customer_sad_img = pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/SAD.png").convert_alpha(), (190, 250))
cup_img = pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/cup.png").convert_alpha(), (120, 150))
order_card_img = pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/static.png").convert_alpha(), (245,115))
banner_img = pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/banner.png").convert_alpha(), (620, 100))
# Ingredient images (just colored squares with letters)
ingredient_images = {
    'I': pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/ice.png").convert_alpha(), (50,50)),  # Ice
    'S': pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/sugar.png").convert_alpha(), (50,50)),  # Sugar
    'W': pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/water.png").convert_alpha(), (50,50)),    # Water
    'C': pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/coffee.png").convert_alpha(), (50,50)),   # Coffee
    'T': pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/tea.png").convert_alpha(), (50,50)),   # Tea
    'V': pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/vanilla.png").convert_alpha(), (50,50)),    # Vanilla
    'M': pygame.transform.scale(pygame.image.load(r"/workspaces/cafe/images/milk.png").convert_alpha(), (50,50))    # Milk
}

# Add letters to ingredient images


# Game variables
score = 0
time_left = 60  # 60 seconds
current_order = ""
order_complete = False
orders_completed = 0
orders = []
current_customer_state = 0  # 0=neutral, 1=happy, 2=sad
customer_timer = 0

# Possible ingredients and their keys
ingredients = {
    'I': "Ice",
    'S': "Sugar",
    'W': "Water",
    'C': "Coffee",
    'T': "Tea",
    'V': "Vanilla",
    'M': "Milk"
}


def generate_order():
    """Generate a random order with at least milk or water"""
    base_options = ['C', 'T', 'V']  # Coffee, Tea, Vanilla
    extras = ['I', 'S']  # Ice, Sugar
    required = ['M', 'W']  # Must have at least one of these
    
    # Start with 1-2 base ingredients
    order = random.sample(base_options, random.randint(1, 2))
    
    # Add 0-2 extras
    order.extend(random.sample(extras, random.randint(0, 2)))
    
    # Ensure we have at least milk or water
    if not any(item in order for item in required):
        order.append(random.choice(required))
    
    # Randomize order
    random.shuffle(order)
    return ''.join(order)

def draw_ingredient_banner():
    """Draw the ingredient keys in a banner at the bottom of the screen"""
    # Draw the banner
    screen.blit(banner_img, (10, SCREEN_HEIGHT - 100))
    
    # Draw the ingredient keys on the banner
    y_pos = SCREEN_HEIGHT - 70
    for i, (key, name) in enumerate(ingredients.items()):
        x_pos = 50 + i * 75
        screen.blit(ingredient_images[key], (x_pos, y_pos-8))
        text = font_small.render(f"{key}: {name}", True, BLACK)
        screen.blit(text, (x_pos + 10, y_pos + 40))

def draw_current_order():
    """Draw the current order being prepared"""
    if current_order:
        # Draw the cup
        screen.blit(cup_img, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25))
        
        # Draw ingredients in the cup
        for i, char in enumerate(current_order):
            screen.blit(ingredient_images[char], 
                       (SCREEN_WIDTH // 2 - 80 + i * 50, SCREEN_HEIGHT // 2 - 100))
        
        # Draw "Current Order" text
        text = font.render("Current Order", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT// 2  + 115))

def draw_order_queue():
    """Draw the queue of orders"""
    for i, order in enumerate(orders):
        # Draw order card
        card_x = 15
        card_y = 15 + i * 120
        screen.blit(order_card_img, (card_x, card_y))
        
        # Draw order number
        text = font.render(f"Order #{i+1}", True, BLACK)
        screen.blit(text, (card_x + 50, card_y + 10))
        
        # Draw ingredients
        for j, char in enumerate(order):
            screen.blit(ingredient_images[char], (card_x + 10 + j * 45, card_y + 40))

def draw_customer():
    """Draw the customer with appropriate expression"""
    customer_x = SCREEN_WIDTH // 2 + 125
    customer_y = SCREEN_HEIGHT // 2 - 75
    
    if current_customer_state == 0:  # Neutral
        screen.blit(customer_neutral_img, (customer_x, customer_y))
    elif current_customer_state == 1:  # Happy
        screen.blit(customer_happy_img, (customer_x, customer_y))
    else:  # Sad
        screen.blit(customer_sad_img, (customer_x, customer_y))

def draw_hud():
    """Draw the heads-up display (score and time)"""
    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 200, 20))
    
    # Draw time
    time_text = font.render(f"Time: {int(time_left)}s", True, BLACK)
    screen.blit(time_text, (SCREEN_WIDTH - 200, 60))
    
    # Draw orders completed
    orders_text = font.render(f"Orders: {orders_completed}", True, BLACK)
    screen.blit(orders_text, (SCREEN_WIDTH - 200, 100))

def check_order_match():
    """Check if the current order matches the first order in queue"""
    global current_order, score, orders_completed, current_customer_state, customer_timer
    
    if orders and current_order == orders[0]:
        # Correct order
        score += 100
        orders_completed += 1
        orders.pop(0)
        current_order = ""
        current_customer_state = 1  # Happy
        customer_timer = 60  # 1 second display (at 60 FPS)
        
        # Generate a new order if queue is getting small
        if len(orders) < 3:
            orders.append(generate_order())
    elif orders and current_order:  # Only penalize if they actually entered something
        # Wrong order
        score = max(0, score - 50)
        current_customer_state = 2  # Sad
        customer_timer = 60  # 1 second display

# Generate initial orders
for _ in range(3):
    orders.append(generate_order())

# Game loop
running = True
last_time = pygame.time.get_ticks()

while running:
    # Keep loop running at the right speed
    clock.tick(FPS)
    
    # Process events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.unicode.upper() in ingredients and not order_complete:
                # Add ingredient to current order
                current_order += event.unicode.upper()
            elif event.key == K_RETURN and current_order:
                # Submit order
                check_order_match()
            elif event.key == K_BACKSPACE and current_order:
                # Remove last ingredient
                current_order = current_order[:-1]
    
    # Update customer expression timer
    if customer_timer > 0:
        customer_timer -= 1
        if customer_timer == 0:
            current_customer_state = 0  # Back to neutral
    
    # Update time
    current_time = pygame.time.get_ticks()
    if current_time - last_time >= 1000:  # 1 second has passed
        time_left -= 1
        last_time = current_time
        
        # Game over when time runs out
        if time_left <= 0:
            running = False
    
    # Draw everything
    screen.blit(background_img, (0, 0))
    draw_order_queue()
    draw_current_order()
    draw_customer()
    draw_ingredient_banner()
    draw_hud()
    
    # Flip the display
    pygame.display.flip()


# Game over screen
screen.fill(BLACK)
game_over_text = font_large.render("Game Over!", True, WHITE)
score_text = font_large.render(f"Final Score: {score}", True, WHITE)
orders_text = font_large.render(f"Orders Completed: {orders_completed}", True, WHITE)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
screen.blit(orders_text, (SCREEN_WIDTH // 2 - orders_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

# Directory to save frames
frame_dir = "frames"
os.makedirs(frame_dir, exist_ok=True)

# Function to capture frames
def capture_frame(frame_count):
    pygame.image.save(screen, os.path.join(frame_dir, f"frame_{frame_count:04d}.png"))

# Game over screen
frame_count = 0
for _ in range(100):  # Capture 100 frames
    screen.fill(BLACK)
    game_over_text = font_large.render("Game Over!", True, WHITE)
    score_text = font_large.render(f"Final Score: {score}", True, WHITE)
    orders_text = font_large.render(f"Orders Completed: {orders_completed}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(orders_text, (SCREEN_WIDTH // 2 - orders_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

# Directory to save frames
frame_dir = "frames"
os.makedirs(frame_dir, exist_ok=True)

# Function to capture frames
def capture_frame(frame_count):
    pygame.image.save(screen, os.path.join(frame_dir, f"frame_{frame_count:04d}.png"))

# Game over screen
game_over_image = pygame.image.load(r"/workspaces/cafe/images/game_over.jpg")  # Replace with your image path
game_over_image = pygame.transform.scale(game_over_image, (640, 500))  # Resize if needed
screen.blit(game_over_image, (SCREEN_WIDTH // 2 - game_over_image.get_width() // 2, SCREEN_HEIGHT // 2 - 250))
game_over_text = font_large.render("Game Over!", True, WHITE)
score_text = font_large.render(f"Final Score: {score}", True, BLACK)
orders_text = font_large.render(f"Orders Completed: {orders_completed}", True, BLACK)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
screen.blit(orders_text, (SCREEN_WIDTH // 2 - orders_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
pygame.display.flip()


# Wait a few seconds before quitting
pygame.time.wait(3000)

pygame.quit()
sys.exit()