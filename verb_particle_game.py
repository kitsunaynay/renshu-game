import requests
import random
from bs4 import BeautifulSoup
import re

def read_verb_list(filename):
    words = []
    with open(filename, 'r') as file:
        for line in file:
            first_word = line.split(';', 1)[0].strip()
            words.append(first_word)
    return words

def print_reibun(text, verb):

    highlight_color = "\033[93m"
    reset_color = "\033[0m"
    particles = ["を", "は", "に", "が", "と", "で"]
    
    index = text.find(verb)
    
    if index == -1:
        return None

    start_index = max(0, index - 6)
    highlighted_text = text[:start_index]
    found = 0
    for i in range(start_index, index):
        letter = text[i]
        if letter in particles and found != 1:
            found = 1
            highlighted_text += highlight_color + letter + reset_color
        else:
            highlighted_text += letter
            
    highlighted_text += text[index:]

    print(highlighted_text)


def get_verb_info(verb):
    url = f'https://jisho.org/search/{verb}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        element = soup.select_one('.concept_light-readings.japanese.japanese_gothic > div > span.text')

        if element.text.strip() != verb[0]:
            verb = element.text.strip()

        ul_element = soup.find('ul', class_='japanese japanese_gothic clearfix')
    
        if ul_element:
            spans = ul_element.find_all('span', class_='unlinked')
            text = ''.join([span.get_text().strip() for span in spans])
            print(verb)
            if verb in text:
                print("inf")
                print_reibun(text, verb)
            elif len(verb) == 2:
                print("2")
                if verb[0] in text:
                    print_reibun(text, verb[0])
            elif len(verb) > 2:
                print("3")
                if verb[:-1] in text:
                    print_reibun(text, verb[:-1])



        verb_info = soup.find(class_='meaning-tags')
        if verb_info:
            text = verb_info.get_text().lower()
            if 'transitive' in text:
                return 'transitive'
            elif 'intransitive' in text:
                return 'intransitive'
    return None

def play_game():
    verbs = read_verb_list("日本学/code/jlpt_verbs.csv")

    hiragana_pattern = re.compile(r'^[\u3040-\u309F]+$')
    verb = random.choice(verbs)
    while (not bool(hiragana_pattern.match(verb[-1]))):
        verb = random.choice(verbs)
    print(f"\n'{verb}'")

    user_input = input()
    
    if user_input == 'close' or user_input == 'x' or user_input == 'exit':
        print("Game closed!")
        return 1

    verb_info = get_verb_info(verb)

    if verb_info is None:
        print(f"Sorry, I couldn't find information about the verb '{verb}'.")
    else:
        print(f">> {verb_info}")
    return 0

if __name__ == '__main__':
    print("Game started. Type 'close' to exit or enter to see the result.\nReminder:")
    print("Transitive: require a direct object. Object + を.\nIntransitive: require no object. 「を・が・は・に」")
    cntue = 0
    while cntue == 0:
        cntue = play_game()