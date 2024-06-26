import pygame
import time
import random
import json
import os

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

display_width = 1400
display_height = 800

road_width = 600  
road_x = (display_width - road_width) // 2  
road_y = 0  
road_height = display_height  

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('RUNing-from-EU')

clock = pygame.time.Clock()

car_folder = 'cars'
car_colors = ['car1.png', 'car2.png', 'car3.png', 'car4.png', 'car5.png']

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


def load_flag_images():
    flag_names = ['austria.png', 'belgium.png', 'finland.png', 'hungarian.png', 'ireland.png', 'netherland.png', 'portugal.png', 'spain.png']
    flags = []
    flag_folder = 'flags'  
    for flag_name in flag_names:
        flag_path = os.path.join(flag_folder, flag_name)
        if os.path.isfile(flag_path):
            try:
                flag_image = pygame.image.load(flag_path).convert_alpha()
                flag_image = pygame.transform.scale(flag_image, (100, 100))  
                flags.append(flag_image)
            except pygame.error as e:
                print(f"Error loading flag image {flag_name}: {e}")
        else:
            print(f"Flag image {flag_name} not found in {flag_folder}")
    return flags


def car(x, y, car_image):
    game_display.blit(car_image, (x, y))

def crash():
    message_display('You Crashed!')

def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 80)
    text_surface = large_text.render(text, True, red)
    text_rect = text_surface.get_rect()
    text_rect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(text_surface, text_rect)
    pygame.display.update()
    
    time.sleep(2)  

def load_scores(filename):
    scores = {}
    try:
        with open(filename, 'r') as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  
    
    scores_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return scores_sorted

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
        top_3_scores = scores[:4]  
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

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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

def game_loop():
    username, previous_score = username_prompt()
    car_image = car_selection_screen()
    car_width, car_height = car_image.get_size()
    x = (display_width - car_width) // 2
    y = display_height * 0.8

    flag_images = load_flag_images()
    if not flag_images:
        print("No flag images found. Exiting.")
        pygame.quit()
        quit()

    obstacle_image = random.choice(flag_images)
    obstacle_start_x = random.randrange(int(road_x), int(road_x) + road_width - 100)
    obstacle_start_y = -600
    obstacle_speed = 7
    obstacle_width = 100
    obstacle_height = 100

    car_mask = pygame.mask.from_surface(car_image)
    obstacle_mask = pygame.mask.from_surface(obstacle_image)

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
                if event.key == pygame.K_UP:
                    y -= 50
                if event.key == pygame.K_DOWN:
                    y += 50

        game_display.fill(white)

        pygame.draw.rect(game_display, black, (road_x, road_y, road_width, road_height), 2)

        game_display.blit(obstacle_image, (obstacle_start_x, obstacle_start_y))
        obstacle_start_y += obstacle_speed

        if x < road_x:
            x = road_x
        elif x > road_x + road_width - car_width:
            x = road_x + road_width - car_width

        car(x, y, car_image)

        elapsed_time = time.time() - start_time
        obstacle_speed = 7 + int(elapsed_time // 5)

        timer_font = pygame.font.Font('freesansbold.ttf', 20)
        timer_text = timer_font.render(f"Time: {elapsed_time:.2f} seconds", True, black)
        game_display.blit(timer_text, (10, 10))

        if previous_score is not None:
            previous_score_text = timer_font.render(f"Previous record: {float(previous_score):.2f} seconds", True, black)
            game_display.blit(previous_score_text, (10, 40))

        car_rect = pygame.Rect(x, y, car_width, car_height)
        obstacle_rect = pygame.Rect(obstacle_start_x, obstacle_start_y, obstacle_width, obstacle_height)
        offset = (obstacle_rect.x - car_rect.x, obstacle_rect.y - car_rect.y)
        
        collision_point = car_mask.overlap(obstacle_mask, offset)
        if collision_point:
            crash()
            game_exit = True

        if obstacle_start_y > display_height:
            obstacle_start_y = -obstacle_height
            obstacle_start_x = random.randrange(int(road_x), int(road_x) + road_width - obstacle_width)
            obstacle_image = random.choice(flag_images)

        pygame.display.update()
        clock.tick(60)

    end_time = time.time()
    elapsed_time = end_time - start_time - 2
    save_score(username, elapsed_time)
    intro_screen()


def save_score(username, score):
    try:
        with open('scores.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[username] = score

    with open('scores.json', 'w') as f:
        json.dump(data, f)

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
                elif event.unicode.isalnum() or event.unicode == ' ':
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

def main():
    intro_screen()

if __name__ == '__main__':
    main()
