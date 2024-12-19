import os 
import time 
import pickle 
import re 
 

def find_books():
    # find a list of valid books
    books = [] 
    for file in os.listdir(): 
        if file.endswith(".txt") or file.endswith(".md"): 
            books.append(file) 
         # finds all text or markdown files in the directory
    return books 


def select_book():
    # prompts the user to pick a book
    books = find_books() 
    os.system("cls") # clears the shell
    print("Select a book from the following: ") 
    for i in books: 
        print(f'[{books.index(i)+1}] {re.sub(r".txt",, ".md", "", i)}') # prints a list of valid books
    try: 
        return books[int(input("> "))-1] 
    except IndexError: 
        print("That's not an option!") 
        return -1 
    except ValueError: 
        print("You should enter the number of the book!") 
        return -1 


def save_data(title: str, name: str, page: int):
    # saves the page number to a pickle file
    data = load_data(title) 
    data.update({name: page}) # updates the name to the new page number in the save data dictionary
    with open(f'{title}_data.pkl', 'wb') as pickle_file: 
        pickle.dump(data, pickle_file) 

 
def load_data(title: str):
    # loads the page number from a pickle file
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
    # splits the book into pages                  
    title = select_book() 
    if title != -1: 
        with open(title, "r") as file: 
            book = file.read() 
        paragraphs = book.split("\n\n") # splits the book into paragraphs
        if not os.path.exists(f'{title}_data.pkl'): # checks if pickle save file already exists i.e. if the book has been read before 
            with open(f'{title}_data.pkl', "wb") as file: 
                pickle.dump({}, file) # if not, makes a new pickle file with blank save data
        return title, paragraphs 

 
def read_book():
    # reads the book
    title, book = format_book() 
    os.system("cls") # clears the shell
    name = input("Enter your name: ") 
    data = load_data(title) 
    if name in data: # checks if the person has read this book before
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
    while command.lower() != "f": # continues printing new pages until the user enters "f"
        try: 
            os.system("cls") # clears the shell 
            print("Enter \"f\" to finish and the ENTER key to continue.\n\n") 
            print(book[page]) 
            page += 1 
            command = input("") 
        except IndexError: 
            print("Wow, you finished the book!") 
            command = "f" 
    end = time.time() 
    os.system("cls") # clears the shell
    print(f'Great! You read for {round(end-start, 2)} seconds.\nYou got up to page {page}!') 
    save_data(title, name, page) 
    main() 

def split_book():
    # separates the book into word counts
    title, book = format_book()
    words = {} # makes a new dictionary for key-value pairs
    for paragraph in book:
        for word in paragraph.split(" "):
            if word in words:
                words[word] += 1 # if the word has already appeared increase the count
            else:
                words[word] == 1 # else create a new count
    for word in words:
        print(f'{word}: {words[word]}') # prints all key-value pairs
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
