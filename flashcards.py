import pickle
import time
import fileinput
import os

# Initialize variables
active_reviews = 0

# Clean console
clear = lambda: os.system('cls') or None

# Load flashcards and their history
try:
    flashcards = pickle.load(open("flashcards.pickle", "rb"))
    flashcards_history = pickle.load(open("flashcards_history.pickle", "rb"))
# If failed create new dictionaries
except (OSError, IOError) as e:
    flashcards = []
    flashcards_history = []

# Levels of your Flashcards and their intervals
# Apprentice: 0, 3h, 6h, 1d | Guru: 3d, 7d | Master: 2w | Burned: 30d
levels = {"Apprentice_Lvl_0": 0,"Apprentice_Lvl_1": 10800, "Apprentice_Lvl_2": 21600, "Apprentice_Lvl_3": 86400,
          "Guru_Lvl_1": 259200, "Guru_Lvl_2": 864000, "Master": 1209600, "Burned": 2592000}

# Convert level number to level name
x_to_level_name = ["Apprentice_Lvl_0", "Apprentice_Lvl_1", "Apprentice_Lvl_2","Apprentice_Lvl_3",
          "Guru_Lvl_1", "Guru_Lvl_2", "Master", "Burned"]

# Check if flashcards are ready for reviews
def check_reviews():
    active_counter = 0
    for i, card_info in enumerate(flashcards_history):
        if(card_info["review_ready"]):
            active_counter += 1
            continue
        else:
            level = card_info["level"]
            last_review_time = card_info["last_review_time"]
            # If burned, don't use
            if(level == 7): continue
            # get the time required for the card to be ready for review
            interval_on_that_lvl = levels[x_to_level_name[level]]
            # check if ready
            if(current_time() - last_review_time >= interval_on_that_lvl):
                card_info["review_ready"] = True
                active_counter  += 1
    return active_counter


def current_time():
    return int(round(time.time()))

def save():
    pickle.dump( flashcards, open( "flashcards.pickle", "wb" ) )
    pickle.dump( flashcards_history, open( "flashcards_history.pickle", "wb" ) )

# Choose menu option
def choose_option():
    for line in fileinput.input():
        # convert string to int and return
        try:
            fileinput.close()
            return int(line)

        except ValueError:
            print("Please choose again.")


# Menu Options
def review_flashcards():
    def check_if_correct(card_info):
        print("Press 1 if correct and anything else if not:")
        line = input()

        # convert string to int and return
        if (line == "1"):
            if(card_info["level"] <= 6): card_info["level"] += 1
            card_info["last_review_time"] = current_time()
            card_info["review_ready"] = False

            return card_info
        else:
            if(card_info["level"] > 0):
                card_info["level"] -= 1
            return card_info

    # Iterate through review-ready flashcards
    for i, card_info in enumerate(flashcards_history):
        clear()
        if(card_info["review_ready"]):
            print("Level: ", x_to_level_name[card_info["level"]])
            card = flashcards[i]
            print("\nQuestion: ", card["question"])
            input(": ")
            print("\nAnswer: ", card["answer"])
            card_info = check_if_correct(card_info)
            clear()
        save()

def add_flashcards():
    clear()
    flashcard = {}
    flashcard_history = {"creation_date": current_time(), "level": 0, "last_review_time": current_time(), "review_ready": True}

    print("Write a question:")
    line = input()
    flashcard["question"] = line

    print("\nWrite an answer:")

    line = input()
    flashcard["answer"] = line

    # Save flashcards
    flashcards.append(flashcard)
    flashcards_history.append(flashcard_history)
    save()

def print_instruction():
    with open("instruction.txt", 'r') as f:
        instruction = f.read()
        print(instruction)
        input()



def main():
    while True:
        clear()

        # Check which flashcards are review-ready
        active_reviews = check_reviews()

        print("Avaliable reviews: ", active_reviews)
        print("Choose an option:")
        print("1: Review  2: Add flashcards  3: Instruction  4: Exit")
        option = choose_option()
        if(option == 1):
            review_flashcards()

        elif(option == 2):
            add_flashcards()

        elif(option == 3):
            print_instruction()

        elif(option == 4):
            break

# Run program
main()
