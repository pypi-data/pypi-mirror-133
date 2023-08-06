from bs4 import BeautifulSoup
import requests


def parser(class_element) -> str:
    class_element = str(class_element)
    splited_word = class_element.split(">\n")[2]
    return splited_word[:3].upper()

def check(word:str):
    URL = f"https://www.verbformen.com/declension/nouns/{word}.htm"
    print(f"searched : {word}")
    site_request = requests.get(URL)
    
    if site_request.status_code:
        soup = BeautifulSoup(site_request.text, 'html.parser')
        try:
            class_element=soup.find_all(class_='vGrnd rCntr')
            artikel = parser(class_element)
            print(f"answer: {artikel} {word}")
        except Exception as e:
            print(f"something is wrong: {e}")

    else:
        print("answer: NOT found")