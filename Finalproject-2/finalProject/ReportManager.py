from datetime import datetime

class ReportService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def show_all_bill_records_today(self):
        print("\n--- Today's Sales Bills ---")
        today_date = datetime.today()
        bill_date = today_date.strftime("%Y-%m-%d")

        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM salesbill WHERE billdate=%s", (bill_date,))
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n--------------------------------------")
            print(f" Bill Code            : {x[0]}")
            print(f" Date                 : {x[1]}")
            print(f" Total Amount         : {x[2]}")
            print(f" Discount             : {x[3]}")
            print(f" Final Amount         : {x[4]}")
            print(f" Branch ID            : {x[6]}")
            print(f" User ID              : {x[7]}")
            print("--------------------------------------")
        print("End of today's sales records.")

    def price_analysis(self):
        print("\n--- Product Price Analysis ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("""
            SELECT product.pname, price.productId, price.startDate, price.price,
                   LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate) AS previous_price,
                   (price.price - LAG(price.price) OVER (PARTITION BY price.productId ORDER BY price.startDate)) AS price_change
            FROM price
            INNER JOIN product ON price.productId = product.pcode
        """)
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n--------------------------------------")
            print(f" Product Code         : {x[1]}")
            print(f" Product Name         : {x[0]}")
            print(f" Date Applied         : {x[2]}")
            print(f" Current Price (Rs.)  : {x[3]}")
            print(f" Previous Price       : {x[4]}")
            print(f" Price Change         : {x[5]}")
            print("--------------------------------------")
        print("End of price change report.")

    def monthly_sales_analysis(self):
        print("\n--- Monthly Sales Summary by Branch ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("""
            SELECT branchid, YEAR(billdate) AS year, MONTH(billdate) AS month,
                   SUM(billTotal) AS total_bill
            FROM salesbill
            GROUP BY branchid, YEAR(billdate), MONTH(billdate)
            ORDER BY branchid, year, month
        """)
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n--------------------------------------")
            print(f" Branch ID            : {x[0]}")
            print(f" Year                 : {x[1]}")
            print(f" Month                : {x[2]}")
            print(f" Total Sales (Rs.)    : {x[3]}")
            print("--------------------------------------")
        print("End of monthly summary.")

    def weekly_sales_analysis(self):
        print("\n--- Weekly Sales Summary by Branch ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("""
            SELECT salesbill.branchid, branch.branchName,
                   YEAR(salesbill.billdate) AS year,
                   WEEK(salesbill.billdate) AS week,
                   SUM(salesbill.billTotal) AS total_sales
            FROM salesbill
            INNER JOIN branch ON salesbill.branchid = branch.brid
            GROUP BY salesbill.branchid, year, week
            ORDER BY salesbill.branchid, year, week
        """)
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n--------------------------------------")
            print(f" Branch ID            : {x[0]}")
            print(f" Branch Name          : {x[1]}")
            print(f" Year                 : {x[2]}")
            print(f" Week                 : {x[3]}")
            print(f" Weekly Total Sales   : {x[4]}")
            print("--------------------------------------")
        print("End of weekly summary.")

    def sales_product_preferences(self):
        print("\n--- Product Sales Preference Report ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("""
            SELECT si.branchproductid,
                   SUM(si.qty) AS total_quantity_sold,
                   COUNT(DISTINCT si.billId) AS number_of_sales,
                   SUM(si.total) AS total_revenue
            FROM salesitem si
            JOIN salesbill yt ON si.billId = yt.billcode
            GROUP BY si.branchproductid
            ORDER BY total_quantity_sold DESC
        """)
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n--------------------------------------")
            print(f" Branch Product ID     : {x[0]}")
            print(f" Quantity Sold         : {x[1]}")
            print(f" No. of Bills          : {x[2]}")
            print(f" Total Revenue (Rs.)   : {x[3]}")
            print("--------------------------------------")
        print("End of product preference report.")

    def final_sales_analysis(self):
        print("\n--- Total Sales Distribution by Branch ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("""
            SELECT branchid,
                   COUNT(billcode) AS number_of_sales,
                   SUM(total_sales) AS total_sales_amount,
                   AVG(total_sales) AS average_sales_amount,
                   MIN(total_sales) AS minimum_sales_amount,
                   MAX(total_sales) AS maximum_sales_amount
            FROM (
                SELECT billcode, branchid, SUM(billTotal) AS total_sales
                FROM salesbill
                GROUP BY billcode, branchid
            ) AS sales_per_bill
            GROUP BY branchid
            ORDER BY branchid
        """)
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n--------------------------------------")
            print(f" Branch ID              : {x[0]}")
            print(f" No. of Sales           : {x[1]}")
            print(f" Total Sales (Rs.)      : {x[2]}")
            print(f" Minimum Sale (Rs.)     : {x[4]}")
            print(f" Average Sale (Rs.)     : {x[3]}")
            print(f" Maximum Sale (Rs.)     : {x[5]}")
            print("--------------------------------------")
        print("End of final sales analysis.")
