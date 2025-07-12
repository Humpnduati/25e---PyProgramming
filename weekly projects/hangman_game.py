import random

hang = ["""
H A N G M A N - UCL

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
H A N G M A N - UCL

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


def get_random_word():
    champions_league_winners = ['Manutd', 'Milan', 'Barca', 'Madrid', 'Bayern', 'AJAX', 'Juve', 'Liverpool', 'PSG',
                               'Chelsea', 'Mancity']
    word = random.choice(champions_league_winners)
    return word.lower()  # Convert to lowercase for consistency


def display_board(hang, missed_letters, correct_letters, secret_word):
    print(hang[len(missed_letters)])  # Fixed: use hang instead of 'hang'
    print()

    print('Missed Letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print("\n")

    blanks = '_' * len(secret_word)

    for i in range(len(secret_word)):
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]

    for letter in blanks:
        print(letter, end=' ')
    print("\n")


def get_guess(already_guessed):
    while True:
        guess = input('Guess a letter: ').lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif not guess.isalpha():
            print('Please enter a LETTER.')
        else:
            return guess


def play_again():
    return input("\nDo you want to play again? ").lower().startswith('y')


print("H A N G M A N - UCL EDITION")
missed_letters = ''
correct_letters = ''
secret_word = get_random_word()
game_is_done = False

while True:
    display_board(hang, missed_letters, correct_letters, secret_word)

    # Let the player enter a letter
    guess = get_guess(missed_letters + correct_letters)

    if guess in secret_word:
        correct_letters = correct_letters + guess

        # Check if player has won
        found_all_letters = True
        for i in range(len(secret_word)):
            if secret_word[i] not in correct_letters:
                found_all_letters = False
                break
        if found_all_letters:
            print('\nYes! The secret word is "' +
                  secret_word + '"! You have won!')
            game_is_done = True
    else:
        missed_letters = missed_letters + guess

        # Check if player has guessed too many times and lost
        if len(missed_letters) == len(hang) - 1:
            display_board(hang, missed_letters,
                         correct_letters, secret_word)
            print('YOU LOST!\nAfter ' + str(len(missed_letters)) + ' missed guesses and ' +
                  str(len(correct_letters)) + ' correct guesses. Better luck next time!')
            print(f'The secret word was revealed to be: "{secret_word}"')
            game_is_done = True

    # Ask the player if they want to play again (only if the game is done)
    if game_is_done:
        if play_again():
            missed_letters = ''
            correct_letters = ''
            game_is_done = False
            secret_word = get_random_word()
        else:
            break