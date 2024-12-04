# Miranda Rendon
# Julian Gonzalez
# 2520.01

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# connect to SQLite
conn = sqlite3.connect('media.db')
cursor = conn.cursor()

# books database
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL
)
''')

# dvd database
cursor.execute('''
CREATE TABLE IF NOT EXISTS dvds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    director TEXT NOT NULL,
    genre TEXT NOT NULL
)
''')
conn.commit()

def openBookList():
    bookWindow = tk.Toplevel(root)
    bookWindow.title("Books")

    # header bar
    header = tk.Frame(bookWindow)
    header.pack(fill=tk.X, padx=10, pady=5)

    tk.Label(header, text="Books", font=("Arial", 16)).pack(side=tk.LEFT)

    remButton = tk.Button(header, text="Remove", command=lambda: openRemoveBook(bookWindow))
    remButton.pack(side=tk.RIGHT, padx=5)
    
    addButton = tk.Button(header, text="Add", command=lambda: openAddBook(bookWindow))
    addButton.pack(side=tk.RIGHT, padx=5)

    sortVar = tk.StringVar(value="Sort")
    sortMenu = ttk.OptionMenu(header, sortVar, "Sort", "Title", "Author", "Genre", command=lambda x: displayBoooks(bookTree, x))
    sortMenu.pack(side=tk.RIGHT)

    # table of books
    columns = ("Title", "Author", "Genre")
    global bookTree
    bookTree = ttk.Treeview(bookWindow, columns=columns, show="headings")
    bookTree.heading("Title", text="Title")
    bookTree.heading("Author", text="Author")
    bookTree.heading("Genre", text="Genre")
    bookTree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # displays window when opened
    displayBoooks(bookTree)

def openAddBook(parentWindow):
    addWindow = tk.Toplevel(parentWindow)
    addWindow.title("Add Book")

    # input boxes
    tk.Label(addWindow, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    titleEntry = tk.Entry(addWindow)
    titleEntry.grid(row=0, column=1)
    
    tk.Label(addWindow, text="Author:").grid(row=1, column=0, padx=5, pady=5)
    authorEntry = tk.Entry(addWindow)
    authorEntry.grid(row=1, column=1)
    
    tk.Label(addWindow, text="Genre:").grid(row=2, column=0, padx=5, pady=5)
    genreEntry = tk.Entry(addWindow)
    genreEntry.grid(row=2, column=1)
    
    def addBook():
        title = titleEntry.get().strip().title()
        author = authorEntry.get().strip().title()
        genre = genreEntry.get().strip().title()

        if not title or not author or not genre:
            messagebox.showerror("Error", "Fill out all fields")
        else:
            cursor.execute('INSERT INTO books (title, author, genre) VALUES (?, ?, ?)', (title, author, genre))
            conn.commit()
            messagebox.showinfo("Success", "Book added")
            addWindow.destroy()
            displayBoooks(bookTree)
        
    tk.Button(addWindow, text="Add", command=addBook).grid(row=3, column=0, pady=5)
    tk.Button(addWindow, text="Close", command=addWindow.destroy).grid(row=3, column=1, pady=5)

def openRemoveBook(parentWindow):
    removeWindow = tk.Toplevel(parentWindow)
    removeWindow.title("Remove Book")

    tk.Label(removeWindow, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    titleEntry = tk.Entry(removeWindow)
    titleEntry.grid(row=0, column=1)

    def removeBook():
        removeT = titleEntry.get().strip().title()
        if not removeT:
            messagebox.showerror("Error", "Fill out all fields")
        else:
            cursor.execute('DELETE FROM books WHERE title=?', (removeT,))
            conn.commit()
            messagebox.showinfo("Success", "Book removed")
            removeWindow.destroy()
            displayBoooks(bookTree)

    tk.Button(removeWindow, text="Remove", command=removeBook).grid(row=3, column=0, pady=5)
    tk.Button(removeWindow, text="Close", command=removeWindow.destroy).grid(row=3, column=1, pady=5)
        

def displayBoooks(tree, sort_by=None):
    # clear existing table
    for row in tree.get_children():
        tree.delete(row)
    
    # get sorted data from DB
    if sort_by:
        query = f'SELECT title, author, genre FROM books ORDER BY {sort_by.lower()}'
    else:
        query = 'SELECT title, author, genre FROM books'
    cursor.execute(query)
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", tk.END, values=row)

def openDVDList():
    dvdWindow = tk.Toplevel(root)
    dvdWindow.title("DVDs")

    # header bar
    header = tk.Frame(dvdWindow)
    header.pack(fill=tk.X, padx=10, pady=5)

    tk.Label(header, text="DVDs", font=("Arial", 16)).pack(side=tk.LEFT)

    remButton = tk.Button(header, text="Remove", command=lambda: openRemoveDVD(dvdWindow))
    remButton.pack(side=tk.RIGHT, padx=5)
    
    addButton = tk.Button(header, text="Add", command=lambda: openAddDVD(dvdWindow))
    addButton.pack(side=tk.RIGHT, padx=5)

    sortVar = tk.StringVar(value="Sort")
    sortMenu = ttk.OptionMenu(header, sortVar, "Sort", "Title", "Director", "Genre", command=lambda x: showDVDTable(dvdTree, x))
    sortMenu.pack(side=tk.RIGHT)

    # table of books
    columns = ("Title", "Director", "Genre")
    global dvdTree
    dvdTree = ttk.Treeview(dvdWindow, columns=columns, show="headings")
    dvdTree.heading("Title", text="Title")
    dvdTree.heading("Director", text="Director")
    dvdTree.heading("Genre", text="Genre")
    dvdTree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # displays window when opened
    showDVDTable(dvdTree)

def openAddDVD(parentWindow):
    addWindow = tk.Toplevel(parentWindow)
    addWindow.title("Add DVD")

    # input boxes
    tk.Label(addWindow, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    titleEntry = tk.Entry(addWindow)
    titleEntry.grid(row=0, column=1)
    
    tk.Label(addWindow, text="Director:").grid(row=1, column=0, padx=5, pady=5)
    directorEntry = tk.Entry(addWindow)
    directorEntry.grid(row=1, column=1)
    
    tk.Label(addWindow, text="Genre:").grid(row=2, column=0, padx=5, pady=5)
    genreEntry = tk.Entry(addWindow)
    genreEntry.grid(row=2, column=1)
    
    def addDVD():
        title = titleEntry.get().strip().title()
        director = directorEntry.get().strip().title()
        genre = genreEntry.get().strip().title()

        if not title or not director or not genre:
            messagebox.showerror("Error", "Fill out all fields")
        else:
            cursor.execute('INSERT INTO dvds (title, director, genre) VALUES (?, ?, ?)', (title, director, genre))
            conn.commit()
            messagebox.showinfo("Success", "DVD added")
            addWindow.destroy()
            showDVDTable(dvdTree)
        
    tk.Button(addWindow, text="Add", command=addDVD).grid(row=3, column=0, pady=5)
    tk.Button(addWindow, text="Close", command=addWindow.destroy).grid(row=3, column=1, pady=5)

def openRemoveDVD(parentWindow):
    removeWindow = tk.Toplevel(parentWindow)
    removeWindow.title("Remove DVD")

    tk.Label(removeWindow, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    titleEntry = tk.Entry(removeWindow)
    titleEntry.grid(row=0, column=1)

    def removeDVD():
        removeT = titleEntry.get().strip().title()
        if not removeT:
            messagebox.showerror("Error", "Fill out all fields")
        else:
            cursor.execute('DELETE FROM dvds WHERE title=?', (removeT,))
            conn.commit()
            messagebox.showinfo("Success", "DVD removed")
            removeWindow.destroy()
            showDVDTable(dvdTree)

    tk.Button(removeWindow, text="Remove", command=removeDVD).grid(row=3, column=0, pady=5)
    tk.Button(removeWindow, text="Close", command=removeWindow.destroy).grid(row=3, column=1, pady=5)

def showDVDTable(tree, sort_by=None):
    # clear existing table
    for row in tree.get_children():
        tree.delete(row)
    
    # get sorted data from DB
    if sort_by:
        query = f'SELECT title, director, genre FROM dvds ORDER BY {sort_by.lower()}'
    else:
        query = 'SELECT title, director, genre FROM dvds'
    cursor.execute(query)
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", tk.END, values=row)

root = tk.Tk()
root.title("Physical Media Manager")

welcomeLabel = tk.Label(root, text="Welcome to your Physical Media Manager!")
welcomeLabel.pack(pady=10)

bookButton = tk.Button(root, text="Book", command=openBookList)
bookButton.pack(pady=10)

dvdButton = tk.Button(root, text="DVD", command=openDVDList)
dvdButton.pack(pady=10)

root.mainloop()

# close database
conn.close()
