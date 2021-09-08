# Blackjack
# Dealer hits all soft 17s
import random, time

numbers = [1,2,3,4,5,6,7,8,9,10,10,10,10]
suits = ['Clubs', 'Hearts', 'Diamonds', 'Spades']
extra = ['King', 'Queen', 'Jack', '10']
def genCard():
    num1 = random.choice(numbers)
    if num1 == 10:
        cardnum = random.choice(extra)
    elif num1 == 1:
        cardnum = 'Ace'
    elif num1 <= 10:
        cardnum = str(num1)

    card = cardnum + ' of ' + random.choice(suits)
    return (num1, card)

def check():
    global balance
    global playCount
    # after deal
    if playCount == 1:
        if dealerHand == 21:
            if userHand == 21:
                print('Dealer also got blackjack.')
                push()
                return True
            else:
                print('Dealer got blackjack.')
                lose()
                return True
        if userHand == 21:
            print('\nYou win $' + str(float(bet*1.5))+ '!\n\n')
            balance = float(balance + (bet*1.5))
            return True
    # after every user play
    if userHand > 21:
        lose()
        return True
    # after user and AI are done
    if (stand == True) and (AIdone == True):
        if dealerHand > 21:
            win()
            return True
        if userHand > dealerHand:
            win()
            return True
        elif userHand == dealerHand:
            push()
            return True
        else:
            lose()
            return True
    # user surrenders
    if surrender == True:
        print('\nYou lose.\n\n')
        balance = float(balance - (bet/2))
        return True

def win():
    global balance
    print('\nYou win $' + str(bet)+ '!\n\n')
    balance = balance + bet
    return

def push():
    print('\nYou push.\n\n')
    return

def lose():
    global balance
    print('\nYou lose.\n\n')
    balance = balance - bet
    return
        
balance = 100
done = False
while not done: # Session
    playCount = 0
    stand = False
    surrender = False
    # Place bet
    bet = 0
    print('Balance: $' + str(balance))
    while True:
        try:
            bet = int(input('Bet: '))
            if (bet > balance) or (bet < 5):
                print('That is not a valid bet.\n')
            else:
                break
        except ValueError:
            print('That is not a valid bet.\n')
    allCards = []
    print('A bet of $' + str(bet) + ' has been placed.\n\n')

    # Deal out hands
    for i in range(4): # 0 & 1 are dealer
        cardData = genCard()
        allCards.append(cardData)
    dealerHand = allCards[0][0] + allCards[0][0]
    userHand = allCards[2][0] + allCards[3][0]
    print('Dealer\'s hand: ' + allCards[0][1] + ' and [HOLE CARD]')
    print('Known hand value: ' + str(dealerHand - allCards[0][0]) + '\n')
    print('Your hand: ' + allCards[2][1] + ' and ' + allCards[3][1])
    #if user gets an ace
    if (allCards[2][0] == 1) or (allCards[3][0] == 1):
        while True:
            aceChoice = input('You got an ace. Do you want it to be worth 1 or 11? ')
            if aceChoice == '11':
                userHand += 10
                break
            elif aceChoice == '1':
                break
            else:
                print('Invalid value.')
    print('Hand value: ' + str(userHand))
    over = check()

    # Main play
    over = False
    AIdone = False
    while not over: # Round
        if userHand == 21:
            break
        print('\n\n[1] Hit\n[2] Stand\n[3] Double down\n[4] Surrender')
        option = input('What would you like to do? ')
        if option == '1':
            newCard = genCard()
            userHand += newCard[0]
            if newCard[0] == 1:
                while True:
                    aceChoice = input('You got an ace. Do you want it to be worth 1 or 11? ')
                    if aceChoice == '11':
                        userHand += 10
                        break
                    elif aceChoice == '1':
                        break
                    else:
                        print('Invalid value.')
            print('\n' + str(newCard[1]))
            print('New hand value: ' + str(userHand))
        elif option == '2':
            stand = True
        elif option == '3':
            if bet*2 <= balance:
                print('Your bet has been doubled to $' + str(bet*2))
                bet = bet*2
                stand = True
                newCard = genCard()
                userHand += newCard[0]
                if newCard[0] == 1:
                    while True:
                        aceChoice = input('You got an ace. Do you want it to be worth 1 or 11? ')
                        if aceChoice == '11':
                            userHand += 10
                            break
                        elif aceChoice == '1':
                            break
                        else:
                            print('Invalid value.')
                print('\n' + str(newCard[1]))
                print('New hand value: ' + str(userHand))
            else:
                print('\nYou do not have enough money to double down.')
        elif option == '4':
            surrender = True
        else:
            print('That is not a valid option.')
        if (stand == True):
            if over:
                break
            print('\n\nDealer\'s hole card is: ' + allCards[0][1])
            print('New hand value: ' + str(dealerHand))
            while dealerHand < 17:
                time.sleep(3)
                newCard = genCard()
                dealerHand += newCard[0]
                if (newCard[0] == 1) and (dealerHand <= 10):
                    dealerHand += 10
                print('\nDealer draws a card.\n' + str(newCard[1]))
                print('New hand value: ' + str(dealerHand))
            AIdone = True
            time.sleep(3)
        playCount += 1
        over = check()
        
    if balance <= 0:
        print('\nYou have no money left.')
        done = True
