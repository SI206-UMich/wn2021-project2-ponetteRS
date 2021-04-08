from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    with open(filename) as f:
        file = f.read()

    books_lst = []
    author_lst = []
    final_lst = [] 

    
    soup = BeautifulSoup(file, "lxml")
  
    soup2 = soup.find_all("tr", itemtype="http://schema.org/Book") #larger piece
    author_names = []

    for i in soup2:
        author = i.find("div", class_="authorName__container")
        author_names.append(author)

    book_titles = soup.find_all("a", class_="bookTitle") 

    for author in author_names:
        author_lst.append(author.text.strip())
    
    for book in book_titles:
        books_lst.append(book.text.strip())
    
    for i in range(len(book_titles)):
        final_lst.append((books_lst[i], author_lst[i]))
    #print(books_lst, author_lst, final_lst)

    return final_lst


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    content = requests.get(url)
    links = []
    soup = BeautifulSoup(content.text, "lxml")
    table = soup.find("div", class_="leftContainer")
    tags = table.find_all("a")

    for tag in tags:
        href = tag["href"]
        if href.startswith("/book/show/"):
            links.append(f"https://www.goodreads.com{href}")

    return links[:10]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    
    info = requests.get(book_url)
    soup = BeautifulSoup(info.text, "lxml")

    title = soup.find("h1", class_="gr-h1 gr-h1--serif").text.strip()
    author = soup.find("div", class_="authorName__container").text
    pages = soup.find("span", itemprop="numberOfPages").text.strip()

    pages = pages.split(" ")
    pages = pages[0]
    pages = int(pages)

    return (title, author, pages)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    root_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    filename = os.path.join(root_path, filepath)
    with open(filename, "r") as file_content:
        file_str = file_content.read()
     
    soup = BeautifulSoup(file_str, "lxml")
    category_list = []
    content = soup.find_all("h4")
    
    for category in content:
        category_list.append(category.text.strip())

    title_list = []
    for div in soup.find_all('div', 'category__winnerImageContainer'):
        for img in div.find_all("img", alt=True):
            title_list.append(img["alt"])
    
    url_lst = []
    urls = soup.find_all("div", "category clearFix")
    for url in urls:
        url_lst.append(url.find("a")["href"])

    tup_list = []
    for category,title,url in zip(category_list, title_list, url_lst):
        tup = (category, title, url)
        tup_list.append(tup)
    
    return tup_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), 'w') as csv_content:
        csv_file = csv.writer(csv_content, delimiter=",")
        csv_file.writerow(["Book title", "Author Name"])
        print(data)
        for tup in data:
            csv_file.writerow(tup) #this doesn't seem to be writing to the file


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    # search_urls = get_search_links()
    search_urls = get_search_links()
    


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        lst_titles = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(lst_titles), 20, "Length is not 20")

        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(lst_titles, list)

        # check that each item in the list is a tuple

        for item in lst_titles:
            if type(item)  is tuple == False:
                return "Items in lst_titles not all tuple"

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        #I went to the website and picked the first result assuming they will match
        self.assertEqual(lst_titles[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)","J.K. Rowling"), "First book and author are not correct")

        # check that the last title is correct (open search_results.htm and find it)
        #I went to the website and picked the last result assuming they will match
        self.assertEqual(lst_titles[-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)", "Last title is incorrect")

    def test_get_search_links(self):
        #helps set up
        
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls) is list, True, "search_urls is not a list")

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10, "Length of TestCases.search_urls is not 10")

        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            if type(url) is not str:
                return "Not all urls in TestCases.search_urls are strings"

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        #FIXME what makes an url correct?


    def test_get_book_summary(self): 
        #start after first two functions running bc build off each other
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []

        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        for summary in summaries:
            self.assertIsInstance(summary, tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(summary), 3)
            # check that the first two elements in the tuple are string
            self.assertIsInstance(summary[0], str)
            self.assertIsInstance(summary[1], str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertIsInstance(summary[2], int)
            # check that the first book in the search has 337 pages
            self.assertEqual(summaries[0][2], 337) #is this the correct indentation?

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_book_sums = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_book_sums), 20)

            # assert each item in the list of best books is a tuple
        for tup in best_book_sums:
            # check that each tuple has a length of 3
            self.assertEqual(len(tup), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        # print(best_book_sums[0])
        self.assertEqual(best_book_sums[0][0],'Fiction')
        self.assertEqual(best_book_sums[0][1],"The Midnight Library")
        self.assertEqual(best_book_sums[0][2],'https://www.goodreads.com/choiceawards/best-fiction-books-2020')
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_book_sums[-1][0],'Picture Books')
        self.assertEqual(best_book_sums[-1][1],"Antiracist Baby")
        self.assertEqual(best_book_sums[-1][2],'https://www.goodreads.com/choiceawards/best-picture-books-2020')

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        best_books = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(best_books, "test.csv")
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        lst = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "test.csv"), "r") as testfile:
            csv_reader = csv.reader(testfile)
        # read in the csv that you wrote
            for elem in csv_reader:
                lst.append(elem)

        # check that there are 21 lines in the csv
        self.assertEqual(len(lst), 21)
        # check that the header row is correct
        self.assertEqual(lst[0], ["Book title", "Author Name"])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(lst[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(lst[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2) #commenting out to save time
    #get_titles_from_search_results("search_results.htm")



