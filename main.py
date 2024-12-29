import os
import time
import pickle
import re


class PickleSaver:
    def __init__(self, title: str):
        self.title = title

    def save_data(self, name: str, page: int):
        # saves the page number to a pickle file
        data = self.load_data()
        data.update(
            {name: page}
        )  # updates the name to the new page number in the save data dictionary
        with open(f"{self.title}_data.pkl", "wb") as pickle_file:
            pickle.dump(data, pickle_file)

    def load_data(self):
        # loads the page number from a pickle file
        if not os.path.exists(f"{self.title}_data.pkl"):
            print("No existing data found.")
            return {}
        try:
            with open(f"{self.title}_data.pkl", "rb") as pickle_file:
                data = pickle.load(pickle_file)
                return data
        except EOFError:
            print("The data file is corrupted!")
            return {}
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return {}


class Formatter:

    def find_books(self):
        books = []
        for file in os.listdir():
            if file.endswith(".txt") or file.endswith(".md"):
                books.append(file)
        return books

    def select_book(self):
        books = self.find_books()
        if not books:
            print("No books found.")
            return None, []
        for i in books:
            print(f"[{books.index(i)+1}] {re.sub(r".txt|.md", "", i)}") # prints a list of valid books
        try:
            choice = int(input("Select a book by number: ")) - 1
            if choice < 0 or choice >= len(books):
                print("Invalid input. Please enter a valid number.")
            title = books[choice]
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return self.select_book()
        except IndexError:
            print("That value is out of range!")
        except Exception as e:
            print(f"Sorry, there was an error: {e}")
        with open(title, "r") as file:
            paragraphs = file.read().split(
                "\n\n"
            )  # splits the book into paragraphs
        if not os.path.exists(f"{title}_data.pkl"):
            with open(f"{title}_data.pkl", "wb") as file:
                pickle.dump(
                    {}, file
                )  # if not, makes a new pickle file with blank save data
        return title, paragraphs

    def split_book(self):
        title, book = self.select_book()
        words = {}
        for paragraph in book:
            for word in paragraph.split(" "):
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
        sorted_words = sorted(
            words.items(), key=lambda item: item[1], reverse=True
        )[:50]
        for word in sorted_words:
            print(f"{word}: {words[word]}")


class Reader:
    def read_book(self):
        formatter = Formatter()
        title, book = formatter.select_book()
        if title is None:
            print("No book selected. Exiting.")
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
                print(
                    "Enter \"f\" to finish and the ENTER key to continue.\n\n"
                )
                print(book[page])
                page += 1
                command = input("")
            except IndexError:
                print("Wow, you finished the book!")
                command = "f"
        end = time.time()
        os.system("cls")
        print(
            f"Great! You read for {round(end-start, 2)} seconds.\nYou got up to page {page}!"
        )
        saver.save_data(name, page)


def main():
    choice = input(
        """PYTHON READER
[1] Read a book
[2] Analyse a book
> """
    )
    reader = Reader()
    formatter = Formatter()
    results = {1: reader.read_book, 2: formatter.split_book}
    while True:
        try:
            choice = int(choice)
            results[choice]()
            break
        except KeyError:
            print("Please enter a valid number!")
        except ValueError:
            print("Please enter a valid number!")
        except Exception as e:
            print(f"Sorry, there was an error: {e}")
        choice = input(
            """PYTHON READER
[1] Read a book
[2] Analyse a book
> """
        )


if __name__ == "__main__":
    main()
