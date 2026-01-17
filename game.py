import pygame  # Import pygame library for game development
import sys  # Import sys for system-specific parameters and functions (like exit)

# Initialize pygame modules
pygame.init()

# Set up game window dimensions
WINDOW_WIDTH = 1000  # Width of the game window in pixels
WINDOW_HEIGHT = 600  # Height of the game window in pixels

# Create the game window with specified dimensions
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the game window
pygame.display.set_caption("2 Player Shooting Duel")

# Create a clock object to control game frame rate
clock = pygame.time.Clock()

# Define colors using RGB values (Red, Green, Blue)
WHITE = (255, 255, 255)  # White color
BLACK = (0, 0, 0)  # Black color
RED = (255, 0, 0)  # Red color
BLUE = (0, 0, 255)  # Blue color
GREEN = (0, 255, 0)  # Green color
YELLOW = (255, 255, 0)  # Yellow color
GRAY = (128, 128, 128)  # Gray color

# Player class to represent each player in the game
class Player:
    def __init__(self, x, y, color, controls):
        # Initialize player position
        self.x = x  # X coordinate of player
        self.y = y  # Y coordinate of player
        self.width = 40  # Width of player rectangle
        self.height = 60  # Height of player rectangle
        self.color = color  # Color of the player
        self.speed = 5  # Movement speed in pixels per frame
        self.health = 100  # Starting health points
        self.max_health = 100  # Maximum health points
        self.controls = controls  # Dictionary containing key bindings for this player
        self.bullets = []  # List to store bullets fired by this player
        self.shoot_cooldown = 0  # Cooldown timer to prevent rapid shooting
        
    def move(self, keys):
        # Move player based on pressed keys
        if keys[self.controls['up']]:  # Check if up key is pressed
            self.y -= self.speed  # Move player up by decreasing y coordinate
        if keys[self.controls['down']]:  # Check if down key is pressed
            self.y += self.speed  # Move player down by increasing y coordinate
        if keys[self.controls['left']]:  # Check if left key is pressed
            self.x -= self.speed  # Move player left by decreasing x coordinate
        if keys[self.controls['right']]:  # Check if right key is pressed
            self.x += self.speed  # Move player right by increasing x coordinate
            
        # Keep player within screen boundaries
        if self.x < 0:  # If player goes off left edge
            self.x = 0  # Reset to left edge
        if self.x > WINDOW_WIDTH - self.width:  # If player goes off right edge
            self.x = WINDOW_WIDTH - self.width  # Reset to right edge
        if self.y < 0:  # If player goes off top edge
            self.y = 0  # Reset to top edge
        if self.y > WINDOW_HEIGHT - self.height:  # If player goes off bottom edge
            self.y = WINDOW_HEIGHT - self.height  # Reset to bottom edge
    
    def shoot(self, target_x, target_y):
        # Create a bullet when player shoots
        if self.shoot_cooldown <= 0:  # Check if cooldown has expired
            # Calculate direction from player to target
            dx = target_x - (self.x + self.width // 2)  # Horizontal distance to target
            dy = target_y - (self.y + self.height // 2)  # Vertical distance to target
            
            # Calculate distance to normalize direction vector
            distance = (dx ** 2 + dy ** 2) ** 0.5  # Pythagorean theorem
            
            if distance > 0:  # Prevent division by zero
                # Normalize direction (make it a unit vector)
                dx = dx / distance  # Normalized x direction
                dy = dy / distance  # Normalized y direction
                
                # Create bullet starting from player's center
                bullet = {
                    'x': self.x + self.width // 2,  # Bullet starts at player's center x
                    'y': self.y + self.height // 2,  # Bullet starts at player's center y
                    'dx': dx * 10,  # Bullet horizontal velocity (10 pixels per frame)
                    'dy': dy * 10,  # Bullet vertical velocity (10 pixels per frame)
                    'owner': self  # Reference to player who shot this bullet
                }
                self.bullets.append(bullet)  # Add bullet to player's bullet list
                self.shoot_cooldown = 20  # Set cooldown to 20 frames (prevents spam)
    
    def update(self):
        # Update player state each frame
        if self.shoot_cooldown > 0:  # If cooldown is active
            self.shoot_cooldown -= 1  # Decrease cooldown by 1 each frame
        
        # Update all bullets
        for bullet in self.bullets[:]:  # Iterate over copy of list (allows safe removal)
            bullet['x'] += bullet['dx']  # Move bullet horizontally
            bullet['y'] += bullet['dy']  # Move bullet vertically
            
            # Remove bullet if it goes off screen
            if (bullet['x'] < 0 or bullet['x'] > WINDOW_WIDTH or 
                bullet['y'] < 0 or bullet['y'] > WINDOW_HEIGHT):
                self.bullets.remove(bullet)  # Remove bullet from list
    
    def draw(self, screen):
        # Draw player on screen
        # Draw player body as a rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw player's gun (small rectangle extending from player)
        gun_length = 30  # Length of gun visual
        gun_x = self.x + self.width // 2  # Gun starts at player center x
        gun_y = self.y + self.height // 2  # Gun starts at player center y
        # Draw gun as a small rectangle
        pygame.draw.rect(screen, BLACK, (gun_x - 2, gun_y - 15, 4, gun_length))
        
        # Draw health bar above player
        bar_width = self.width  # Health bar width matches player width
        bar_height = 5  # Health bar height
        bar_x = self.x  # Health bar x position
        bar_y = self.y - 10  # Health bar y position (above player)
        
        # Draw background of health bar (gray)
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Draw current health (colored portion)
        health_width = int(bar_width * (self.health / self.max_health))  # Calculate width based on health percentage
        health_color = GREEN if self.health > 50 else YELLOW if self.health > 25 else RED  # Color based on health level
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Draw all bullets
        for bullet in self.bullets:  # Iterate through all bullets
            pygame.draw.circle(screen, BLACK, (int(bullet['x']), int(bullet['y'])), 5)  # Draw bullet as black circle

def check_collision(bullet, player):
    # Check if a bullet collides with a player
    bullet_x = bullet['x']  # Get bullet x position
    bullet_y = bullet['y']  # Get bullet y position
    bullet_radius = 5  # Bullet collision radius
    
    # Check if bullet is within player's rectangle bounds
    if (bullet_x >= player.x - bullet_radius and  # Bullet left edge touches player
        bullet_x <= player.x + player.width + bullet_radius and  # Bullet right edge touches player
        bullet_y >= player.y - bullet_radius and  # Bullet top edge touches player
        bullet_y <= player.y + player.height + bullet_radius):  # Bullet bottom edge touches player
        return True  # Collision detected
    return False  # No collision

def main():
    # Main game function
    # Create player 1 (left side, red color)
    player1 = Player(
        x=100,  # Starting x position (left side of screen)
        y=WINDOW_HEIGHT // 2 - 30,  # Starting y position (center vertically)
        color=RED,  # Red color for player 1
        controls={  # Control keys for player 1
            'up': pygame.K_w,  # W key to move up
            'down': pygame.K_s,  # S key to move down
            'left': pygame.K_a,  # A key to move left
            'right': pygame.K_d,  # D key to move right
            'shoot': pygame.K_SPACE  # Space key to shoot
        }
    )
    
    # Create player 2 (right side, blue color)
    player2 = Player(
        x=WINDOW_WIDTH - 140,  # Starting x position (right side of screen)
        y=WINDOW_HEIGHT // 2 - 30,  # Starting y position (center vertically)
        color=BLUE,  # Blue color for player 2
        controls={  # Control keys for player 2
            'up': pygame.K_UP,  # Up arrow key to move up
            'down': pygame.K_DOWN,  # Down arrow key to move down
            'left': pygame.K_LEFT,  # Left arrow key to move left
            'right': pygame.K_RIGHT,  # Right arrow key to move right
            'shoot': pygame.K_RETURN  # Enter key to shoot
        }
    )
    
    # Game loop flag
    running = True  # Set to False to exit game
    
    # Main game loop
    while running:
        # Handle events (keyboard, mouse, window close, etc.)
        for event in pygame.event.get():  # Get all events from event queue
            if event.type == pygame.QUIT:  # If user clicks window close button
                running = False  # Exit game loop
                pygame.quit()  # Uninitialize pygame
                sys.exit()  # Exit program
        
        # Get current state of all keyboard keys
        keys = pygame.key.get_pressed()  # Returns dictionary of all key states
        
        # Update player 1
        player1.move(keys)  # Move player 1 based on key presses
        if keys[player1.controls['shoot']]:  # If player 1's shoot key is pressed
            # Calculate target position (center of player 2)
            target_x = player2.x + player2.width // 2  # Target x is player 2's center
            target_y = player2.y + player2.height // 2  # Target y is player 2's center
            player1.shoot(target_x, target_y)  # Shoot towards player 2
        player1.update()  # Update player 1's state (bullets, cooldown, etc.)
        
        # Update player 2
        player2.move(keys)  # Move player 2 based on key presses
        if keys[player2.controls['shoot']]:  # If player 2's shoot key is pressed
            # Calculate target position (center of player 1)
            target_x = player1.x + player1.width // 2  # Target x is player 1's center
            target_y = player1.y + player1.height // 2  # Target y is player 1's center
            player2.shoot(target_x, target_y)  # Shoot towards player 1
        player2.update()  # Update player 2's state (bullets, cooldown, etc.)
        
        # Check collisions between player 1's bullets and player 2
        for bullet in player1.bullets[:]:  # Iterate over copy of bullet list
            if check_collision(bullet, player2):  # Check if bullet hits player 2
                player2.health -= 10  # Reduce player 2's health by 10
                player1.bullets.remove(bullet)  # Remove bullet after hit
                if player2.health <= 0:  # If player 2's health reaches 0
                    player2.health = 0  # Set health to 0 (prevent negative)
        
        # Check collisions between player 2's bullets and player 1
        for bullet in player2.bullets[:]:  # Iterate over copy of bullet list
            if check_collision(bullet, player1):  # Check if bullet hits player 1
                player1.health -= 10  # Reduce player 1's health by 10
                player2.bullets.remove(bullet)  # Remove bullet after hit
                if player1.health <= 0:  # If player 1's health reaches 0
                    player1.health = 0  # Set health to 0 (prevent negative)
        
        # Clear screen with white background
        screen.fill(WHITE)  # Fill entire screen with white color
        
        # Draw both players
        player1.draw(screen)  # Draw player 1 and their bullets
        player2.draw(screen)  # Draw player 2 and their bullets
        
        # Display game over message if a player dies
        font = pygame.font.Font(None, 72)  # Create font object (size 72)
        if player1.health <= 0:  # If player 1 is dead
            text = font.render("Player 2 Wins!", True, BLUE)  # Create blue text
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))  # Center text
            screen.blit(text, text_rect)  # Draw text on screen
        elif player2.health <= 0:  # If player 2 is dead
            text = font.render("Player 1 Wins!", True, RED)  # Create red text
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))  # Center text
            screen.blit(text, text_rect)  # Draw text on screen
        
        # Display health values
        health_font = pygame.font.Font(None, 36)  # Create smaller font for health display
        p1_health_text = health_font.render(f"P1 Health: {player1.health}", True, RED)  # Player 1 health text
        p2_health_text = health_font.render(f"P2 Health: {player2.health}", True, BLUE)  # Player 2 health text
        screen.blit(p1_health_text, (10, 10))  # Draw player 1 health in top left
        screen.blit(p2_health_text, (WINDOW_WIDTH - 200, 10))  # Draw player 2 health in top right
        
        # Display controls
        controls_font = pygame.font.Font(None, 24)  # Create font for controls
        p1_controls = controls_font.render("P1: WASD + SPACE", True, BLACK)  # Player 1 controls text
        p2_controls = controls_font.render("P2: ARROWS + ENTER", True, BLACK)  # Player 2 controls text
        screen.blit(p1_controls, (10, WINDOW_HEIGHT - 30))  # Draw at bottom left
        screen.blit(p2_controls, (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30))  # Draw at bottom right
        
        # Update display (show everything we drew)
        pygame.display.flip()  # Update entire screen
        
        # Control game speed (60 frames per second)
        clock.tick(60)  # Wait to maintain 60 FPS

# Run the game if this file is executed directly
if __name__ == "__main__":  # Check if script is run directly (not imported)
    main()  # Call main function to start game

