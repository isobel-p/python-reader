import os
import time

def find_books():
    books = []
    for file in os.listdir():
        if file.endswith(".txt"):
            books.append(file)
    return books

def select_book(): 
    books = find_books()
    print("Select a book to convert from the following: ") 
    for i in books: 
        print(f'[{books.index(i)}] {i}') 
    try:
        return books[int(input("> "))] 
    except IndexError: 
        print("That's not an option!") 
        return -1
    except ValueError: 
        print("You should enter the number of the book!") 
        return -1
    
def format_book():
    title = select_book()
    if title != -1:
        file = open(title, "r")
        book = file.read()
        paragraphs = book.split("\n\n")
        file.close()
        return paragraphs

def read_book(book = None):
    if book == None:
        book = format_book()
    try:
        page = int(input("Enter page number: "))
        if page == 0:
            print("You are about to begin reading.", end=" ")
        else:
            print(f'You are about to continue from page {page}.', end=" ")
        #print("Make sure to save your progress - do not close the program manually.")
        print("Enter \"f\" to finish and the ENTER key to continue.\n----------------------")
        page -= 1
        command = ""
        start = time.time()
        while command.lower() != "f":
            try:
                print(book[page])
                page += 1
                # command = input("Enter \"f\" to finish and the ENTER key to continue.\n")
                command = input("")
            except IndexError:
                print("Wow, you finished the book!")
                command = "f"
        end = time.time()
        print(f'Great! You read for {round(end-start, 2)} seconds.')
        print(f'You got up to page {page} - remember!') # todo: find a way to save this automatically
    except ValueError:
        print("Enter a page number!")
        read_book(book)

def main():
    choice = input("""PYTHON READER 
[1] Read a book 
...more options here
> """)
    results  = {"1":"read_book"} 
    globals()[results[choice]]()

main()