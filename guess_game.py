def guess_the_number():
    """A simple number guessing game with a fixed number."""
    print("Hello! What is your name?")
    name = input()

    secret_number = 10  
    print(f"\nWell, {name}, I am thinking of a number between 1 and 20.")

    guess_count = 0

    while True:
        print("Take a guess.")
        guess = int(input()) 
        guess_count += 1

        if guess < secret_number:
            print("\nYour guess is too low.")
        elif guess > secret_number:
            print("\nYour guess is too high.")
        else:
            print(f"\nGood job, {name}! You guessed my number in {guess_count} guesses!")
            break  
