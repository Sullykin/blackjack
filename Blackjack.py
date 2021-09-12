import pygame
import random
import time
import sys
import os

# Blackjack
# Dealer hits all soft 17s

pygame.font.init()
WHITE = (255,255,255)
BLACK = (0,0,0)
FONT = pygame.font.Font('Assets\\ror.ttf', 20)

class Blackjack:
    def __init__(self):
        self.suits = ['Clubs', 'Hearts', 'Diamonds', 'Spades']
        self.names = ['Jack', 'Queen', 'King']
        self.chips = {'green': 5, 'blue': 10, 'red': 50, 'black': 100}
        self.balance = 1000
        self.playing = False
        # init pygame
        pygame.mixer.pre_init(44100, -16, 1, 512) # reduces audio latency
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 900))
        self.clock = pygame.time.Clock()
        # cache assets
        #images = {str(i)[:-4]:pygame.image.load("images/"+i) for i in os.listdir("images") if os.path.isfile("images/"+i)}

    def main_menu(self):
        # create representation of user's balance with a random
        # amount of each denomination
        '''
        temp_bal = self.balance
        player_chips = []
        while temp_bal > 0:
            chip = self.chips[random.randint(1, 4)-1]
            if not self.chips[chip] > temp_bal:
                player_chips.append()
                temp_bal -= self.chips[chip]
        '''
        self.buttons = [Button(1500/2-100, 750, 200, 75, 'Play')]
        while not self.playing:
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                quit_attempt = False
                if event.type == pygame.QUIT:
                    quit_attempt = True
                # keydown events
                elif event.type == pygame.KEYDOWN:
                    alt_pressed = pressed_keys[pygame.K_LALT] or \
                                    pressed_keys[pygame.K_RALT]
                    # alt + f4
                    if event.key == pygame.K_F4 and alt_pressed:
                        quit_attempt = True
                if quit_attempt:
                    pygame.quit()
                    sys.exit()

                for button in self.buttons:
                    button.update(event)
 
            self.screen.fill((0,100,0))
            self.screen.blit(get_image('Assets/Cards/cardBack_red2.png'), (100, 600))
            for button in self.buttons:
                button.draw()
            pygame.display.flip()
            self.clock.tick(60)       

    def play(self):
        while self.playing:
            self.box = InputBox(330, 860, 75, 30)
            self.buttons = [Button(410, 800, 150, 30, 'Hit'), Button(580, 800, 150, 30, 'Stand'),
                            Button(750, 800, 150, 30, 'Double Down'), Button(920, 800, 150, 30, 'Surrender')]
            self.stand = False
            self.hole_card = True
            self.over = False
            self.bet = None
            self.framecount = 0
            self.userHand_sum = 0
            self.dealerHand_sum = 0
            self.user_ace = 0
            self.dealer_ace = 0
            self.userHand = []
            self.dealerHand = []
            self.deck = []
            self.animation = ''
            self.gameover_text = ''
            frame = 0 # animation frame var
            while not self.over: # Game
                # Wait for bet
                # Shuffle
                # Deal
                # Check for blackjacks
                # Wait for valid user action
                # Check bust/blackjack
                # Repeat until game over or stand
                # AI reveals hole card
                # AI does action every 3 seconds
                # Repeat until hand >= 17
                # Compare hands
                # game over screen
                pressed_keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    check_universal_events(event, pressed_keys)
                    for button in self.buttons:
                        button.update(event)
                    self.box.handle_event(event)

                if self.stand and self.framecount % 180 == 0:
                    if self.dealerHand_sum < 17:
                        card = self.deck.pop()
                        self.dealerHand.append(card)
                        if card[0] == 1:
                            self.dealer_ace += 1
                        self.dealerHand_sum += self.dealerHand[-1][0]
                    elif self.dealerHand_sum >= 17 or (self.dealerHand_sum == 11 and self.dealer_ace):
                        if self.dealerHand_sum > 21 or self.userHand_sum > self.dealerHand_sum:
                            self.balance += self.bet
                            self.gameover(f'You won ${self.bet}!')
                        elif self.userHand_sum == self.dealerHand_sum:
                            self.gameover('You push.')
                        else:
                            self.balance -= self.bet
                            self.gameover(f'You lost ${self.bet}.')

                self.screen.fill((0,100,0))
                pygame.draw.rect(self.screen, 0, (0, 850, 1500, 50))
                if self.stand or not self.dealerHand:
                    dealerHand_sum = self.dealerHand_sum
                elif self.dealerHand:
                    dealerHand_sum = self.dealerHand_sum - self.dealerHand[1][0] 
                drawText(f'Dealer\'s hand: {dealerHand_sum}', 20, 1500//2+100, 875, center=True)
                drawText(f'Your hand: {self.userHand_sum}', 20, 1500//2-100, 875, center=True)
                drawText(f'Balance: {self.balance}', 20, 10, 865)
                for i, card in enumerate(self.userHand):
                    filename = f'card{card[2]}{card[1]}'
                    self.screen.blit(get_image(f'Assets/Cards/{filename}.png'), ((i*150)+(1920//2-150-215), 580))
                for i, card in enumerate(self.dealerHand):
                    filename = f'card{card[2]}{card[1]}'
                    if i == 1 and not self.stand:
                        self.screen.blit(get_image(f'Assets/Cards/cardBack_red2.png'), ((i*150)+(1920//2-150-215), 50))
                    else:
                        self.screen.blit(get_image(f'Assets/Cards/{filename}.png'), ((i*150)+(1920//2-150-215), 50))
                for x in range(len(self.deck)//2):
                    self.screen.blit(get_image('Assets/Cards/cardBack_red2.png'), (300-(x*2), 50-x))
                if self.animation:
                    frame += 1
                    if self.animation == 'hit':
                        pass
                    elif self.animation == 'double down':
                        pass
                    if frame == 60:
                        self.animation = ''
                    if not self.animation and self.gameover_text:
                        self.gameover(self.gameover_text)
                for button in self.buttons:
                    button.draw()
                drawText('Bet: ', 20, 280, 865)
                if self.bet:
                    drawText(str(self.bet), 20, 330, 865)
                else:
                    self.box.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(60)
                self.framecount += 1

    def gameover(self, gameover_text):
        self.over = True
        self.endscreen = True
        buttons = [Button(1500//2-170, 500, 150, 50, 'New Game'),
                   Button(1500//2, 500, 150, 50, 'Main Menu')]
        if 'won' in gameover_text:
            color = (0,255,100)
        elif 'push' in gameover_text:
            color = WHITE
        elif 'lost' in gameover_text:
            color = (255,0,0)
        while self.endscreen:
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                check_universal_events(event, pressed_keys)
                for button in buttons:
                    button.update(event)

            drawText(gameover_text, 75, 1500//2, 350, center=True, color=color, fontfile='freesansbold.ttf')
            for button in buttons:
                button.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def shuffle_deck(self):
        self.deck = []
        for suit in self.suits:
            for num in range(14):
                if num == 0:
                    continue
                name = num
                if num > 10:
                    name = self.names[num-11]
                    num = 10
                elif num < 2:
                    name = 'Ace'
                card = (num, name, suit)
                self.deck.append(card)
        random.shuffle(self.deck)

    def deal_hands(self):
        # Deal out hands
        self.dealerHand = [self.deck.pop(), self.deck.pop()]
        self.userHand = [self.deck.pop(), self.deck.pop()]
        #if user gets an ace
        for card in self.userHand:
            if card[0] == 1:
                self.user_ace += 1
        self.dealerHand_sum = self.dealerHand[0][0] + self.dealerHand[1][0]
        self.userHand_sum = self.userHand[0][0] + self.userHand[1][0]
        if self.dealerHand_sum == 21:
            if self.userHand_sum == 21:
                self.gameover_text = 'You push.'
            else:
                self.balance -= (self.bet)
                self.gameover_text = f'You lost ${self.bet}.'
        elif self.userHand_sum == 21 or (self.userHand_sum == 11 and self.user_ace):
            self.balance += (self.bet*1.5)
            self.gameover_text = f'You won ${self.bet*1.5}0!'

    def hit(self):
        card = self.deck.pop()
        self.userHand.append(card)
        if card[0] == 1:
            self.user_ace += 1
        self.userHand_sum += self.userHand[-1][0]
        # Check bust
        if self.userHand_sum > 21:
            self.balance -= self.bet
            self.gameover_text = f'You lost ${self.bet}.'
        # Check blackjack
        elif self.userHand_sum == 21 or (self.userHand_sum == 11 and self.user_ace):
            self.balance += (self.bet*1.5)
            self.gameover_text = f'You won ${self.bet*1.5}0!'

    def double_down(self):
        self.bet *= 2
        self.stand = True
        card = self.deck.pop()
        self.userHand.append(card)
        if card[0] == 1:
            self.user_ace += 1
        self.userHand_sum += self.userHand[-1][0]
        if self.userHand_sum > 21 or (self.userHand_sum == 11 and self.user_ace == 1):
            self.balance -= self.bet
            self.gameover_text = f'You lost ${self.bet}.'


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (100,100,100)
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.cursor = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = WHITE if self.active else (100,100,100)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    try:
                        bet = int(self.text)
                        if bet <= game.balance:
                            game.bet = bet
                            game.shuffle_deck()
                            game.deal_hands()
                    except:
                        pass
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        game.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(game.screen, self.color, self.rect, 2)
        if game.framecount % 60 == 0:
            self.cursor = not self.cursor
        if self.active and self.cursor:
            pygame.draw.rect(game.screen, WHITE, (self.rect.x+self.txt_surface.get_width()+10, self.rect.y+7, 2, 18))


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, color=(255,255,255), textColor=(0)):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((x,y,w,h))
        self.text = text
        self.color = color
        self.textColor = textColor
        self.soundFlag = False
        self.showBorder = False

    def update(self, event):
        # update flags for glow and mouseover
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos[0], pos[1]):
            if self.soundFlag:
                play_sound('Assets\\mouseover.wav')
            self.soundFlag = False
            self.showBorder = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #play_sound('Assets\\select.wav')
                if self.text == 'Quit':
                    pygame.quit()
                    sys.exit()
                elif self.text == 'Play':
                    game.playing = True
                elif self.text == 'Hit':
                    if not game.stand:
                        game.animation = 'hit'
                        game.hit()
                elif self.text == 'Stand':
                    game.stand = True
                elif self.text == 'Double Down':
                    if game.bet*2 <= game.balance:
                        game.animation = 'double down'
                        game.double_down()
                elif self.text == 'Surrender':
                    game.balance -= self.bet/2
                    game.gameover(f'You lost ${game.bet/2}0.')
                elif self.text == 'Main menu':
                    game.playing = False
                    game.endscreen = False
                elif self.text == 'New Game':
                    game.endscreen = False
                    
        else:
            self.showBorder = False
            self.soundFlag = True

    def draw(self):
        if self.showBorder:
            pygame.draw.rect(game.screen, (140,0,20), (self.rect.x-3, self.rect.y-3, self.rect.w+6, self.rect.h+6), 5)
        pygame.draw.rect(game.screen, self.color, self.rect)
        drawText(self.text, 20, self.rect.x+(self.rect.w//2), self.rect.y+(self.rect.h//2), self.textColor, True)

def check_universal_events(event, pressed_keys):
    quit_attempt = False
    if event.type == pygame.QUIT:
        quit_attempt = True
    # keydown events
    elif event.type == pygame.KEYDOWN:
        alt_pressed = pressed_keys[pygame.K_LALT] or \
                        pressed_keys[pygame.K_RALT]
        # alt + f4
        if event.key == pygame.K_F4 and alt_pressed:
            quit_attempt = True
    if quit_attempt:
        pygame.quit()
        sys.exit()

def drawText(text, size, x, y, color=WHITE, center=False, fontfile="Assets/ror.ttf"):
    font = pygame.font.Font(fontfile, size)
    text = font.render(text, True, color)
    if center:
        game.screen.blit(text, (x - (text.get_width() // 2), y - (text.get_height() // 2)))
    else:
        game.screen.blit(text, (x, y))

_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play()

if __name__ == "__main__":
    game = Blackjack()
    while True:
        game.main_menu()
        game.play()
