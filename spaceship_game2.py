import pygame
import random

# Initialize Pygame
pygame.init()

#music
pygame.mixer.music.load('battle_loop1.mp3')
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=10000)

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
STAR_NUM = random.randint(75, 250)  # Number of stars in the background
LASER_SPEED = 10
LASER_TRAIL_LENGTH = 7 # Length of the laser trail
SHIP_SPEED = 9 # Speed of the spaceship movement
MAGENTA = (255, 0, 255)  # Color for the laser
BLACK = (0, 0, 0,)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
# Gradient colors
START_COLOR = (155, 35, 255)  # Purple-blue
END_COLOR = (140, 69, 0)     # Orange-red

# Font initialization
font = pygame.font.Font(None, 24)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('the E.T. Space Adventure')

# Generate stars
stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(STAR_NUM)]

# Constants for the bars
HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT = 200, 20
EXP_BAR_WIDTH, EXP_BAR_HEIGHT = 200, 20
BAR_PADDING = 10  # Padding between the edge of the screen and the bars

def draw_health_bar(screen, x, y, current_health, max_health):
    # Draw the background of the health bar
    pygame.draw.rect(screen, RED, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT), 2)  # Border
    # Fill the health bar according to the current health
    health_width = int((current_health / max_health) * HEALTH_BAR_WIDTH)
    pygame.draw.rect(screen, RED, (x, y, health_width, HEALTH_BAR_HEIGHT))

def draw_experience_bar(screen, x, y, current_exp, max_exp):
    # Draw the background of the experience bar
    pygame.draw.rect(screen, BLUE, (x, y, EXP_BAR_WIDTH, EXP_BAR_HEIGHT), 2)  # Border
    # Fill the experience bar according to the current experience
    exp_width = int((current_exp / max_exp) * EXP_BAR_WIDTH)
    pygame.draw.rect(screen, BLUE, (x, y, exp_width, EXP_BAR_HEIGHT))

def interpolate_color(start_color, end_color, factor):
    # Ensure that color values are clamped between 0 and 255
    return (
        max(0, min(255, int(start_color[0] + (end_color[0] - start_color[0]) * factor))),
        max(0, min(255, int(start_color[1] + (end_color[1] - start_color[1]) * factor))),
        max(0, min(255, int(start_color[2] + (end_color[2] - start_color[2]) * factor)))
    )

def reset_game():
    global spaceship, enemies, score, level  # Use global if these are defined at the top level
    # Reset spaceship
    spaceship = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    # Reset enemies
    enemies = [Enemy(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(5)]
    # Reset score and level or any other necessary variables
    score = 0
    level = 1


class Enemy:
  def __init__(self, x, y, value=10, base_speed=1):
    self.x = x
    self.y = y
    self.speed = base_speed  # Enemy movement speed
    self.health = 10
    self.value = value
    self.width = 20
    self.height = 20
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

  def update(self):

        # Check if the enemy is hit by the player
        if self.rect.colliderect(player.rect):
            self.kill()

  def update_speed(self, level):
        # Increase speed based on player's level, could be a linear or non-linear increase
        self.speed += level * 0.1  # Example: Increase speed by 10% per level

  def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill() == enemy.remove




  def move_towards_player(self, player):
    # Calculate the difference between enemy and player position
    #OLD DX DXY dx, dy = player.x - self.x + random.randint(-500, 500), player.y - self.y + random.randint(-500, 500)
    dx, dy = player.x - self.x, player.y - self.y
    # Check for zero distance to avoid division by zero in normalization
    if dx == 0 and dy == 0:
        dx, dy = 1, 0  # Arbitrary small movement

    
    # Normalize the direction vector for a smooth chase
    direction = pygame.math.Vector2(dx, dy).normalize()

    # Move the enemy towards the player by its speed
    self.x += direction.x * self.speed
    self.y += direction.y * self.speed
    self.rect.update(self.x, self.y, self.width, self.height)  # Update the rect position

  def draw(self, screen):
    # Draw a red circle for the enemy sprite
    pygame.draw.ellipse(screen, RED, self.rect, 30)


class Laser:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.x, self.y - 10), 2)

# Player's spaceship
class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.health = 100
        self.max_health = 100
        self.experience = 0
        self.max_experience = 100
        self.level = 1
        self.score = 0
        self.missile_charge_start_time = None
        self.last_damage_time = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Initialize the rect

        self.lasers = []
        self.thrust_particles = []

    def update_rect(self):
        # Update the rectangle position
        self.rect.x = self.x
        self.rect.y = self.y

    def calculate_rect(self, points):
        # Create a rect from polygon points by finding the min/max x and y
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def draw(self, screen):
        # Main body of the spaceship
        main_body = [(self.x, self.y - self.height // 2), (self.x - self.width // 2, self.y + self.height // 2), (self.x + self.width // 2, self.y + self.height // 2)]
        pygame.draw.polygon(screen, WHITE, main_body)
        

        # Wings
        left_wing = [(self.x - self.width // 2, self.y + self.height // 2), (self.x - self.width, self.y), (self.x - self.width // 2, self.y +50)]
        right_wing = [(self.x + self.width // 2, self.y + self.height // 2), (self.x + self.width, self.y), (self.x + self.width // 2, self.y +50)]
        pygame.draw.polygon(screen, WHITE, left_wing)
        pygame.draw.polygon(screen, WHITE, right_wing)


        # Cockpit
        cockpit_rect = pygame.Rect(self.x - 5, self.y - self.height // 6, 11, 50)
        pygame.draw.ellipse(screen, BLACK, cockpit_rect)

        # Thrust particles
        new_particles = []
        for particle in self.thrust_particles:
            color_factor = particle[2] / 3.0  # Color changes as the particle shrinks
            color = interpolate_color(START_COLOR, END_COLOR, 1 - color_factor)
            pygame.draw.circle(screen, color, (particle[0], particle[1]), int(particle[2]))
            particle[1] += particle[3]
            particle[2] -= 0.15  # Shrink particle size
            if particle[2] > 0:
                new_particles.append(particle)
        self.thrust_particles = new_particles

        # Lasers
        for laser in self.lasers:
            pygame.draw.line(screen, MAGENTA, (laser[0], laser[1]), (laser[0], laser[1] - 3))

    def move(self, direction):
        if direction == 'left' and self.x - self.width > 0:
            self.x -= SHIP_SPEED
        elif direction == 'right' and self.x + self.width < SCREEN_WIDTH:
            self.x += SHIP_SPEED
        elif direction == 'up' and self.y - self.height > SCREEN_HEIGHT * 0.25:
            self.y -= SHIP_SPEED
        elif direction == 'down' and self.y + self.height < SCREEN_HEIGHT:
            self.y += SHIP_SPEED
        # Add thrust particle
        if direction in ['left', 'right', 'up', 'down']:
            for i in range(5):  # Generate multiple particles
                self.thrust_particles.append([self.x, self.y + self.height // 2, random.uniform(.1, 3.0), random.randint(1, 7)])
        self.update_rect()

    def shoot(self):
        self.lasers.append([self.x, self.y - 20])
        new_laser = Laser(self.x, self.y, LASER_SPEED, MAGENTA)

    def update_lasers(self, enemies):
        for laser in self.lasers[:]:
            start_color = MAGENTA  # Bright white at the front
            end_color = WHITE  # Magenta at the back
            for i in range(LASER_TRAIL_LENGTH):
                color = interpolate_color(start_color, end_color, i / LASER_TRAIL_LENGTH)
                pygame.draw.line(screen, color, (laser[0], laser[1] - i * 10), (laser[0], laser[1] - (i + 1) * 10), 2)
            laser[1] -= LASER_SPEED  # Move laser up
            if laser[1] < -10 * LASER_TRAIL_LENGTH:
                self.lasers.remove(laser)

            for enemy in enemies[:]:  # Another shallow copy for safe modification
                if (laser[0] - enemy.x) ** 2 + (laser[1] - enemy.y) ** 2 < 100:  # Assuming a simple radius for hit detection
                    self.update_score(enemy.value)
                    self.gain_experience(10)
                    enemies.remove(enemy)  # Remove the enemy if hit
                    self.lasers.remove(laser)  # Remove the laser
                    break

    def draw_lasers(self, screen):
        # Draw all the lasers
        for laser in self.lasers:
            laser.draw(screen)



    def take_damage(self, amount, current_time):
        self.health -= amount
        self.last_damage_time = current_time
        #pygame.mixer.Sound.play(damage_sound)  # Assuming you have a sound loaded named damage_sound
        if self.health <= 0:
            self.health = 0
            restart = game_over_screen(screen, self.score, self.level)
            if restart:
                self.reset_game()  # Implement this method to reset the game state
            else:
                return
            print("GAME OVER")
                
    def update(self, current_time):
        if self.invulnerable and (current_time - self.last_damage_time > self.invulnerable_duration):
            self.rect.x = self.x
            self.rect.y = self.y
            self.invulnerable = False
            self.restore_sprite()  # Restore the sprite's original appearance
            

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.max_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_experience *= 2.5  # Increase the experience needed for the next level
        self.max_health += 10  # Increase max health with each level
        self.health = self.max_health  # Restore full health

    def update_score(self, points):
        self.score += points

    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= (100 + (self.level * 10)):  # Example threshold for leveling up
            self.level_up()

    def handle_obstacle_collision(spaceship, obstacles, current_time):
        for obstacle in obstacles:
            if pygame.math.Vector2(spaceship.x, spaceship.y).distance_to(pygame.math.Vector2(obstacle.x, obstacle.y)) < 15:
                spaceship.take_damage(1, current_time)  # Pass current_time here as well
                obstacles.remove(obstacle)

        
def draw_stars():
    # Move stars
    for i in range(len(stars)):
        stars[i] = (stars[i][0], stars[i][1] + 1 if stars[i][1] < SCREEN_HEIGHT else 0)
    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 1)

def broad_phase_collisions(player, enemies):
    player_rect = pygame.Rect(player.x - 15, player.y - 15, 20, 20)  # Approximate player size
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, 10, 10)  # Approximate enemy size
        if player_rect.colliderect(enemy_rect):
            return detailed_collision_check(player, enemy)  # Only check if bounding boxes collide
    return False


def check_collision(player, enemies, current_time):
    current_time = pygame.time.get_ticks()  # Get the current time
    for enemy in list(enemies):
        distance = pygame.math.Vector2(player.x, player.y).distance_to(pygame.math.Vector2(enemy.x, enemy.y))
        # Debug output for collision checking
        print(f"Checking collision: Player at ({player.x}, {player.y}) and Enemy at ({enemy.x}, {enemy.y}) with distance {distance}")
        if distance <= 25:  # Assuming a collision radius of 30
            player.take_damage(1, current_time)
            return True
        return False


enemy = Enemy(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))

def game_over_screen(screen, score, level):
    game_over_font = pygame.font.Font(None, 74)  # Large font for "Game Over"
    score_font = pygame.font.Font(None, 36)      # Smaller font for showing stats

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    spaceship.reset_game()  # Return True to indicate the player wants to restart
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False

        screen.fill(BLACK)  # Clear the screen or set a game over background

        # Display "Game Over" text
        game_over_text = game_over_font.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(game_over_text, game_over_rect)

        # Display Score
        score_text = score_font.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        # Display Level
        level_text = score_font.render(f"Reached Level: {level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(level_text, level_rect)

        # Instructions to restart or quit
        instructions_text = score_font.render("Press Enter to Restart or ESC to Exit", True, YELLOW)
        instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))
        screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()  # Update the display

        pygame.time.wait(100)  # Wait a little before the next frame to reduce CPU usage

# Game loop
def game_loop():
    clock = pygame.time.Clock()
    spaceship = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    enemies = [Enemy(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(5)]

    last_spawn_time = pygame.time.get_ticks()
    spawn_rate = 500  # Base spawn rate in milliseconds (1 second)
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Assuming 'r' is for 'reset'
                reset_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spaceship.shoot()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship.move('left')
        if keys[pygame.K_RIGHT]:
            spaceship.move('right')
        if keys[pygame.K_UP]:
            spaceship.move('up')
        if keys[pygame.K_DOWN]:
            spaceship.move('down')

        print(f"Spaceship position: ({spaceship.x}, {spaceship.y})")
        if check_collision(spaceship, enemies, current_time):
            damage_amount = 1
            spaceship.take_damage(damage_amount, current_time)


        # Adjust spawn rate based on level, reducing the interval by 0.1 seconds per level
        adjusted_spawn_rate = max(5, spawn_rate - spaceship.level * 10)  # Prevent spawn rate from going too low, min cap at 200 ms
        spaceship.max_experience = 100 + (spaceship.level * 10)
        LASER_SPEED = (4 + spaceship.level*10)
        LASER_TRAIL_LENGTH = (4 + spaceship.level*10) # Length of the laser trail
        SHIP_SPEED = 7 + (spaceship.level*10)

        # Spawn enemies with increasing value and speed
        if current_time - last_spawn_time > adjusted_spawn_rate:
            enemy_value = 10 + (spaceship.level // 100)  # Increase value based on score
            new_enemy = Enemy(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50), value=enemy_value)
            new_enemy.update_speed(spaceship.level + (random.randint(1, 5)))  # Update speed based on the current level
            enemies.append(new_enemy)
            last_spawn_time = current_time

        screen.fill(BLACK)
        
        draw_stars()
        spaceship.update_lasers(enemies)
        spaceship.draw(screen)

        # Update and draw the enemy
        for enemy in enemies:
            enemy.move_towards_player(spaceship)
            enemy.draw(screen)
            # Debug output for enemy position and health
            if enemy.health <= 0:
                enemies.remove(enemy)
                enemy.update()

        

        draw_health_bar(screen, BAR_PADDING, BAR_PADDING, spaceship.health, spaceship.max_health)
        draw_experience_bar(screen, BAR_PADDING, BAR_PADDING + HEALTH_BAR_HEIGHT + 5, spaceship.experience, spaceship.max_experience)

        health_text = font.render(f"Health: {spaceship.health}", True, WHITE)
        xp_text = font.render(f"XP: {spaceship.experience}/{spaceship.max_experience}", True, WHITE)
        level_text = font.render(f"Level: {spaceship.level}", True, WHITE)
        score_text = font.render(f"Score: {spaceship.score}", True, WHITE)
        
        
        screen.blit(health_text, (10, 10))
        screen.blit(xp_text, (10, 40))
        screen.blit(level_text, (10, 70))
        screen.blit(score_text, (250, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

game_loop()
