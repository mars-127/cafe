# Cafe Order Rush
Pygame playground- Created a mini-game about getting your keys right!

Cafe Order Rush is a fast-paced, time-based game built with Pygame where players act as baristas fulfilling coffee orders under a 60-second time limit. Match customer orders by selecting ingredients using keyboard inputs, earn points for correct orders, and avoid mistakes to keep customers happy!

In Cafe Order Rush, you run a busy cafe, taking and fulfilling customer orders for coffee drinks. Each order consists of a combination of ingredients (e.g., Coffee, Milk, Ice). You input ingredients using keyboard keys, submit orders, and earn points based on accuracy. The game ends after 60 seconds, displaying your final score, orders completed, and high score on a stylized end screen with a GIF animation and pixel font.
Features

## Features
1. Dynamic Order System: Randomly generated orders with base ingredients (Coffee, Tea, Vanilla), extras (Ice, Sugar), and required ingredients (Milk or Water).
2. Customer Feedback: Visual feedback with customer expressions (neutral, happy, sad) based on order accuracy.
3. Scoring and High Score: Earn +100 points for correct orders, lose -50 for mistakes, with persistent high score storage.
4. Animated End Screen: Displays a "Game Over" screen with a looping GIF, final score, high score, and replay/quit options.
5. Pixel Art Aesthetic: Uses a pixel font (Press Start 2P) and scaled images for a retro feel.
6. Responsive Controls: Keyboard inputs for adding (I, S, W, C, T, V, M), submitting (Enter), and removing (Backspace) ingredients.

## Gameplay
### Objective: Fulfill as many coffee orders as possible within 60 seconds.
1. Controls:
Press I, S, W, C, T, V, or M to add Ice, Sugar, Water, Coffee, Tea, Vanilla, or Milk to your current order.
Press Enter to submit the order.
Press Backspace to remove the last ingredient.
Press Esc to quit during gameplay.
On the end screen, press R to replay or Q to quit.
2. Scoring:
Correct order: +100 points.
Incorrect order: -50 points (minimum score: 0).
High score is saved to high_score.txt.
3. Timer: You have 60 seconds to complete as many orders as possible.
Customer Reactions: Customers show happy (correct order) or sad (incorrect order) expressions, reverting to neutral after 1 second.

## Requirements
Python 3.8+
Pygame (pip install pygame)
A pixel font file (e.g., PressStart2P-Regular.ttf) in the fonts/ directory
Image assets in the images/ directory (background, customer faces, cup, order card, ingredients, GIF frames)

## Setup
Clone the Repository and prepare assets. 

## Conceptuals
- Cordinate Geometry
- Random Integers- game dependent outcomes

### Pygame Framework:
Surface rendering (screen.blit) for images and text.
Event handling for keyboard inputs.
Game loop with fixed FPS (60) using pygame.time.Clock.

### Game Logic:
Random order generation with constraints (e.g., must include Milk or Water).
Order matching and scoring system.
Timer-based gameplay with customer feedback.


## Future Improvements

- Sound Effects: Add audio for order completion, errors, and customer reactions.
- Difficulty Scaling: Increase order complexity or reduce time as the game progresses.
- Sprite Groups: Use pygame.sprite.Group for better rendering performance.
- Settings Menu: Allow players to adjust volume, difficulty, or resolution.
- Score Leaderboard: Store multiple high scores with player names.
- Cross-Platform Support: Fully adapt file I/O for Pyodide using local storage.