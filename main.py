import os 
import time 
import pickle 
import re 
 

def find_books(): 
    books = [] 
    for file in os.listdir(): 
        if file.endswith(".txt"): 
            books.append(file) 
    return books 


def select_book(): 
    books = find_books() 
    os.system("cls") 
    print("Select a book from the following: ") 
    for i in books: 
        print(f'[{books.index(i)+1}] {re.sub(r".txt", "", i)}') 
    try: 
        return books[int(input("> "))-1] 
    except IndexError: 
        print("That's not an option!") 
        return -1 
    except ValueError: 
        print("You should enter the number of the book!") 
        return -1 


def save_data(title: str, name: str, page: int): 
    data = load_data(title) 
    data.update({name: page}) 
    with open(f'{title}_data.pkl', 'wb') as pickle_file: 
        pickle.dump(data, pickle_file) 

 
def load_data(title: str): 
    if not os.path.exists(f'{title}_data.pkl'): 
        print("No existing data found.") 
        return {} 
    try: 
        with open(f'{title}_data.pkl', 'rb') as pickle_file: 
            data = pickle.load(pickle_file) 
            return data 
    except EOFError: 
        print("The data file is corrupted!") 
        return {} 
    except Exception as e: 
        print(f"An error occurred while loading data: {e}") 
        return {} 


def format_book(): 
    title = select_book() 
    if title != -1: 
        with open(title, "r") as file: 
            book = file.read() 
        paragraphs = book.split("\n\n") 
        if not os.path.exists(f'{title}_data.pkl'): 
            with open(f'{title}_data.pkl', "wb") as file: 
                pickle.dump({}, file) 
        return title, paragraphs 

 
def read_book(): 
    title, book = format_book() 
    os.system("cls") 
    name = input("Enter your name: ") 
    data = load_data(title) 
    if name in data: 
        page = data[name] 
    else: 
        print("No previous data found. Starting from page 0.") 
        page = 0 
    if page == 0: 
        print("You are about to begin reading.", end=" ") 
    else: 
        print(f'You are about to continue from page {page}.', end=" ") 
    print("Enter \"f\" to finish and the ENTER key to continue.\n\n") 
    command = "" 
    start = time.time() 
    while command.lower() != "f": 
        try: 
            os.system("cls") 
            print("Enter \"f\" to finish and the ENTER key to continue.\n\n") 
            print(book[page]) 
            page += 1 
            command = input("") 
        except IndexError: 
            print("Wow, you finished the book!") 
            command = "f" 
    end = time.time() 
    os.system("cls") 
    print(f'Great! You read for {round(end-start, 2)} seconds.\nYou got up to page {page}!') 
    save_data(title, name, page) 
    main() 

def split_book():
    title, book = format_book()
    words = {}
    for paragraph in book:
        for word in paragraph.split(" "):
            if word in words:
                words[word] += 1
            else:
                words[word] == 1
    for word in words:
        print(f'{word}: {words[word]}')
        main()
 
def main(): 
    choice = input("""PYTHON READER 
[1] Read a book
[2] Analyse a book
...more options here  
> """)  
    results  = {"1":"read_book", "2":"split_book"} 
    try: 
        globals()[results[choice]]() # runs the function name under the key that the user just entered
    except KeyError: 
        print("Please enter a number!") 
        main() 
    except Exception as e: 
        print(f"Sorry, there was an error: {e}") 
        main() 
main()  
