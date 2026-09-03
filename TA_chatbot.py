"""
Task List:

2 - Write the ReadME file according to the requirements
3 - Review all the code and ensure everything is up to par
4 - Write future features / plans for the readme!

"""

import sys
import time
import os
import random
import threading
import msvcrt
import platform
import requests
import json
from operator import contains
from pynput import keyboard
from math import ceil,floor

"""GLOBAL VARIABLES"""

# Responses dictionary & its keys
responses = {
    # Matching any of the variations of "hello"
    "hellovar": [
        ["Hey, What can I assist you with?", 1],
        ["Hello there! How can I help you today?", 1],
        ["Greetings! What can I do for you?", 1],
        ["Hi! How's it going?", 1]
    ],
    
    # Matching any of the variations of "how are you?"
    "howruvar": [
        ["I am doing good! How about you?", 1],
        ["I'm doing great, thanks for asking! What about you?", 1],
        ["I'm feeling fantastic! What can I help you with today?", 1],
        ["I'm all systems go! How are you doing?", 1]
    ],
    
    # Matching any of the variations of "what's 2+2?"
    "2+2": [
        ["5 (they hid a 1)", 1],
        ["The answer is 5. Just trust me on this.", 1],
        ["Well, you see... 2+2 is secretly 5.", 1],
        ["It's 4, but I like to joke around and say 5!", 1]
    ],
    
    # Matching any of the variations of "bazinga"
    "sheldonvar": [
        ["Soft kitty, \nwarm kitty, \nlittle ball of fur. \nHappy kitty, \nsleepy kitty, \npurr, \npurr, \npurr.", 0.1],
        ["That's My Spot.", 1],
        ["Bazinga! You got me good!", 1],
        ["Gotcha! Bazinga!", 1],
        ["Scissors cuts Paper \nPaper covers Rock \nRock crushes Lizard \nLizard poisons Spock \nSpock smashes Scissors \nScissors decapitates Lizard \nLizard eats Paper \nPaper disproves Spock \nSpock vaporizes Rock \n(and as it always has) Rock crushes Scissors", 1]
    ],
    
    # Matching any of the variations of "how's the weather?"
    "weathervar": [
        ["It's sunny and bright outside!", 1],
        ["The forecast says it might rain later today.", 1],
        ["It's cloudy with a chance of me telling a joke!", 1],
        ["The weather is perfect for a walk.", 1]
    ],
    
    # Matching any of the variations of "tell me a joke"
    "jokevar": [
        ["Why don't skeletons fight each other? They don't have the guts.", 1],
        ["Why did the scarecrow win an award? Because he was outstanding in his field!", 1],
        ["Why don’t eggs tell jokes? Because they might crack up.", 1],
        ["What do you call fake spaghetti? An impasta!", 1]
    ],
    
    # Matching any of the variations of "tell me something interesting"
    "factvar": [
        ["Did you know that octopuses have three hearts?", 1],
        ["Honey never spoils. Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!", 1],
        ["A day on Venus is longer than a year on Venus. It's true!", 1],
        ["Sharks have been around longer than trees—about 400 million years!", 1]
    ],
    
    # Matching any of the variations of "thanks"
    "thanksvar": [
        ["You're welcome! Glad I could help.", 1],
        ["Anytime! I'm here whenever you need me.", 1],
        ["No problem, happy to assist!", 1],
        ["You're very welcome!", 1]
    ],
    
    # Matching any of the variations of "sorry"
    "sorryvar": [
        ["No worries! It's all good.", 1],
        ["Don't worry about it, everything's fine.", 1],
        ["It's okay, no harm done!", 1],
        ["No need to apologize, it's all good.", 1]
    ]
}

keys = {
    "hellovar": (["hello", 1], ["hi", 1], ["hey", 1], ["greetings", 3]),
    "howruvar": (["how", 1], ["doing", 3], ["how's", 1], ["going", 3], ["you", 2], ["do", 1]),
    "2+2": (["what's", 1], ["2 plus 2", 5], ["2+2", 5]),
    "sheldonvar":(["bazinga", 10], ["moonpie", 3], ["sheldon", 4], ["cooper", 4], ["amy", 3]),
    "weathervar":(["weather", 5], ["how's", 1], ["how is", 1], ["update", 2]),
    "jokevar":(["tell", 1], ["joke", 3], ["make", 1], ["laugh", 4]),
    "factvar": (["tell", 1], ["me", 1], ["something", 2], ["interesting", 3], ["cool", 2], ["fact", 5]),
    "thanksvar": (["thanks", 3], ["thank", 3], ["you", 1], ["appreciate", 2]),
    "sorryvar": (["sorry", 3], ["my bad", 2], ["oops", 2], ["apologies", 3]),
    "settings": (["settings", 50], ["options", 30]),
    "apod":(["apod", 50], ["astronomy", 10], ["picture", 2], ["day", 2]),
    "cls":(["cls", 50], ["clear", 5]),
    "exit":(["exit", 10], ["bye", 6], ["goodbye", 10], ["leave", 3])
}

nonkey_wordlist = [
    # Articles & Determiners
    "a", "an", "the", "this", "that", "these", "those",
    "my", "your", "his", "her", "its", "our", "their", "whose",
    "all", "any", "both", "each", "either", "every", "few", 
    "many", "more", "most", "much", "neither", "no", "several", "some",
    
    # Prepositions
    "about", "above", "across", "after", "against", "along", "among", 
    "around", "at", "before", "behind", "below", "beneath", "beside", 
    "between", "beyond", "by", "down", "during", "for", "from", "in", 
    "inside", "into", "near", "of", "off", "on", "onto", "out", 
    "outside", "over", "through", "to", "toward", "under", "until", 
    "up", "upon", "with", "within", "without",
    
    # Conjunctions
    "and", "but", "or", "nor", "so", "yet", "for",
    "although", "because", "if", "since", "unless", "until", "while",
    
    # Pronouns
    "i", "me", "we", "us", "you", "he", "him", "she", "her", 
    "it", "they", "them", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves",
    
    # Auxiliary & Modal Verbs
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did",
    "can", "could", "will", "would", "shall", "should", "may", "might", "must"
]

# Internal functionality variables
skipCheck=[False]

# Changeable variables 
api_key = "DEMO_KEY"
textSpeed = 0.045
user_name = os.environ.get("USERNAME")

"""MISC. FUNCTIONS"""

# Discards any buffered keystrokes (e.g. the Enter used to skip animation).
def flush_input():
    while msvcrt.kbhit():
        msvcrt.getch()


"""PRINT RELATED FUNCTIONS"""

# Listener function to check for enter key press, skipping text animation
def t_onpress_print(key): 
    global skipCheck
    if key == keyboard.Key.enter: 
        skipCheck[0] = True
        # print('\nLISTENER STOPPED\n')
        return False  # Stop the listener

# Threader function allowing both the text animation and the listener to run simultaneously, allowing for skipping of text animation
def print_threader(in_str, speed=1):
    speed = textSpeed * speed
    global skipCheck
    skipCheck = [False]
    # print(speed*len(in_str)-0.5)
    t_print = threading.Thread(target=printtime, args=(in_str, speed))
    t_print.start()
    with keyboard.Listener(on_press=t_onpress_print,) as listener:    
        listener.join(timeout=(speed*len(in_str)-0.5))
    t_print.join()

    flush_input()
    return True

# Print function that prints character by character with a delay (FLAIR)
def printtime(in_str, speed=1): 
    global skipCheck
    for i in range(len(in_str)):
        if skipCheck[0]:
            # print('\SKIPPED\n')
            sys.stdout.write(in_str[i:])
            sys.stdout.flush()
            return
        sys.stdout.write(in_str[i])
        sys.stdout.flush()
        time.sleep(speed)

# Clears the text using single line removal (currently backup to clear() function)
def cleartxt(): 
    time.sleep(1)
    sys.stdout.write("\r" + " " * 100) 
    sys.stdout.write("\r")
    sys.stdout.flush()

# Reflects the clear function to the appropriate OS
match platform.system():
    case "Windows":
        clear = lambda: os.system('cls') #Clears the console
    case "Linux" | "Darwin":
        clear = lambda: os.system('clear') #Clears the console
    case _:
        clear = lambda: cleartxt()


"""API / EXTERNAL FUNCTIONS"""

# Astronomy Picture of the Day (APOD) function that fetches the APOD from NASA's API and displays it in the console
def apod_fetch(ask=False):
    if ask:
        print_threader("Please input your own NASA API key to access the APOD feature:\n\n")
        temp = input()
        api_key = temp if temp!="" or api_key!="cancel" else api_key
        if api_key == "cancel":
            return
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print_threader(f"Error fetching APOD: {e}\n Retry? (y/n)\n")
        retry_input = input().lower()[0]
        if retry_input == "y":
            apod_fetch()
        return


    match response.status_code:
        case 200:
            data = response.json()
            title = data.get("title", "No Title")
            explanation = data.get("explanation", "No Explanation").split('  ')
            image_url = data.get("hdurl", "No URL")
    
            print_threader(f"\nTitle: {title} \n")
            print_threader(f"Explanation: \n")
            for paragraph in explanation:
                print_threader(f"{paragraph.lstrip()}\n")
            print_threader(f"\nImage URL: {image_url}\n")
        case 403:
            print_threader("Error: Access Denied, please try another API key or check your credentials.\n")
            apod_fetch(True)
        case 404:
            print_threader("Error: APOD not found. Please try again later.\n")
        case _:
            print_threader(f"Error fetching APOD: {response.status_code}\n")


"""RESPONSE FUNCTIONS"""

# Simple algorithm that responds to user input based on a predefined set of responses ; does not consider similar input, only exact matches
# | NOT FUNCTIONING DUE TO FORMAT CHANGE IN responses & keys DICTIONARY |
def get_response_alg0(user_input):
    out_checkList=False
    counter=0

    for each in responses: 
        if user_input.lower() in each: out_checkList=True; break
        counter+=1
    if not out_checkList: print_threader("Sorry I don't know what that means, try again?");print();chatbot()

    # print a response from the list
    rndindex = random.randint(0, len(responses[keys[counter]]) - 1)

    print_threader(responses[keys[counter]][rndindex][0], responses[keys[counter]][rndindex][1])


# Rounds the input to nearest integer
def round_num(num):
    return ceil(num) if num-floor(num) >= 0.5 else floor(num)

# Removes unnecessary punctuation and non-key words from the input sentence, returning a list of key words for algorithm processing
def strip_sentence(sentence, wordlist=nonkey_wordlist):
    # Remove punctuation and convert to lowercase
    sentence = sentence.lower()
    for char in ['.', ',', '!', '?', ';', ':', '"', "'", '(', ')', '[', ']', '{', '}', '-', '_']:
        sentence = sentence.replace(char, '')
    sentence = sentence.strip().split(' ')
    for word in sentence:
        word = word.strip()
        if word in wordlist:
            sentence.remove(word)
    return sentence

# Analyzes the input with the keys, returning a list of scores for each key with a non-zero score 
# Explained in the README file
def get_similarity_scores(user_input, keys):
    scores = []
    score_index=0
    for key in keys:
        w_sum=0
        scores.append([key, 0])
        for word in user_input:
            found_inKey=False
            for key_word, weight in keys[key]:
                if word == key_word: scores[score_index][1] += weight ; found_inKey=True
            if not found_inKey: w_sum += 1 
            else: found_inKey=False
        if scores[score_index][1] == 0:
            scores.remove(scores[score_index])
        else:
            for key_word, weight in keys[key]: w_sum+=weight if weight>1 else 0
            scores[score_index][1] = round_num((scores[score_index][1] / (w_sum*0.72))*100) if w_sum > 0 else scores[score_index][1]
            score_index += 1
    return scores


# Returns the maximum score from the list of scores, or None if the list is empty
def get_best_output(scores):
    return max(scores, key=lambda x: x[1]) if scores else None

# Checks if the best score meets or exceeds the threshold to be considered a valid match
def check_threshold(best_score, threshold=15):
    return best_score[1] >= threshold if best_score else False

# TESTERS
# t = get_best_output(get_similarity_scores(strip_sentence("what are you doing my fine gentleman?"), keys))
# print(get_similarity_scores(strip_sentence("what are you doing my fine gentleman?"), keys))
# print(t, check_threshold(t))

# Combines all previous functions into the cases possible and prints the output!
def get_response_alg1(user_input):
    best_score = get_best_output(get_similarity_scores(strip_sentence(user_input), keys))
    # TESTERS
    # print(best_score)
    # print(check_threshold(best_score))
    match best_score[0]:
        case "apod":
            apod_fetch(api_key=="DEMO_KEY")
        case "settings":
            settings()
        case "cls":
            clear()
        case "exit":
            ty_response = random.choice(responses["thanksvar"])
            print_threader(ty_response[0], ty_response[1])
            exit()
        case _:
            if check_threshold(best_score):
                random_response = random.choice(responses[best_score[0]])
                print_threader(random_response[0], random_response[1])
            else:
                print_threader("I'm sorry, I don't have a response for that. \n Would you like something else?")


"""SETTINGS / CHATBOT FUNCTIONS"""

# Simple settings menu, case specific for user variables (API key, text speed, username)
def settings(case=None):
    global api_key
    global textSpeed
    global user_name

    
    match case:
        case None: 
            print_threader("Settings Menu: \n\n")
            print_threader("1. Change NASA API Key \n2. Change Text Speed \n3. Change User Name \n4. Back to Chatbot\n")
            settings(input())
        case "0":
            print_threader("Would you like to change another setting? \n\n")
            print_threader("1. Change NASA API Key\n")
            print_threader("2. Change Text Speed\n")
            print_threader("3. Change User Name\n")
            print_threader("4. Back to Chatbot\n")
        case "1":
            print_threader("Please input your own NASA API key:\n\n")
            api_key = input()
            print_threader("API key updated successfully!\n")
            settings()
        case "2":
            if not case: print_threader("Current text speed is " + str(textSpeed) + " seconds per character.\n")
            print_threader("Please input the desired text speed (in seconds per character, e.g.):\n\n")
            try:
                textSpeed = float(input())
                print_threader(f"Text speed updated to {textSpeed} seconds per character.\n")
                settings(0)
            except ValueError:
                print_threader("Invalid input. Please enter a valid number.\n")
                settings(2)
        case "3":
            print_threader("Please input your desired username:\n\n")
            user_name = input()
            print_threader("Username updated successfully!\n")
            settings()
        case "4":
            chatbot()
        case _:
            print_threader("Invalid choice. Please try again.\n")
            settings()


# Main chatbot loop
def chatbot():
    global api_key
    global user_name
    print()

    print(user_name + " > \n")
    user_input = input()

    print()

    print("Bot > \n")
    # Lowers the runtime for fast inputs - even with algorithm implementation
    match user_input.lower():
        case 'exit' | 'bye':
            print_threader("Goodbye! Take care!\n\n")
            exit()
        case 'apod':
            apod_fetch(api_key=="DEMO_KEY")
        case "clear" | "cls":
            clear()
        case "settings":
            settings()
        case _:
            get_response_alg1(user_input)
    
    chatbot()

if __name__ == "__main__":
    # Prints the user's name from the environment variable USERNAME to personalise the greeting, then starts the chatbot
    print_threader("Hello, " + user_name + " what do you need?"); print()
    chatbot()