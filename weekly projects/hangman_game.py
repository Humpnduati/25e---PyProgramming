import random

hang = ["""

H A N G M A N -UCL

  +---+
  |   |
  O   |
      |
      |
      |
=========""", """
H A N G M A N - UCL

  +---+
  |   |
  O   |
  |   |
      |
      |
=========""", """
H A N G M A N -UCL 

  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""", """
H A N G M A N - UCL

  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""", """
H A N G M A N - UCL

  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""", """
H A N G M A N - UCL

  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
========="""]


def getRandomWord():
    champions_league_winners = ['Manutd', 'Milan', 'Barca', 'Madrid', 'Bayern', 'AJAX', 'Juve', 'Livepool', 'PSG',
                                'Chelsea', 'Mancity']

    word = random.choice(champions_league_winners)
    return word


def displayBoard(hang, missedLetters, correctLetters, secretWord):
    print(hang[len(missedLetters)])
    print()

    print('Missed Letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print("\n")

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)):  # replace blanks with correctly guessed letters
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i + 1:]

    for letter in blanks:  # show the secret word with spaces in between each letter
        print(letter, end=' ')
    print("\n")


def getGuess(alreadyGuessed):
    while True:
        guess = input('Guess a letter: ')
        guess = guess.lower()
        try:
            if len(guess) != 1:
                print('Please enter a single letter.')
            elif guess in AttemptFailed:
                print('Attempt Failed. Choose again.')

            else:
                return guess
                continue
        except ValueError:
            return guess


def playAgain():
    return input("\nDo you want to play again? ").lower().startswith('y')


missedLetters = ''
correctLetters = ''
secretWord = getRandomWord()
gameIsDone = False

while True:
    displayBoard(hang, missedLetters, correctLetters, secretWord)

    guess = getGuess(missedLetters + correctLetters)

    try:

        if guess in secretWord:
            correctLetters = correctLetters + guess

            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print('\nYes! The secret word is "' +
                      secretWord + '"! You have won!')
                gameIsDone = True
        else:
            missedLetters = missedLetters + guess

            if len(missedLetters) == len(hang) - 1:
                displayBoard(hang, missedLetters,
                             correctLetters, secretWord)
                print('YOU LOST!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' +
                      str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                gameIsDone = True

    except:

        if gameIsDone:
            if playAgain():
                missedLetters = ''
                correctLetters = ''
                gameIsDone = False
                secretWord = getRandomWord()
            else:
                break