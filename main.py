import pygame as py
import math # Helps with stats calculations
import os  
import random # Helps in generating the enemies in random positions
import time # Helps record game time and easily get stats

py.init()
py.mixer.init() 

LIGHT_BLUE = (135, 206, 250)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
PINK = (255, 105, 180)
FUCHSIA = (255, 0, 255) 
BLUE = (173, 216, 230)


# Setting up window display
width, height = 800, 850
screen = py.display.set_mode((width, height))
screen.fill(WHITE)
py.display.set_caption('AGAINST ALL ODDS')

# Setting up main circle
circle_color = BLACK
circle_radius = 200
circle_thickness = 10
circle_position = (width // 2, height // 2)
circle_angle = 180
circle_speed = 0.001

# Loading the user sprite
user_image = py.image.load(os.path.join("Assets", "attack2.png"))
user_image_orig = user_image.copy()  # Make a copy of the original image for rotation
user_rect = user_image.get_rect(center=circle_position)

# Randomly setting the starting position of the user sprite on the circle border
user_start_angle = random.uniform(0, 2*math.pi)
user_rect = user_image.get_rect(center=circle_position)
user_rect.center = (circle_position[0] + math.cos(user_start_angle) * circle_radius,
                    circle_position[1] + math.sin(user_start_angle) * circle_radius)

# Creating the circle surface
circle_surface = py.Surface((circle_radius * 2, circle_radius * 2), py.SRCALPHA)
py.draw.circle(circle_surface, circle_color, (circle_radius, circle_radius), circle_radius, circle_thickness)


reload_sound = py.mixer.Sound(os.path.join('Assets', 'reloads.wav'))
hit_sound = py.mixer.Sound(os.path.join('Assets', 'hit.wav'))
shoot_sound = py.mixer.Sound(os.path.join('Assets', 'shoot.wav'))
move_sound = py.mixer.Sound(os.path.join('Assets', 'move.wav'))
bang_sound = py.mixer.Sound(os.path.join('Assets', 'bang.wav'))
game_sound = py.mixer.Sound(os.path.join('Assets', 'game.wav'))
intro_sound = py.mixer.Sound(os.path.join('Assets', 'intro.wav'))
outro_sound = py.mixer.Sound(os.path.join('Assets', 'outro.wav'))

# lowering background music sound
game_sound.set_volume(0.5)

intro_sound.set_volume(0.1)

# Setting up the font
font = py.font.SysFont('Comic Sans MS', 36)


def show_home_screen():
    while True:
        # Handle events
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()

        # Drawing the background
        screen.fill(BLACK)
        info_font = py.font.SysFont('Comic Sans MS', 20)
        rule_font = py.font.SysFont('Comic Sans MS', 30)

        # Draw design
        for i in range(20):
            snowflake_pos = (random.randint(0, width), random.randint(0, height))
            py.draw.circle(screen, ORANGE, snowflake_pos, 2)

        # Drawing the title and button
        title_text = font.render("AGAINST ALL ODDS", True, WHITE)
        move_text = info_font.render("A and D ~ Move", True, WHITE)
        shoot_text = info_font.render("SPACE BAR ~ Shoot", True, WHITE)
        reload_text = info_font.render("R ~ reload", True, WHITE)
        info_text = info_font.render("'Annoying, hard, rigged... Call it what you want'", True, WHITE)
        border = info_font.render("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", True, WHITE)
        rules = rule_font.render("RULES", True, WHITE)
        rule1 = info_font.render("Shoot the glowing circles that move towards you to gain points", True, WHITE)
        rule2 = info_font.render("If the glowing circle ends up hitting your base (spinning circle), you lose a life", True, WHITE)
        rule3 = info_font.render("You only have 10 bullets to shoot before having to reload", True, WHITE)
        rule4 = info_font.render("Reloading is only allowed once all 10 bullets have been used", True, WHITE)
        rule5 = info_font.render("Ohh, and who said you can gain lives...", True, WHITE)
        screen.blit(title_text, (230, 10))
        screen.blit(info_text, (190, 100))
        screen.blit(move_text, (330, 150))
        screen.blit(shoot_text, (307, 200))
        screen.blit(reload_text, (355, 250))
        screen.blit(border, (10, 300))
        screen.blit(rules, (355,330))
        screen.blit(rule1, (110, 400))
        screen.blit(rule2, (40, 450))
        screen.blit(rule3, (140, 500))
        screen.blit(rule4, (133, 550))
        screen.blit(rule5, (230, 600))

        # Drawing the button
        start_button_text = font.render("Start Game", True, WHITE)
        start_button_rect = start_button_text.get_rect(center=(400,800))
        mouse_pos = py.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            py.draw.rect(screen, BLUE, start_button_rect, border_radius=10)
        else:
            py.draw.rect(screen, LIGHT_BLUE, start_button_rect, border_radius=10)
        py.draw.rect(screen, WHITE, start_button_rect, 3, border_radius=10)
        screen.blit(start_button_text, start_button_rect)

        # Checking if button got clicked
        mouse_pressed = py.mouse.get_pressed()
        if start_button_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            return  # Exit the function to start the game

        # Updating screen
        py.display.update()

high_score = 0

def show_end_screen():
    global high_score
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()
        
        # Draw the background
        screen.fill(BLACK)
        
        # Update high score
        if score > high_score:
            high_score = score

        for i in range(20):
            snowflake_pos = (random.randint(0, width), random.randint(0, height))
            py.draw.circle(screen, ORANGE, snowflake_pos, 2)

        title_font = py.font.SysFont('Comic Sans MS', 60)
        aao = title_font.render('AGAINST ALL ODDS', True, WHITE)
        screen.blit(aao, (100, 5))

        # Creating the box to store the stats
        box_rect = py.Rect(150, 150, 500, 500)

        # Draw the end screen elements inside the box
        font = py.font.SysFont('Comic Sans MS', 40)
        title_text = font.render("GAME OVER", True, WHITE)
        high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
        score_text = font.render("Your Score: " + str(score), True, WHITE)
        time_text = font.render("Bullets Fired: " + str(bullets_used_count), True, WHITE)

        accuracy = 0
        if bullets_used_count != 0:
            accuracy = math.ceil((score / bullets_used_count) * 100)# math.ceil rounds up to whole number
        accuracy_text = font.render("Accuracy: " + str(accuracy) + "%", True, WHITE)
        
        screen.blit(title_text, (box_rect.centerx - title_text.get_width() // 2, box_rect.top + 30))
        py.draw.rect(screen, WHITE, box_rect, 3, border_radius=10)
        screen.blit(high_score_text, (box_rect.left + 120, box_rect.top + 150))
        screen.blit(score_text, (box_rect.left + 120, box_rect.top + 250))
        screen.blit(time_text, (box_rect.left + 110, box_rect.top + 350))
        screen.blit(accuracy_text, (box_rect.left + 120, box_rect.top + 450))

        # Drawing the button
        font = py.font.SysFont('Comic Sans MS', 50)
        start_button_text = font.render("Play Again", True, WHITE)
        start_button_rect = start_button_text.get_rect(center=(box_rect.centerx, box_rect.bottom + 120))
        py.draw.rect(screen, LIGHT_BLUE, start_button_rect, border_radius=10)
        py.draw.rect(screen, WHITE, start_button_rect, 3, border_radius=10)
        screen.blit(start_button_text, start_button_rect)

        # Checking for button 
        mouse_pos = py.mouse.get_pos()
        mouse_pressed = py.mouse.get_pressed()
        if start_button_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            main()
            return  # Exit the function to start the game

        # Updating the screen
        py.display.update()


        # Adding a small delay to reduce CPU usage
        py.time.delay(10)


def generate_attacking_circle(current_time):
    attacking_circle_radius = random.randint(10, 30)
    max_attacking_circle_speed = 0.3
    elapsed_time = current_time / 1000 
    attacking_circle_speed = min(max_attacking_circle_speed, elapsed_time * 0.003)
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'left':
        attacking_circle_x = -attacking_circle_radius
        attacking_circle_y = random.randint(0, height)
    elif side == 'right':
        attacking_circle_x = width + attacking_circle_radius
        attacking_circle_y = random.randint(0, height)
    elif side == 'top':
        attacking_circle_x = random.randint(0, width)
        attacking_circle_y = -attacking_circle_radius
    else:
        attacking_circle_x = random.randint(0, width)
        attacking_circle_y = height + attacking_circle_radius
    return (attacking_circle_x, attacking_circle_y, attacking_circle_radius, attacking_circle_speed)

max_bullets = 10
bullets_fired = 0

home_screen_showed = False

def reset_game():
    global lives, score, attacking_circles, start_time, bullets, bullets_used_count, bullets_fired
    
    # Reset game variables
    lives = 3
    score = 0
    attacking_circles = []
    bullets = 10
    bullets_fired = 0
    bullets_used_count = 0


def main():
    global circle_angle, score, circle_speed, bullets, home_screen_showed
    # Only show home screen once
    reset_game()
    if not home_screen_showed:
        intro_sound.play()
        show_home_screen()
        home_screen_showed = True
    # Starting timer once user clicks play button
    if home_screen_showed == True:
        intro_sound.stop()
        change_of_direction_time = py.time.get_ticks() + 15000  # 15 seconds from now
    score = 0
    bullets = []
    bullet_speed = 7
    attacking_circles = []
    lives = 3

    # Timer for spawning enemies
    enemy_timer = 0
    enemy_spawn_time = 5  # 5 seconds

    # Starting time
    start_time = time.time()

    def shoot():
        global bullets, bullet_speed_x, bullet_speed_y, bullets_fired, bullets_used_count
            
        if bullets_fired >= max_bullets:
            return

        # Calculating the velocity vector of the bullet based on the angle of the user sprite
        bullet_speed_x = bullet_speed * math.sin(user_angle)
        bullet_speed_y = -bullet_speed * math.cos(user_angle)

        # Creating the bullet
        bullet_rect = py.Rect(user_rect.centerx - 5, user_rect.centery - 5, 10, 15)

        bullets.append(bullet_rect)
        bullets_fired += 1
        bullets_used_count += 1
        

    def reload():
        global bullets_fired
        bullets_fired = 0

    game_sound.play()

    while True:
        current_time = time.time() - start_time

        if current_time >= 120:
            enemy_spawn_time = 0.5
        elif current_time >= 60:
            enemy_spawn_time = 2
        elif current_time >= 25:
            enemy_spawn_time = 4  

        # Spawning a new enemy every 5 seconds (default time)
        if current_time - enemy_timer >= enemy_spawn_time:
            attacking_circle = generate_attacking_circle(current_time * 1000)
            attacking_circles.append(attacking_circle)
            enemy_timer = current_time

        if py.time.get_ticks() >= change_of_direction_time:
            circle_speed *= -1
            change_of_direction_time += 15000  # 15 seconds from now


        # Updating the attacking circles position
        for _ in range(len(attacking_circles)):
            attacking_circle_x, attacking_circle_y, attacking_circle_radius, attacking_circle_speed = attacking_circles[0]
            center_x = width // 2
            center_y = height // 2
            dx = center_x - attacking_circle_x
            dy = center_y - attacking_circle_y
            distance_to_center = math.sqrt(dx ** 2 + dy ** 2)
            if distance_to_center > 0:
                dx_normalized = dx / distance_to_center
                dy_normalized = dy / distance_to_center
                attacking_circle_x += dx_normalized * attacking_circle_speed
                attacking_circle_y += dy_normalized * attacking_circle_speed
            attacking_circles[0] = (attacking_circle_x, attacking_circle_y, attacking_circle_radius, attacking_circle_speed)
            if distance_to_center <= circle_radius + attacking_circle_radius:
                attacking_circles.pop(0)
                bang_sound.play()
                lives -= 1
                if lives == 0:
                    # End the game
                    outro_sound.play()
                    show_end_screen()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_a:
                    # Moving the user sprite counterclockwise on the circle
                    move_sound.play()
                    circle_angle -= math.pi/10
                elif event.key == py.K_d:
                    # Moving the user sprite clockwise on the circle
                    move_sound.play()
                    circle_angle += math.pi/10
                elif event.key == py.K_SPACE:
                    # Check if user has bullets remaining or not
                    if bullets_fired != max_bullets:
                        shoot_sound.play()
                    shoot()
                elif event.key == py.K_r:
                    if bullets_fired != max_bullets:
                        break
                    reload_sound.play()
                    reload()

        # Updating the circle angle/speed
        circle_angle += circle_speed

        # Rotating the user sprite to align with the circle angle/speed
        user_angle = circle_angle + math.pi / 2  # Add pi/2 to align with top of circle
        user_image = py.transform.rotate(user_image_orig, -math.degrees(user_angle))
        user_rect = user_image.get_rect(center=circle_position)

        # Calculation of the position of the user sprite on the circle
        user_x = circle_position[0] + math.cos(circle_angle) * circle_radius
        user_y = circle_position[1] + math.sin(circle_angle) * circle_radius
        user_rect.center = (user_x, user_y)

        # Rotating the circle surface to align with the user angle
        circle_surface_rotated = py.transform.rotate(circle_surface, math.degrees(-user_angle))
        rotated_rect = circle_surface_rotated.get_rect(center=circle_position)

        # Drawing the rotated circle onto the screen
        screen.fill(WHITE)
        screen.blit(circle_surface_rotated, rotated_rect)

        # Drawing the user sprite onto the screen
        screen.blit(user_image, user_rect)

        # Drawing the attacking circles onto the screen
        for attacking_circle_x, attacking_circle_y, attacking_circle_radius, _ in attacking_circles:
            random_color = random.randint(1, 3)
            if random_color == 1:
                color = PINK
            elif random_color == 2:
                color = FUCHSIA
            else:
                color = PURPLE
            py.draw.circle(screen, color, (int(attacking_circle_x), int(attacking_circle_y)), attacking_circle_radius)

        # Drawing the score onto the screen
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Drawing the bullet count or reload message onto the screen
        if bullets_fired == max_bullets:
            reload_text = font.render('Out of Bullets', True, BLACK)
            screen.blit(reload_text, (280, 400))
        else:
            bullet_text = font.render(f"Bullets: {max_bullets - bullets_fired}/{max_bullets}", True, BLACK)
            screen.blit(bullet_text, (280, 400))

        # Loading the heart image
        heart_image = py.image.load(os.path.join("Assets", "lives.png"))

        heart1_position = (510, 740)
        heart2_position = (580, 740)
        heart3_position = (650, 740)
        
        # The images are being drawn in backwards order so that when user loses a live, the starting heart is gone and not the last.
        if lives >= 1:
            screen.blit(heart_image, heart3_position)
        if lives >= 2:
            screen.blit(heart_image, heart2_position)
        if lives >= 3:
            screen.blit(heart_image, heart1_position)

        # Checking if any bullet has hit an attacking circle
        for bullet_rect in bullets:
            for i, attacking_circle in enumerate(attacking_circles):
                attacking_circle_x, attacking_circle_y, attacking_circle_radius, _ = attacking_circle
                if math.hypot(attacking_circle_x - bullet_rect.centerx, attacking_circle_y - bullet_rect.centery) <= attacking_circle_radius:
                    # Remove the bullet and the attacking circle that has been hit
                    hit_sound.play()
                    del attacking_circles[i]
                    bullets.remove(bullet_rect)
                    score += 1
                    break

        # Moving and drawing the bullets
        for bullet_rect in bullets:
            bullet_rect.move_ip(bullet_speed_x, bullet_speed_y)
            py.draw.circle(screen, BLACK, bullet_rect.center, 10)

            # Removing any bullets that have gone off the screen
            if not screen.get_rect().colliderect(bullet_rect):
                bullets.remove(bullet_rect)
       

        # Removing any bullets that have gone off the top of the screen
        bullets = [bullet_rect for bullet_rect in bullets if bullet_rect.bottom > 0]

        # Updating the screen
        py.display.update()





if __name__ == "__main__":
    main()