import tkinter as tk
from tkinter import font
import os
import time
import pickle

class App(tk.Tk):
    def __init__(self):
        super().__init__() # inherits from the tk.Tk class
        self.title("Python Reader") # title of window
        self.geometry("500x500") # size of window
        self.frames = {} # dictionary to store the pages
        self.make_pages()

    def make_pages(self):
        for F in (Pages.MainPage, Pages.ErrorPage, Pages.SelectPage):  # list of classes of pages
            page_name = F.__name__
            page = F(parent=self, controller=self)  # makes a new instance of the page
            self.frames[page_name] = page  # stores the page in the local dictionary
            page.grid(row=0, column=0, sticky="nsew") # places page in window
        self.show_page("MainPage")  # shows the main page

    def show_page(self, page_name, message=None):
        page = self.frames[page_name]
        if message:
            page.set_message(message)
        page.tkraise() # shows the page

class Pages:
    class MainPage(tk.Frame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.controller = controller
            reader = Reader(controller)       # new instances of the 
            formatter = Formatter(controller) # Reader and Formatter classes
            bold = font.Font(weight="bold")

            label = tk.Label(self, text="Welcome to the Python Reader!", font=bold)
            label.pack(pady=10, padx=10)
            read_button = tk.Button(self, text="Read a book",
                                    command=lambda: reader.read_book())
            read_button.pack(pady=10)
            analyse_button = tk.Button(self, text="Analyse a book",
                                       command=lambda: formatter.split_book())
            analyse_button.pack(pady=10)

            self.pack(expand=True, fill=tk.BOTH)

    class ErrorPage(tk.Frame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.controller = controller
            self.message_label = tk.Label(self, text="", fg="red")
            self.message_label.pack(pady=10, padx=10)
            button = tk.Button(self, text="Go to the main page",
                               command=lambda: controller.show_page("MainPage"))
            button.pack()

        def set_message(self, message):
            self.message_label.config(text=message)

    class SelectPage(tk.Frame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.controller = controller
            self.selected_book = tk.StringVar()  # stores the selected book
            self.message_label = tk.Label(self, text="", fg="red")
            self.message_label.pack(pady=10)
            
            label = tk.Label(self, text="Select a book to read:")
            label.pack(pady=10)
            
            self.book_buttons_frame = tk.Frame(self)  # frame to hold the radio buttons
            self.book_buttons_frame.pack(pady=10)
            
            submit_button = tk.Button(self, text="Submit", command=self.submit_selection)
            submit_button.pack(pady=10)
        
        def display_books(self, books):
            # clears any existing widgets in the book_buttons_frame
            for widget in self.book_buttons_frame.winfo_children():
                widget.destroy()
            
            # displays a message if no books are available
            if not books:
                self.controller.show_page("ErrorPage", message="Your library is empty!\nDownload any .txt or .md file into this directory to get started.")
                return
            
            # creates a radio button for each book
            for book in books:
                radio_button = tk.Radiobutton(self.book_buttons_frame, text=book, variable=self.selected_book, value=book)
                radio_button.pack(anchor="w")
        
        def submit_selection(self):
            selected_book = self.selected_book.get()  # gets the selected book
            if selected_book:
                reader = Reader(self.controller)
                reader.read_book(selected_book)
            else:
                self.controller.show_page("ErrorPage", message="Please select a book.")
        
        def set_message(self, message):
            self.message_label.config(text=message)  # sets the message in the message_label

class PickleSaver:
    def __init__(self, title: str):
        self.title = title

    def save_data(self, name: str, page: int):
        # saves the page number to a pickle file
        data = self.load_data()
        data.update({name: page}) # updates the name to the new page number in the save data dictionary
        with open(f"{self.title}_data.pkl", "wb") as pickle_file:
            pickle.dump(data, pickle_file)

    def load_data(self):
        # loads the page number from a pickle file
        if not os.path.exists(f"{self.title}_data.pkl"):
            self.controller.show_page("ErrorPage", message="No existing data found.")
            return {}
        try:
            with open(f"{self.title}_data.pkl", "rb") as pickle_file:
                data = pickle.load(pickle_file)
                return data
        except EOFError:
            self.controller.show_page("ErrorPage", message="The data file is corrupted!")
            return {}
        except Exception as e:
            self.controller.show_page("ErrorPage", message=f"An error occurred while loading data: {e}")
            return {}

class Formatter:
    def __init__(self, controller):
        self.controller = controller

    def find_books(self):
        books = []
        for file in os.listdir():
            if file.endswith(".txt") or file.endswith(".md"):
                books.append(file)
        return books

    def select_book(self, selected_book=None):
        books = self.find_books()
        if not books:
            self.controller.show_page("ErrorPage", message="Your library is empty!\nDownload any .txt or .md file into this directory to get started.")
            return None, []
        
        if selected_book:
            try:
                with open(selected_book, "r") as file:
                    paragraphs = file.read().split("\n\n") # splits the book into paragraphs
                if not os.path.exists(f"{selected_book}_data.pkl"):
                    with open(f"{selected_book}_data.pkl", "wb") as file:
                        pickle.dump({}, file) # if not, makes a new pickle file with blank save data
                return selected_book, paragraphs
            except Exception as e:
                self.controller.show_page("ErrorPage", message=f"An error occurred: {e}")
                return None, []
        else:
            self.controller.frames["SelectPage"].display_books(books)
            self.controller.show_page("SelectPage")
            return None, []

    def split_book(self):
        title, book = self.select_book()
        if title is None:
            return
        words = {}
        for paragraph in book:
            for word in paragraph.split(" "):
                word = word.lower().strip(",.!?\"'()[]{}<>:;")  # normalises words
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
        sorted_words = sorted(words.items(), key=lambda item: item[1], reverse=True)
        top = sorted_words[:10]
        for word, count in top:
            print(f"{word}: {count}")

class Reader:
    def __init__(self, controller):
        self.controller = controller

    def read_book(self, selected_book=None):
        formatter = Formatter(self.controller)
        title, book = formatter.select_book(selected_book)
        if title is None:
            return
        saver = PickleSaver(title)
        os.system("cls")
        name = input("Enter your name: ")
        data = saver.load_data()
        if name in data:
            page = data[name]
        else:
            input("No previous data found. Starting from page 0.")
            page = 0
        if page == 0:
            input("You are about to begin reading.")
        else:
            input(f"You are about to continue from page {page}.")
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
        print(f"Great! You read for {round(end-start, 2)} seconds.\nYou got up to page {page}!")
        saver.save_data(name, page)

if __name__ == "__main__":
    app = App()
    app.mainloop()
