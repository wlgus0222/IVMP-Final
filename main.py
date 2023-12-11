import pygame
import sys
import os

from tiles import beatarray

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (96,212,252)

POSITION_A = 187
POSITION_B = 258
POSITION_C = 329
POSITION_D = 400
POSITION_E = 471
POSITION_F = 542

SPEED = 3
VISUAL_LATENCY = 80

STRUM_POSITION = 500

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

strum = pygame.image.load('notestrum.png')

pressed = pygame.image.load('pressed.png')

pygame.display.set_caption('20201914 PLAYBEATS!!')

class Button():
    def __init__(self, pos, text_input, font, base_color, hover_color, file_name = None):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hover_color = base_color, hover_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.file_name = file_name

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hover_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def checkHover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

def main_menu():
    menu_text = pygame.font.Font("RetroGaming.ttf", 100).render("PLAYBEATS!!", True, WHITE)
    menu_rect = menu_text.get_rect(center=(400, 100))

    level1_button = Button(pos=(400, 250), text_input="Level 1", font=pygame.font.Font("RetroGaming.ttf", 60), base_color=BLUE, hover_color=WHITE)
    level2_button = Button(pos=(400, 400), text_input="Level 2", font=pygame.font.Font("RetroGaming.ttf", 60), base_color=BLUE, hover_color=WHITE)

    while True:
        screen.fill(BLACK)

        pos = pygame.mouse.get_pos()

        screen.blit(menu_text, menu_rect)

        level1_button.changeColor(pos)
        level1_button.update(screen)

        level2_button.changeColor(pos)
        level2_button.update(screen)
    
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if level1_button.checkForInput(pos):
                    initialize('easy', "AJourneyAwaits.mp3")
                elif level2_button.checkForInput(pos):
                    initialize('hard', "CyberpunkMoonlightSonata.mp3")
                    

        pygame.display.update()


class Note(pygame.sprite.Sprite):
    def __init__(self, identity, strumTime, position):
        pygame.sprite.Sprite.__init__(self)
        self.idnum = identity
        self.strum = strumTime
        self.miss = False
        self.hit = False
        self.difference = -2000000
        if position == 1:
            self.image = pygame.image.load('noteA.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(POSITION_A, -100)
        if position == 2:
            self.image = pygame.image.load('noteB.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(POSITION_B, -100)
        if position == 3:
            self.image = pygame.image.load('noteC.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(POSITION_C, -100)
        if position == 4:
            self.image = pygame.image.load('noteC.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(POSITION_D, -100)
        if position == 5:
            self.image = pygame.image.load('noteB.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(POSITION_E, -100)
        if position == 6:
            self.image = pygame.image.load('noteA.png')
            self.rect = self.image.get_rect()
            self.rect.move_ip(POSITION_F, -100)

    def update(self, pressed, time):

        if self.hit or self.miss:
            self.kill()

        if not self.hit and not self.miss and self.rect.centery > 520:
            self.miss = True
            self.difference = -1000000

        if self.rect.centery > 480 and not self.miss and pressed:
            if not self.hit:
                pressed = False
                self.difference = self.strum - time

            self.hit = True

    def move(self, shift):
        if shift > 0:
            self.rect.centery = shift

def combo_count(amount):
    font = pygame.font.Font("RetroGaming.ttf", 40)
    text = font.render( f"Combo: {amount}", True, WHITE)
    screen.blit(text, (20, 20))

def score_count(score_amount):
    font = pygame.font.Font("RetroGaming.ttf", 40)
    text = font.render(f"{score_amount}", True, WHITE)
    screen.blit(text, (630, 20))

def initialize(difficulty, audio_file_name):
    try:
        beatmap, ending_time = beatarray(audio_file_name, difficulty)
    except:
        print('Unable to read audio file')
        main_menu()

    game_loop(audio_file_name, beatmap, ending_time)

def game_loop(file_name, beatmap, ending_time):
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.set_volume(0.7)

    combo = 0
    score = 0

    keypressA = False
    keypressS = False
    keypressD = False
    keypressJ = False
    keypressK = False
    keypressL = False

    notesA = pygame.sprite.Group()
    notesB = pygame.sprite.Group()
    notesC = pygame.sprite.Group()
    notesD = pygame.sprite.Group()
    notesE = pygame.sprite.Group()
    notesF = pygame.sprite.Group()

    note_dict = {
        1: notesA.add,
        2: notesB.add,
        3: notesC.add,
        4: notesD.add,
        5: notesE.add,
        6: notesF.add,
    }

    for idx, beat in enumerate(beatmap):
        timing = beat['time']
        position = beat['position']
        note_dict[position](Note(idx, timing, position))


    current = 0
    previousframetime = 0
    lastplayheadposition = 0
    mostaccurate = 0

    pygame.mixer.music.play()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                press_sound = pygame.mixer.Sound('beat.ogg')
                press_sound.play()
                if event.key == pygame.K_a:
                    keypressA = True
                if event.key == pygame.K_s:
                    keypressS = True
                if event.key == pygame.K_d:
                    keypressD = True
                if event.key == pygame.K_j:
                    keypressJ = True
                if event.key == pygame.K_k:
                    keypressK = True
                if event.key == pygame.K_l:
                    keypressL = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    keypressA = False
                if event.key == pygame.K_s:
                    keypressS = False
                if event.key == pygame.K_d:
                    keypressD = False
                if event.key == pygame.K_j:
                    keypressJ = False
                if event.key == pygame.K_k:
                    keypressK = False
                if event.key == pygame.K_l:
                    keypressL = False

        current += clock.get_time()

        if current >= ending_time:
            pygame.mixer.music.unload()
            main_menu()

        mostaccurate += current - previousframetime
        previousframetime = current
        songtime = pygame.mixer.music.get_pos()
        if songtime != lastplayheadposition:
            mostaccurate = (mostaccurate + songtime)/2
            lastplayheadposition = songtime

        screen.fill(BLACK)
        combo_count(combo)
        score_count(score)

        if keypressA:
            screen.blit(pressed, (POSITION_A, 474))
        if keypressS:
            screen.blit(pressed, (POSITION_B, 474))
        if keypressD:
            screen.blit(pressed, (POSITION_C, 474))
        if keypressJ:
            screen.blit(pressed, (POSITION_D, 474))
        if keypressK:
            screen.blit(pressed, (POSITION_E, 474))
        if keypressL:
            screen.blit(pressed, (POSITION_F, 474))

        notesA.draw(screen)
        notesB.draw(screen)
        notesC.draw(screen)
        notesD.draw(screen)
        notesE.draw(screen)
        notesF.draw(screen)

        screen.blit(strum, (0, 0))

        for note in notesA:
            distance = STRUM_POSITION - (note.strum/SPEED - mostaccurate/SPEED) + VISUAL_LATENCY
            note.move(distance)
            statusa = note.difference
            if -500 <= statusa <= 500:
                combo += 1
                score += 100
            elif statusa == -1000000:
                combo = 0

        for note in notesB:
            distances = STRUM_POSITION - (note.strum/SPEED - mostaccurate/SPEED) + VISUAL_LATENCY
            note.move(distances)
            statusb = note.difference
            if -500 <= statusb <= 500:
                combo += 1
                score += 100
            elif statusb == -1000000:
                combo = 0

        for note in notesC:
            distance = STRUM_POSITION - (note.strum/SPEED - mostaccurate/SPEED) + VISUAL_LATENCY
            note.move(distance)
            statusc = note.difference
            if -500 <= statusc <= 500:
                combo += 1
                score += 100
            elif statusc == -1000000:
                combo = 0

        for note in notesD:
            distance = STRUM_POSITION - (note.strum/SPEED - mostaccurate/SPEED) + VISUAL_LATENCY
            note.move(distance)
            statusd = note.difference
            if -500 <= statusd <= 500:
                combo += 1
                score += 100
            elif statusd == -1000000:
                combo = 0

        for note in notesE:
            distance = STRUM_POSITION - (note.strum/SPEED - mostaccurate/SPEED) + VISUAL_LATENCY
            note.move(distance)
            statuse = note.difference
            if -500 <= statuse <= 500:
                combo += 1
                score += 100
            elif statuse == -1000000:
                combo = 0

        for note in notesF:
            distance = STRUM_POSITION - (note.strum/SPEED - mostaccurate/SPEED) + VISUAL_LATENCY
            note.move(distance)
            statusf = note.difference
            if -500 <= statusf <= 500:
                combo += 1
                score += 100
            elif statusf == -1000000:
                combo = 0

        notesA.update(keypressA, mostaccurate)
        notesB.update(keypressS, mostaccurate)
        notesC.update(keypressD, mostaccurate)
        notesD.update(keypressJ, mostaccurate)
        notesE.update(keypressK, mostaccurate)
        notesF.update(keypressL, mostaccurate)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main_menu()
