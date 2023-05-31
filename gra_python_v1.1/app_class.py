import sys
from player_class import *
from enemy_class import *
import random

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()
        self.bg_win = pygame.image.load('bg.png')
        self.point = pygame.image.load('pkt.png')
        self.lose = pygame.image.load('przegrana.png')
        self.question = 0
        self.question_bg = pygame.image.load('pytania.png')
        self.bg_poczatek = pygame.image.load('poczatek.png')

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            elif self.state == 'win':
                self.win_events()
                self.win_update()
                self.win_draw()
            elif self.state == 'question':
                self.question_events()
                self.question_update()
                self.question_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ############################ Funkcje pomocnicze ##################################

    @staticmethod
    def draw_text(words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    # załadowanie tla i przeskalowanie go do odpowiednich wymiarów

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # otwieranie pliku walls
        # tworzenie listy scian z koordynatami scian
        # zapisanymi jako wektor
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height),
                             (WIDTH, x * self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

    ########################### Intro funkcje ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_poczatek, (MAIN_BUFFER, MAIN_BUFFER))
        self.draw_text('Student-man', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 200], 56, (181, 153, 53), 'impact', centered=True)
        self.draw_text('Wciśnij Spacje aby rozpocząć', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 50], 26, RED, 'impact', centered=True)
        self.draw_text('Tryb 1 gracza', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 150], 26, (44, 167, 198), 'impact', centered=True)
#        self.draw_text('Wykonane przez:', self.screen, [WIDTH // 2, HEIGHT // 2 + 100], START_TEXT_SIZE, (255, 250, 205),
#                       START_FONT, centered=True)
#        self.draw_text('Kozak Aleksandra', self.screen, [WIDTH // 2, HEIGHT // 2 + 130], START_TEXT_SIZE, (255, 250, 205),
#                       START_FONT, centered=True)
#        self.draw_text('Łukasik Łukasz', self.screen, [WIDTH // 2, HEIGHT // 2 + 160], START_TEXT_SIZE, (255, 250, 205),
#                      START_FONT, centered=True)
#        self.draw_text('Majewski Jakub', self.screen, [WIDTH // 2, HEIGHT // 2 + 190], START_TEXT_SIZE, (255, 250, 205),
#                       START_FONT, centered=True)
#        self.draw_text('Mazurek Krzysztof', self.screen, [WIDTH // 2, HEIGHT // 2 + 220], START_TEXT_SIZE, (255, 250, 205),
#                       START_FONT, centered=True)
#        self.draw_text('Michalec Mateusz', self.screen, [WIDTH // 2, HEIGHT // 2 + 250], START_TEXT_SIZE, (255, 250, 205),
#                       START_FONT, centered=True)
#        self.draw_text('Zając Mikołaj', self.screen, [WIDTH // 2, HEIGHT // 2 + 280], START_TEXT_SIZE, (255, 250, 205),
#                       START_FONT, centered=True)
        pygame.display.update()

    ########################### Gra funkcje ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

        if self.player.current_score == 287:
            #287
            self.state = "win"

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        self.draw_text('Aktualny Wynik: {}'.format(self.player.current_score),
                       self.screen, [WIDTH // 2, 10], 18, WHITE, START_FONT, centered=True)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.question = random.randint(1, 12)
            self.state = 'question'
#            self.player.grid_pos = vec(self.player.starting_pos)
#            self.player.pix_pos = self.player.get_pix_pos()
#            self.player.direction *= 0
#            for enemy in self.enemies:
#                enemy.grid_pos = vec(enemy.starting_pos)
#                enemy.pix_pos = enemy.get_pix_pos()
#                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            self.screen.blit(self.point, (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2 - 7,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2 - 5))
#           pygame.draw.circle(self.screen, (124, 123, 7),
#                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
#                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    ########################### Koniec gry funkcje ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.lose, (MAIN_BUFFER, MAIN_BUFFER))
        quit_text = "Wciśnij Escape aby wyjść z gry."
        again_text = "Wciśnij Spacje aby zagrać ponownie"
        self.draw_text("Niestety nie udało Ci się zaliczyć semestru", self.screen, [WIDTH // 2, 100], 34, RED, "impact", centered=True)
        self.draw_text("Twój wynik to: {} punktów ECTS".format(self.player.current_score), self.screen, [
            WIDTH // 2, 150], 46, WHITE, "impact", centered=True)
        self.draw_text(again_text, self.screen, [
            WIDTH // 2, HEIGHT // 2], 36, RED, "impact", centered=True)
        self.draw_text(quit_text, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 36, RED, "impact", centered=True)
        pygame.display.update()

    ########################### Wygrana funkcje ################################

    def win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def win_update(self):
        pass

    def win_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_win, (MAIN_BUFFER, MAIN_BUFFER))
        quit_text = "Wciśnij Escape aby wyjść z gry."
        again_text = "Wciśnij Spacje aby zagrać ponownie"
        self.draw_text("Udało Ci się uzyskać zaliczenie", self.screen, [WIDTH // 2, 100], 46, RED, "impact", centered=True)
        self.draw_text("Twój wynik to: {} punktów ECTS".format(self.player.current_score), self.screen, [
            WIDTH // 2, 150], 46, BLACK, "impact", centered=True)
        self.draw_text(again_text, self.screen, [
            WIDTH // 2, HEIGHT // 2], 36, RED, "impact", centered=True)
        self.draw_text(quit_text, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 36, RED, "impact", centered=True)
        pygame.display.update()

    ########################### pytania funkcje ################################

    def question_events(self):
        if self.question == 5:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.player.lives += 1
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
        elif self.question == 2 or self.question == 8 or self.question ==  10:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.player.lives += 1
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
        elif self.question == 1 or self.question == 4 or self.question == 6 or self.question == 9 or self.question == 11:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.player.lives += 1
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
        elif self.question == 3 or self.question == 7 or self.question == 12:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.player.lives += 1
                    self.player.grid_pos = vec(self.player.starting_pos)
                    self.player.pix_pos = self.player.get_pix_pos()
                    self.player.direction *= 0
                    for enemy in self.enemies:
                        enemy.grid_pos = vec(enemy.starting_pos)
                        enemy.pix_pos = enemy.get_pix_pos()
                        enemy.direction *= 0
                    self.state = 'playing'

    def question_update(self):
        pass

    def question_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.question_bg, (MAIN_BUFFER, MAIN_BUFFER))
        if self.question == 1:
            self.draw_text("Co robi typowy informatyk jak coś się zepsuje?", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. siada i płacze", self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. oddaje do serwisu", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. włącza i wyłączą urządzenie", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. szuka pomocy w internecie", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 2:
            self.draw_text("Jak się nazywa słynny obrońca Częstochowy?", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. Zenon Martyniuk", self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Marcin Najman", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Tomasz Hajto", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Krzysztof Stanowski", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 3:
            self.draw_text('Kto jest wykonwcą utworu "Nie pytają Cię o imię,', self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text('walcząc z ostrym cieniem mgły?"', self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. Rychu Peja", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Bayer Full", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Norbi", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Andrzej Duda", self.screen, [WIDTH // 2, 350], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 4:
            self.draw_text("Przez jaki kolor oczu podmiot liryczny oszalał", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("w piosence Zenona Martyniuka?", self.screen,
                           [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. Czarne", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Niebiskie", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Zielone", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Oliwkowe", self.screen, [WIDTH // 2, 350], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 5:
            self.draw_text("W którym roku odbyła się Bitwa pod Grunwaldem?", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. 1410", self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. 1140", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. 1401", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. 1411", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 6:
            self.draw_text("Jak nazywa się stolica Autralii?", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. Oslo", self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Sydney", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Canberra", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Melbourne", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 7:
            self.draw_text("Jaki jest wynik równania 2+2x2?", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. 8", self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. 10", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. 4", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. 6", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 8:
            self.draw_text("Czym był Potop Szwedzki?", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. Powieść Henryka Sienkiewicza", self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Szereg wojen prowadzonych przez Szwecję", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("o dominacje nad morzem Bałtyckim", self.screen,
                           [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Wielka powódź w 1701 roku w Szwecji", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Promocje w sklepie IKEA", self.screen, [WIDTH // 2, 350], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 9:
            self.draw_text("Jak potocznie w piłce nożnej mówi się na", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text(
                "zachowanie zawodnika drużyny przeciwnej,",
                self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                centered=True)
            self.draw_text(
                "który przecina linie obrony w momencie podania?",
                self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                centered=True)
            self.draw_text("1. Rzut rożny", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Kiks", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Spalony", self.screen, [WIDTH // 2, 350], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Arsenal", self.screen, [WIDTH // 2, 400], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 10:
            self.draw_text("Jak nazywa się łańcuch górski", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("oddzielający Europe od Azji?", self.screen, [WIDTH // 2, 150],
                           26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. Andy", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Ural", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Tatry", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Alpy", self.screen, [WIDTH // 2, 350], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 11:
            self.draw_text("Jakie jest ulubione miejsce coczwartkowych,", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("krakowskich spotkań studentów?", self.screen,
                           [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. Rynek", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Plaża pod Mostem Poniatowskiego", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Miasteczko Studenckie AGH", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Wyspa słodowa", self.screen, [WIDTH // 2, 350], 26, BLACK, "impact",
                           centered=True)
        elif self.question == 12:
            self.draw_text("Kim jest Marcin Najman?", self.screen, [WIDTH // 2, 100], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("1. Najlepszym przyjacielem Stanowskiego", self.screen, [WIDTH // 2, 150], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("2. Sportowcem", self.screen, [WIDTH // 2, 200], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("3. Ekspertem w TVP", self.screen, [WIDTH // 2, 250], 26, BLACK, "impact",
                           centered=True)
            self.draw_text("4. Wszystkie odpowiedzi są poprawne", self.screen, [WIDTH // 2, 300], 26, BLACK, "impact",
                           centered=True)
        pygame.display.update()
