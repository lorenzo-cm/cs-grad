class Book:

    REGULAR: int = 0
    NEW_RELEASE: int = 1
    CHILDREN: int = 2

    def __init__(self, title: str, price_code: int):
        self.title = title
        self.price_code = price_code

class Rental:
    def __init__(self, book: Book, days_rented: int):
        self.book = book
        self.days_rented = days_rented

class Client:

    def __init__(self, name: str):
        self.name = name
        self.rentals = []

    def add_rental(self, rental: Rental):
        self.rentals.append(rental)

    def statement(self) -> str:

        total_amount = 0
        frequent_renter_points = 0
        result = f"Rental summary for {self.name}\n"
        
        for rental in self.rentals:
            amount = 0
            
            # determine amounts for each line
            if rental.book.price_code == Book.REGULAR:
                amount += 2
                if rental.days_rented > 2:
                    amount += (rental.days_rented - 2) * 1.5
            elif rental.book.price_code == Book.NEW_RELEASE:
                amount += rental.days_rented * 3
            elif rental.book.price_code == Book.CHILDREN:
                amount += 1.5
                if rental.days_rented > 3:
                    amount += (rental.days_rented - 3) * 1.5

            # add frequent renter points
            frequent_renter_points += 1
            if rental.book.price_code == Book.NEW_RELEASE and rental.days_rented > 1:
                frequent_renter_points += 1

            # show each rental result
            result += f"- {rental.book.title}: {amount}\n"
            total_amount += amount
        
        # show total result
        result += f"Total: {total_amount}\n"
        result += f"Points: {frequent_renter_points}"
        return result