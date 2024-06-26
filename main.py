import pygame
import time
import random
import json
import os

# Initialize pygame
pygame.init()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Set display size
display_width = 1400
display_height = 800

# Define road boundaries
road_width = 600  # Width of the road
road_x = (display_width - road_width) // 2  # X-coordinate of the road
road_y = 0  # Y-coordinate of the road
road_height = display_height  # Height of the road

# Configure display
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('RUNing-from-EU')

# Define clock
clock = pygame.time.Clock()

# Car image paths
car_folder = 'cars'
car_colors = ['car1.png', 'car2.png', 'car3.png', 'car4.png', 'car5.png']

# Flag image paths
flag_folder = 'flags'
flag_images = ['austria.png', 'belgium.png', 'finland.png', 'hungarian.png', 'ireland.png', 'netherland.png', 'portugal.png', 'spain.png']

# Load car images
def load_car_images():
    cars = {}
    car_width = 150
    car_height = 250
    for color in car_colors:
        car_path = os.path.join(car_folder, color)
        if not os.path.exists(car_path):
            print(f"Error: file {color} not found.")
            return None
        try:
            original_image = pygame.image.load(car_path)
            scaled_image = pygame.transform.scale(original_image, (car_width, car_height))
            cars[color] = scaled_image
        except pygame.error as e:
            print(f"Error loading image {color}: {e}")
            return None
    return cars

# Load flag images
def load_flag_images():
    flags = []
    for filename in flag_images:
        flag_path = os.path.join(flag_folder, filename)
        if os.path.isfile(flag_path):
            try:
                flag_image = pygame.image.load(flag_path).convert_alpha()
                flags.append(flag_image)
            except pygame.error as e:
                print(f"Error loading flag image {filename}: {e}")
    return flags

# Display car on screen
def car(x, y, car_image):
    game_display.blit(car_image, (x, y))

# Display crash message
def crash():
    message_display('You Crashed!')

# Display text on screen
def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 80)
    text_surface = large_text.render(text, True, red)
    text_rect = text_surface.get_rect()
    text_rect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(text_surface, text_rect)
    pygame.display.update()
    
    time.sleep(2)  # Remove the delay here to avoid adding time to the score

# Load previous scores
def load_scores(filename):
    scores = {}
    try:
        with open(filename, 'r') as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Return empty dict if file not found or cannot be decoded
    
    scores_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return scores_sorted

# Display intro screen with previous scores
def intro_screen():
    intro = True
    while intro:
        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 40)
        text_surface = large_text.render("Score History:", True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((display_width / 2), (display_height / 2 - 100))
        game_display.blit(text_surface, text_rect)

        scores = load_scores('scores.json')
        top_3_scores = scores[:4]  # Get top 3 scores
        if top_3_scores:
            text_y = display_height / 2
            for username, score in top_3_scores:
                score_text = f'{username}: {float(score):.2f} s'
                score_surface = large_text.render(score_text, True, black)
                score_rect = score_surface.get_rect()
                score_rect.center = ((display_width / 2), text_y)
                game_display.blit(score_surface, score_rect)
                text_y += 50
        else:
            no_score_text = 'No previous games recorded.'
            no_score_surface = large_text.render(no_score_text, True, black)
            no_score_rect = no_score_surface.get_rect()
            no_score_rect.center = ((display_width / 2), (display_height / 2))
            game_display.blit(no_score_surface, no_score_rect)

        if button("New Game", display_width / 2 - 100, display_height - 100, 200, 50, green, blue):
            game_loop()
        
        if button("Show All Scores", display_width / 2 - 100, display_height - 200, 200, 50, green, blue):
            show_all_scores()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Show all scores screen
def show_all_scores():
    showing_scores = True
    while showing_scores:
        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 40)
        text_surface = large_text.render("All Scores:", True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((display_width / 2), (display_height / 3 - 100))
        game_display.blit(text_surface, text_rect)

        scores = load_scores('scores.json')
        if scores:
            text_y = display_height / 3.5
            for username, score in scores:
                score_text = f'{username}: {float(score):.2f} s'
                score_surface = large_text.render(score_text, True, black)
                score_rect = score_surface.get_rect()
                score_rect.center = ((display_width / 2), text_y)
                game_display.blit(score_surface, score_rect)
                text_y += 50
        else:
            no_score_text = 'No previous games recorded.'
            no_score_surface = large_text.render(no_score_text, True, black)
            no_score_rect = no_score_surface.get_rect()
            no_score_rect.center = ((display_width / 2), (display_height / 2))
            game_display.blit(no_score_surface, no_score_rect)

        if button("Back", display_width / 2 - 100, display_height - 100, 200, 50, red, blue):
            showing_scores = False

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Create button on screen
def button(msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))

    small_text = pygame.font.Font('freesansbold.ttf', 20)
    text_surf = small_text.render(msg, True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(text_surf, text_rect)

    return False

# Main game loop
def game_loop():
    username, previous_score = username_prompt()
    car_image = car_selection_screen()
    car_width, car_height = car_image.get_size()
    x = (display_width - car_width) // 2
    y = display_height * 0.8

    obstacle_start_x = random.randrange(int(road_x), int(road_x) + road_width - 100)
    obstacle_start_y = -600
    obstacle_speed = 7
    obstacle_width = 100
    obstacle_height = 100

    flags = load_flag_images()

    start_time = time.time()
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 50
                if event.key == pygame.K_RIGHT:
                    x += 50

        game_display.fill(white)

        # Draw road
        pygame.draw.rect(game_display, black, (road_x, road_y, road_width, road_height), 2)

        # Draw obstacles (flags)
        if flags:
            flag_image = random.choice(flags)
            game_display.blit(flag_image, (obstacle_start_x, obstacle_start_y))

        obstacle_start_y += obstacle_speed

        # Ensure car stays within the road boundaries
        if x < road_x:
            x = road_x
        elif x > road_x + road_width - car_width:
            x = road_x + road_width - car_width

        car(x, y, car_image)

        # Increase difficulty over time
        elapsed_time = time.time() - start_time
        obstacle_speed = 7 + int(elapsed_time // 5)

        # Display timer on screen
        timer_font = pygame.font.Font('freesansbold.ttf', 20)
        timer_text = timer_font.render(f"Time: {elapsed_time:.2f} seconds", True, black)
        game_display.blit(timer_text, (10, 10))

        # Display previous score if exists
        if previous_score is not None:
            previous_score_text = timer_font.render(f"Previous record: {float(previous_score):.2f} seconds", True, black)
            game_display.blit(previous_score_text, (10, 40))

        # Collision detection with obstacles
        if y < obstacle_start_y + obstacle_height:
            if x > obstacle_start_x and x < obstacle_start_x + obstacle_width or x + car_width > obstacle_start_x and x + car_width < obstacle_start_x + obstacle_width:
                crash()
                game_exit = True

        # Reset obstacle position if it goes off screen
        if obstacle_start_y > display_height:
            obstacle_start_y = -obstacle_height
            obstacle_start_x = random.randrange(int(road_x), int(road_x) + road_width - obstacle_width)

        pygame.display.update()
        clock.tick(60)

    end_time = time.time()
    elapsed_time = end_time - start_time - 2
    save_score(username, elapsed_time)
    intro_screen()

# Save current game time
def save_score(username, score):
    try:
        with open('scores.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[username] = score

    with open('scores.json', 'w') as f:
        json.dump(data, f)

# Username input screen
def username_prompt():
    username = ''
    font = pygame.font.Font('freesansbold.ttf', 32)
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.unicode.isalnum() or event.unicode == ' ':  # Allow alphanumeric characters and spaces
                    username += event.unicode

        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 75)
        text_surface = large_text.render("Enter your name:", True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((display_width / 2), (display_height / 2 - 50))
        game_display.blit(text_surface, text_rect)

        input_surface = font.render(username, True, black)
        input_rect = input_surface.get_rect()
        input_rect.center = ((display_width / 2), (display_height / 2 + 50))
        game_display.blit(input_surface, input_rect)

        pygame.display.update()
        clock.tick(15)

    scores = load_scores('scores.json')
    previous_score = dict(scores).get(username)

    return username, previous_score

# Car color selection screen
def car_selection_screen():
    cars = load_car_images()
    selected_car = None

    if cars is None:
        pygame.quit()
        quit()

    while selected_car is None:
        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 75)
        text_surface = large_text.render("Select your car:", True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((display_width / 2), (display_height / 2 - 200))
        game_display.blit(text_surface, text_rect)

        car_x = 150
        for car_color, car_image in cars.items():
            game_display.blit(car_image, (car_x, display_height / 2 - 100))
            if button("Select", car_x, display_height / 2 + 100, 100, 50, green, blue):
                selected_car = car_image
            car_x += 200

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    return selected_car

# Main function to start the game
def main():
    intro_screen()

if __name__ == '__main__':
    main()
