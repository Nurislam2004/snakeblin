import pygame
import random

class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position, body_color):
        """
        Инициализация объекта.

        :param position: Позиция объекта на игровом поле (кортеж (x, y)).
        :param body_color: Цвет объекта (RGB кортеж).
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта.

        :param surface: Поверхность для отрисовки.
        """
        pass

class Apple(GameObject):
    """Класс, представляющий яблоко на игровом поле."""

    def __init__(self, position=None):
        """
        Инициализация яблока.

        :param position: Позиция яблока на игровом поле (кортеж (x, y)).
        """
        super().__init__(position, (255, 0, 0))  # Красный цвет
        if position is None:
            self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (random.randint(0, 31) * 20, random.randint(0, 23) * 20)

    def draw(self, surface):
        """
        Отрисовка яблока на игровой поверхности.

        :param surface: Поверхность для отрисовки.
        """
        pygame.draw.rect(surface, self.body_color, pygame.Rect(self.position[0], self.position[1], 20, 20))

class Snake(GameObject):
    """Класс, представляющий змейку на игровом поле."""

    def __init__(self, position):
        """
        Инициализация змейки.

        :param position: Начальная позиция змейки на игровом поле (кортеж (x, y)).
        """
        super().__init__(position, (0, 255, 0))  # Зеленый цвет
        self.length = 1
        self.positions = [position]
        self.direction = (20, 0)  # Начальное направление движения вправо
        self.next_direction = None

    def update_direction(self, direction):
        """
        Обновляет направление движения змейки.

        :param direction: Новое направление движения (кортеж (dx, dy)).
        """
        if direction != (-self.direction[0], -self.direction[1]):
            self.next_direction = direction

    def move(self):
        """Обновляет позицию змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        new_head = (self.positions[0][0] + self.direction[0], self.positions[0][1] + self.direction[1])

        # Проверка на выход за границы поля
        if new_head[0] >= 640:
            new_head = (0, new_head[1])
        elif new_head[0] < 0:
            new_head = (640 - 20, new_head[1])
        elif new_head[1] >= 480:
            new_head = (new_head[0], 0)
        elif new_head[1] < 0:
            new_head = (new_head[0], 480 - 20)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """
        Отрисовка змейки на игровой поверхности.

        :param surface: Поверхность для отрисовки.
        """
        for position in self.positions:
            pygame.draw.rect(surface, self.body_color, pygame.Rect(position[0], position[1], 20, 20))

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        :return: Позиция головы змейки (кортеж (x, y)).
        """
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = (20, 0)
        self.next_direction = None



def main():

    """Основная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake((320, 240))
    apple = Apple()

    def handle_keys():
        """Обрабатывает нажатия клавиш для управления змейкой."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.update_direction((0, -20))
                elif event.key == pygame.K_DOWN:
                    snake.update_direction((0, 20))
                elif event.key == pygame.K_LEFT:
                    snake.update_direction((-20, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction((20, 0))

    while True:
        handle_keys()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill((0, 0, 0))  # Очистка экрана
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(10)  # Замедление игры до 10 кадров в секунду

if __name__ == "__main__":
    main()