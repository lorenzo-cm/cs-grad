from model import Book, Rental, Client

def test_rent_regular_book_short_duration():
    book = Book("Refactoring", Book.REGULAR)
    r = Rental(book, 2)

    c = Client("Fulano")
    c.add_rental(r)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Refactoring: 2\n"
        "Total: 2\n"
        "Points: 1"
    )
    
    assert c.statement() == expected_report

def test_rent_regular_book_long_duration():
    book = Book("Refactoring", Book.REGULAR)
    r = Rental(book, 3)

    c = Client("Fulano")
    c.add_rental(r)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Refactoring: 3.5\n"
        "Total: 3.5\n"
        "Points: 1"
    )
    
    assert c.statement() == expected_report

def test_rent_multiple_regular_books():
    book1 = Book("Refactoring", Book.REGULAR)
    book2 = Book("Clean Code", Book.REGULAR)
    
    r1 = Rental(book1, 1)
    r2 = Rental(book2, 3)
    
    c = Client("Fulano")
    c.add_rental(r1)
    c.add_rental(r2)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Refactoring: 2\n"
        "- Clean Code: 3.5\n"
        "Total: 5.5\n"
        "Points: 2"
    )
    
    assert c.statement() == expected_report

def test_rent_children_book_short_duration():
    book = Book("Peter Pan", Book.CHILDREN)
    r = Rental(book, 2)

    c = Client("Fulano")
    c.add_rental(r)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Peter Pan: 1.5\n"
        "Total: 1.5\n"
        "Points: 1"
    )
    
    assert c.statement() == expected_report

def test_rent_children_book_long_duration():
    book = Book("Peter Pan", Book.CHILDREN)
    r = Rental(book, 4)

    c = Client("Fulano")
    c.add_rental(r)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Peter Pan: 3.0\n"
        "Total: 3.0\n"
        "Points: 1"
    )
    
    assert c.statement() == expected_report

def test_rent_multiple_children_books():
    book1 = Book("Peter Pan", Book.CHILDREN)
    book2 = Book("ABC", Book.CHILDREN)
    
    r1 = Rental(book1, 1)
    r2 = Rental(book2, 4)
    
    c = Client("Fulano")
    c.add_rental(r1)
    c.add_rental(r2)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Peter Pan: 1.5\n"
        "- ABC: 3.0\n"
        "Total: 4.5\n"
        "Points: 2"
    )
    
    assert c.statement() == expected_report

def test_rent_new_release_book_short_duration():
    book = Book("LLMs", Book.NEW_RELEASE)
    r = Rental(book, 1)

    c = Client("Fulano")
    c.add_rental(r)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- LLMs: 3\n"
        "Total: 3\n"
        "Points: 1"
    )
    
    assert c.statement() == expected_report

def test_rent_new_release_book_long_duration():
    book = Book("LLMs", Book.NEW_RELEASE)
    r = Rental(book, 2)

    c = Client("Fulano")
    c.add_rental(r)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- LLMs: 6\n"
        "Total: 6\n"
        "Points: 2"
    )
    
    assert c.statement() == expected_report

def test_rent_multiple_new_release_books():
    book1 = Book("LLMs", Book.NEW_RELEASE)
    book2 = Book("AWS", Book.NEW_RELEASE)
    
    r1 = Rental(book1, 2)
    r2 = Rental(book2, 5)
    
    c = Client("Fulano")
    c.add_rental(r1)
    c.add_rental(r2)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- LLMs: 6\n"
        "- AWS: 15\n"
        "Total: 21\n"
        "Points: 4"
    )
    
    assert c.statement() == expected_report

def test_rent_distinct_books_short_duration():
    book1 = Book("Refactoring", Book.REGULAR)
    book2 = Book("Peter Pan", Book.CHILDREN)
    book3 = Book("LLMs", Book.NEW_RELEASE)
    
    r1 = Rental(book1, 1)
    r2 = Rental(book2, 1)
    r3 = Rental(book3, 1)
    
    c = Client("Fulano")
    c.add_rental(r1)
    c.add_rental(r2)
    c.add_rental(r3)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Refactoring: 2\n"
        "- Peter Pan: 1.5\n"
        "- LLMs: 3\n"
        "Total: 6.5\n"
        "Points: 3"
    )
    
    assert c.statement() == expected_report

def test_rent_distinct_books_long_duration():
    book1 = Book("Refactoring", Book.REGULAR)
    book2 = Book("Peter Pan", Book.CHILDREN)
    book3 = Book("LLMs", Book.NEW_RELEASE)
    
    r1 = Rental(book1, 3)
    r2 = Rental(book2, 4)
    r3 = Rental(book3, 2)
    
    c = Client("Fulano")
    c.add_rental(r1)
    c.add_rental(r2)
    c.add_rental(r3)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Refactoring: 3.5\n"
        "- Peter Pan: 3.0\n"
        "- LLMs: 6\n"
        "Total: 12.5\n"
        "Points: 4"
    )
    
    assert c.statement() == expected_report
