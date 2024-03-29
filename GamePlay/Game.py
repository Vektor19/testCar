import pygame
import sys
import random
from GamePlay.Button import Button
from Configuration.Configuration import Configuration
from Configuration.Car import Car
from GamePlay.GameCar import GameCar
from GamePlay.GameObstacle import GameObstacle
from GamePlay.Road import Road
from GamePlay.GameStateEnum import GameState 
from GamePlay.Menu import Menu
from GamePlay.ImagesUtils import ImagesUtils
# Test
class Game:
    """
    Represents the main game engine for the car racing game.

    Attributes:
        WIDTH (int): The width of the game window.
        HEIGHT (int): The height of the game window.
        FPS (int): Frames per second for the game.
        SPACE_FROM_BOTTOM (int): Space reserved from the bottom of the window.
        time_spawning (int): Time interval for spawning obstacles.
        session_status (GameState): The current state of the game session.
        screen (pygame.Surface): The game screen surface.
        car (GameCar): The player's car object.
        road (Road): The road object where the game takes place.
        leaders (list): List of leader objects containing player records.
        car_image (pygame.Surface): Image representing the player's car.
        obstacle_images (list): List of images representing various obstacles.
        obstacles_configuration (list): List of obstacle configurations.
        obstacles (list): List of obstacle objects currently present in the game.
        obstacle_timer (int): Timer for adding new obstacles.
        background_image (pygame.Surface): Background image for the game.
        score (int): The player's current score.
        score_font_color (tuple): RGB tuple representing the color of the score font.
        font (pygame.font.Font): Font object for rendering text.
        menu_button (Button): Button object for accessing the game menu.
    """
    def __init__(self, configuration: Configuration, leaders):
        """
        Initializes the game.

        Args:
            configuration (Configuration): The configuration object containing game settings.
            leaders (list): List of leader objects containing player records.
        """
        pygame.init()
        self.menu = Menu(self.resume_game, self.restart_game, self.quit_game)
        # Константи для вікна гри
        self.WIDTH, self.HEIGHT = configuration.map.width, configuration.map.height
        self.FPS = 60
        self.SPACE_FROM_BOTTOM = 150;
        self.time_spawning = 60 // configuration.level.speedModificator

        self.session_status = GameState.PLAYING
        # Створення вікна гри
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Car racing")

        self.car = self.__get_cargame__(configuration.car, configuration.level.speedModificator);

        road_speed = 5 * configuration.level.speedModificator
        self.road = Road(self.WIDTH // 4, 0, self.WIDTH // 2, self.HEIGHT, road_speed, 20)
        self.leaders = leaders

        # Завантаження картинок машини та перешкоди
        self.car_image = ImagesUtils.load_image(configuration.car.photo).convert_alpha()
        self.car_image = pygame.transform.scale(self.car_image, (self.car.width, self.car.height))
        
        self.obstacle_images = self.__get_obstacle_images__(configuration.obstacles)
        self.obstacles_configuration = configuration.obstacles
        # Список для зберігання перешкод
        self.obstacles = []
        # Лічильник часу для додавання нових перешкод
        self.obstacle_timer = 0
        
        self.background_image = ImagesUtils.load_image(configuration.map.photo).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        # Рахунок користувача
        self.score = 0
        self.score_font_color = configuration.font_color
        self.font = pygame.font.SysFont(None, 30)
        self.menu_button = Button("Menu", (self.WIDTH - 50, 0), (50, 50))


    def __get_cargame__(self, car: Car, speedModificator: int):
        """
        Creates a game car object.

        Args:
            car (Car): The car object.
            speedModificator (int): The speed modifier for the car.

        Returns:
            GameCar: The game car object.
        """
        # Початкові координати машини
        car_X = self.WIDTH // 2 - 25
        car_Y = self.HEIGHT - self.SPACE_FROM_BOTTOM;
        car_velocity = 5*speedModificator

        return GameCar(car, car_X, car_Y, car_velocity)

    def __get_obstacle_images__(self, obstacles_objects):
        """
        Loads and scales obstacle images.

        Args:
            obstacles_objects (list): List of obstacle objects.

        Returns:
            list: List of obstacle images.
        """
        obstacle_images = []
        for obstacle in obstacles_objects:
            obstacle_image = ImagesUtils.load_image(obstacle.photo).convert_alpha()
            obstacle_image = pygame.transform.scale(obstacle_image, (obstacle.width, obstacle.height))
            obstacle_images.append(obstacle_image)
        return obstacle_images

    def run(self):
        """Runs the main game loop."""
        # Основний цикл гри
        running = True
        while running:
            self.__handle_events__()
            if self.session_status == GameState.GAME_OVER:  # Перевіряємо, чи гра завершилася
                running = False  # Зупиняємо цикл гри
            elif self.session_status == GameState.MENU:
                self.menu.draw_menu(self.screen)
            else:
                self.update()
                self.render()

            # Контроль кадрів за секунду
            pygame.time.Clock().tick(self.FPS)
        
        self.display_results() # Показуємо результати

    def restart_game(self):
        """Restarts the game."""
        self.score = 0
        self.obstacles.clear()
        self.session_status = GameState.PLAYING
        self.menu.is_drawn = False

    def resume_game(self):
        """
        Resumes the game after pause.
        """
        self.session_status = GameState.PLAYING
        self.menu.is_drawn = False

    def quit_game(self):
        """Quits the game."""
        pygame.quit()
        sys.exit()

    def __handle_events__(self):
        """Handles game events such as key presses or mouse clicks."""
        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if self.menu_button.is_clicked(mouse_position):
                    self.session_status = GameState.MENU
                elif self.session_status == GameState.MENU:
                    for item in self.menu.menu_items:
                        if item.is_clicked(pygame.mouse.get_pos()):
                            item.action()

    def update(self):
        """Updates the game state."""
        # Керування машиною
        keys = pygame.key.get_pressed()
        print(keys)
        print(pygame.K_LEFT)
        if keys[pygame.K_LEFT]:
            self.car.X -= self.car.velocity
        if keys[pygame.K_RIGHT]:
            self.car.X += self.car.velocity

        # Обмеження руху машини в межах вікна
        if self.car.X < self.road.X:
            self.car.X = self.road.X
        elif self.car.X > self.road.X + self.road.width - self.car.width:
            self.car.X = self.road.X + self.road.width - self.car.width

        # Додавання нових перешкод через певний інтервал часу
        self.obstacle_timer += 1
        self.__add_new_obstacle__()
        self.__move_obstacles_down__()

    def __move_obstacles_down__(self):
        """Moves obstacles downwards."""
        # Рух перешкод вниз
        for obstacle in self.obstacles:
            obstacle.Y += self.car.velocity
            # Видалення перешкод, які вийшли за межі вікна
            if obstacle.Y > self.HEIGHT:
                self.obstacles.remove(obstacle)


            diff_betweent_car_and_obstacle = obstacle.Y - self.car.Y - self.car.height
            if  diff_betweent_car_and_obstacle <= 0 and diff_betweent_car_and_obstacle > -self.car.velocity:
                # Збільшення рахунку при проходженні перешкоди
                self.score += 1

            # Перевірка зіткнення з перешкодами
            if obstacle.Y + obstacle.height > self.car.Y and obstacle.Y < self.car.Y + self.car.height and self.car.X < obstacle.X + obstacle.width and self.car.X + self.car.width > obstacle.X:
                self.session_status = GameState.GAME_OVER

    def __add_new_obstacle__(self):
        """Adds a new obstacle."""
        if self.obstacle_timer >= self.time_spawning:  # Додавання нової перешкоди кожну секунду
            random_i = random.randint(0, len(self.obstacles_configuration)-1)
            obstacle = GameObstacle(self.obstacles_configuration[random_i], 0, 0, self.obstacle_images[random_i])

            # Випадковий вибір інтервалу для генерації перешкоди
            obstacle_intervals = [(self.road.X, self.road.X + self.road.width // 2 - obstacle.width - self.road.separate_line_width // 2), (self.road.X + self.road.width // 2 + self.road.separate_line_width // 2, self.road.X + self.road.width - obstacle.width)]
            interval = random.choice(obstacle_intervals)
            # Генерація випадкової позиції x з вибраного інтервалу
            obstacle.X = random.randint(*interval)

            self.obstacles.append(obstacle)
            self.obstacle_timer = 0

    def render(self):
        """Renders the game graphics on the screen."""
        # Оновлення екрану
        self.__draw_background__()

        self.__draw_road__()     

        self.__draw_user_car__()

        self.__draw_obstacles__()

        self.__draw_score__()

        self.menu_button.draw(self.screen)

        pygame.display.flip()

    def __draw_road__(self):
        """Draws the road on the game screen."""
        # Малювання дороги
        pygame.draw.rect(self.screen, (50, 50, 50), (self.road.X, self.road.Y, self.road.width, self.road.height))  # Сірий колір для асфальту
        pygame.draw.rect(self.screen, (255, 255, 255), (self.road.X + (self.road.width // 2) - self.road.separate_line_width // 2, self.road.Y, self.road.separate_line_width, self.road.height))  # Білий колір для розділової смуги

    def __draw_background__(self):
        """Draws the game background on the screen."""
        self.screen.blit(self.background_image, (0, 0))  # Відображення фонового зображення

    def __draw_user_car__(self):
        """Draws the user's car on the screen."""
        # pygame.draw.rect(self.screen, (0, 0, 0), (self.car.X, self.car.Y, self.car.width, self.car.height))
        self.screen.blit(self.car_image, (self.car.X, self.car.Y, self.car.width, self.car.height))

    def __draw_obstacles__(self):
        """Draws the obstacles on the screen."""
        # for obstacle in self.obstacles:
        #     pygame.draw.rect(self.screen, (0, 255,0 ), (obstacle.X, obstacle.Y, obstacle.width, obstacle.height))
        for obstacle in self.obstacles:
            self.screen.blit(obstacle.image, (obstacle.X, obstacle.Y, obstacle.width, obstacle.height))

    def __draw_score__(self):
        """Draws the user's score on the screen."""
        score_text = self.font.render("Score: " + str(self.score), True, self.score_font_color)
        self.screen.blit(score_text, (10, 10))

    def display_results(self):
        """Displays the game results on the screen."""
        # Завантаження результатів з файлу або з іншого джерела
        results = self.leaders

        # Сортування результатів за спаданням
        sorted_results = sorted(results, key=lambda x: x.record, reverse=True)

        # Відображення тексту та заднього фону у вікні гри
        font_title = pygame.font.SysFont("comicsansms", 40)
        font_body = self.font
        title_surface = font_title.render("Leader board", True, (255, 255, 255))
        background_rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)

        # Відображення заднього фону та тексту
        self.screen.fill((0, 0, 0))  # Заповнення екрану чорним кольором
        pygame.draw.rect(self.screen, (100, 100, 100), background_rect)  # Задній фон
        title_rect = title_surface.get_rect(center=(self.WIDTH // 2, 50))

        self.screen.blit(title_surface, title_rect)  # Надпис "Leader board"

        y_position = 150  # Початкова позиція по вертикалі
        for result in sorted_results:
            result_text = "{}: {}".format(result.nickname, result.record)
            text_surface = font_body.render(result_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(midtop=(self.WIDTH // 2, y_position))  # Розміщення по вертикалі
            self.screen.blit(text_surface, text_rect)  # Список лідерів
            y_position += 50  # Збільшення позиції по вертикалі для наступного рядка

        # Відображення результату гравця
        result_text = "Your result: {}".format(self.score)
        result_surface = font_body.render(result_text, True, (255, 255, 255))
        result_rect = result_surface.get_rect(center=(self.WIDTH // 2, y_position + 50))  # Розміщення по вертикалі
        self.screen.blit(result_surface, result_rect)  # Надпис "Your result"

        pygame.display.flip()