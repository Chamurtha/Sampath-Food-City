from datetime import datetime

class ProductService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def search_product(self):
        print("\n--- Search Product ---")
        pcode = input("Enter Product Code: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product WHERE pcode=%s", (pcode,))
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n-------------------------------")
            print(f" Product ID             : {x[0]}")
            print(f" Name                   : {x[1]}")
            print(f" Unit                   : {x[2]}")
            print(f" Price (Rs.)            : {x[3]}")
            print(f" Discount (%)           : {x[4]}")
            print(f" Price After Discount   : {x[5]}")
            print(f" Product Code           : {x[6]}")
            print("-------------------------------")
        print("End of search result.")

    def search_product_get_id_and_price(self, pcode) -> list:
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product WHERE pcode=%s", (pcode,))
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n-------------------------------")
            print(f" Product ID             : {x[0]}")
            print(f" Name                   : {x[1]}")
            print(f" Unit                   : {x[2]}")
            print(f" Price (Rs.)            : {x[3]}")
            print(f" Discount (%)           : {x[4]}")
            print(f" Price After Discount   : {x[5]}")
            print(f" Product Code           : {x[6]}")
            print("-------------------------------")
            return [x[0], x[3]]

    def show_all_products(self):
        print("\n--- All Product Records ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product")
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n-------------------------------")
            print(f" Product Code           : {x[6]}")
            print(f" ID                     : {x[0]}")
            print(f" Name                   : {x[1]}")
            print(f" Unit                   : {x[2]}")
            print(f" Price (Rs.)            : {x[3]}")
            print(f" Discount (%)           : {x[4]}")
            print(f" Price After Discount   : {x[5]}")
            print("-------------------------------")
        print("End of product list.")

    def update_product(self):
        print("\n--- Update Product ---")
        pcode = input("Enter Product Code: ")
        pname = input("Enter Product Name: ")
        unit = input("Enter Product Unit: ")
        price = float(input("Enter Product Price: "))
        discount = float(input("Enter Product Discount (%): "))
        price_after_discount = price - (discount * price)

        self.db_connection.connect()
        sql = "UPDATE product SET pname=%s, unit=%s, price=%s, discount=%s, priceAfterDiscount=%s WHERE pcode=%s"
        val = (pname, unit, price, discount, price_after_discount, pcode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()

        print("Product record updated successfully.")

    def add_product_price_level(self, pcode, price):
        today_date = datetime.today()
        start_date = today_date.strftime("%Y-%m-%d")

        self.db_connection.connect()
        sql = "INSERT INTO price (productId, price, startDate) VALUES (%s, %s, %s)"
        val = (pcode, price, start_date)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Price level recorded.")

    def update_product_price_level(self):
        print("\n--- Update Product Price ---")
        pcode = input("Enter Product Code: ")
        price = float(input("Enter New Product Price: "))

        self.db_connection.connect()
        sql = "UPDATE product SET price=%s WHERE pcode=%s"
        val = (price, pcode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Price updated in product table.")

        self.add_product_price_level(pcode, price)

    def price_analysis(self):
        print("\n--- Product Price Analysis Report ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("""
            SELECT  product.pname, price.productId, price.startDate, price.price, 
                    LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate) AS previous_price, 
                    (price.price - LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate)) AS price_change 
            FROM price 
            INNER JOIN product ON price.productId = product.pcode
        """)
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n-------------------------------")
            print(f" Product Code         : {x[1]}")
            print(f" Product Name         : {x[0]}")
            print(f" Start Date           : {x[2]}")
            print(f" Current Price        : {x[3]}")
            print(f" Previous Price       : {x[4]}")
            print(f" Price Change         : {x[5]}")
            print("-------------------------------")
        print("End of price analysis report.")

    def delete_product(self):
        print("\n--- Delete Product ---")
        pcode = input("Enter Product Code: ")
        self.db_connection.connect()
        sql = "DELETE FROM product WHERE pcode=%s"
        self.db_connection.get_cursor().execute(sql, (pcode,))
        self.db_connection.commit()
        if self.db_connection.get_cursor().rowcount >= 1:
            print("Product deleted successfully.")
        else:
            print("No product found with that code.")

    def add_branch_product_for_new_product(self, bcode, proid):
        proqty = "0"
        self.db_connection.connect()
        sql = "INSERT INTO branchproduct (branchId, productId, branchqty) VALUES (%s, %s, %s)"
        val = (bcode, proid, proqty)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print(f"Product assigned to branch {bcode} with 0 quantity.")

    def all_branch_product_for_new_product(self, pcode):
        pdata = self.search_product_get_id_and_price(pcode)
        proid = pdata[0]
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM branch")
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print(f"Assigning product to branch {x[0]} - {x[1]}")
            bcode = x[0]
            self.add_branch_product_for_new_product(bcode, proid)

# Clean Coding Techniques


    def add_product(self):
        print("\n--- Add New Product ---")
        pcode = input("Enter Product Code: ")
        pname = input("Enter Product Name: ")
        unit = input("Enter Product Unit: ")
        price = float(input("Enter Product Price: "))
        discount = float(input("Enter Discount (%): "))
        price_after_discount = price - (discount * price)

        self.db_connection.connect()
        sql = "INSERT INTO product (pname, unit, price, discount, priceAfterDiscount, pcode) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (pname, unit, price, discount, price_after_discount, pcode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("New product added successfully.")

        self.add_product_price_level(pcode, price)
        self.all_branch_product_for_new_product(pcode)
