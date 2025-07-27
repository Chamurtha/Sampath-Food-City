from datetime import datetime

class SalesService:
    def __init__(self, db_connection, branch_id, user_id):
        self.db_connection = db_connection
        self.branch_id = branch_id
        self.user_id = 1  # hardcoded for now; can change to user_id[0][0]

    def add_sales_item(self, bill_id) -> float:
        pcode = input("Enter Product Code: ")
        pqty = input("Enter Product Quantity: ")

        pdata = self.search_product_get_id_and_price(pcode)
        pid = pdata[0]
        pprice = pdata[1]
        ptotal = float(pprice) * float(pqty)

        pdata_stock = self.search_branch_product_for_stock(pid, self.branch_id)
        pb_id = pdata_stock[0]
        pb_qty_old = pdata_stock[1]
        pb_qty_new = float(pb_qty_old) - float(pqty)

        self.update_branch_product_for_stock(pb_id, pb_qty_new)

        self.db_connection.connect()
        sql = "INSERT INTO salesitem (billId, qty, price, total, branchproductid) VALUES (%s, %s, %s, %s, %s)"
        val = (bill_id, pqty, pprice, ptotal, pb_id)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()

        print("Sales item added successfully.")
        return ptotal

    def search_product_get_id_and_price(self, pcode) -> list:
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product WHERE pcode=%s", (pcode,))
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n-------------------------------")
            print(f" Product ID            : {x[0]}")
            print(f" Name                  : {x[1]}")
            print(f" Unit                  : {x[2]}")
            print(f" Price (Rs.)           : {x[3]}")
            print(f" Discount (%)          : {x[4]}")
            print(f" Price After Discount  : {x[5]}")
            print(f" Code                  : {x[6]}")
            print("-------------------------------")
            return [x[0], x[3]]

    def update_branch_product_for_stock(self, bpid, proqty):
        self.db_connection.connect()
        sql = "UPDATE branchproduct SET branchqty=%s WHERE bpid=%s"
        val = (proqty, bpid)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Branch stock quantity updated.")

    def search_branch_product_for_stock(self, pid, bid) -> list:
        pid = str(pid)
        bid = str(bid)

        self.db_connection.connect()
        self.db_connection.get_cursor().execute(
            "SELECT * FROM branchproduct WHERE productId=%s AND branchId=%s", (pid, bid)
        )
        results = self.db_connection.get_cursor().fetchall()
        for x in results:
            return [x[0], x[3]]

    def add_sales(self):
        print("\n--- Create New Sales Bill ---")
        bcode = input("Enter Bill Code         : ")
        bdis = float(input("Enter Discount (%)      : "))
        ptype = input("Enter Payment Method    : ")
        pcount = int(input("Enter No. of Product Types: "))

        bill_total = 0
        for _ in range(pcount):
            bill_total += self.add_sales_item(bcode)

        today_date = datetime.today().strftime("%Y-%m-%d")
        total_after_discount = bill_total - (bdis * bill_total)

        print(f"\nBill Total             : Rs. {bill_total:.2f}")
        print(f"Discount Applied       : {bdis * 100}%")
        print(f"Final Total            : Rs. {total_after_discount:.2f}")
        print(f"Date                   : {today_date}")

        self.db_connection.connect()
        sql = """
            INSERT INTO salesbill
            (billcode, billdate, billTotal, discount, totalAfterDiscount, paymentType, userId, branchid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (bcode, today_date, bill_total, bdis, total_after_discount, ptype, self.user_id, self.branch_id)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()

        print("New sales bill saved successfully.")

    def search_sales_bill_item(self, billcode):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM salesitem WHERE billId=%s", (billcode,))
        results = self.db_connection.get_cursor().fetchall()

        for idx, x in enumerate(results, start=1):
            print(f"\n--- Item {idx} ---")
            print(f" Branch Product ID      : {x[5]}")
            print(f" Quantity               : {x[2]}")
            print(f" Unit Price (Rs.)       : {x[3]}")
            print(f" Total (Rs.)            : {x[4]}")
            print("---------------------------")

    def search_sales_bill(self):
        print("\n--- Search Sales Bill ---")
        billcode = input("Enter Bill Code: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM salesbill WHERE billcode=%s", (billcode,))
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n---------------------------")
            print(f" Bill Code               : {x[0]}")
            print(f" Date                    : {x[1]}")
            print(f" Total Before Discount   : {x[2]}")
            print(f" Discount (%)            : {x[3]}")
            print(f" Final Total             : {x[4]}")
            print(f" Payment Type            : {x[5]}")
            print(f" Branch ID               : {x[6]}")
            print(f" Staff/User ID           : {x[7]}")
        self.search_sales_bill_item(billcode)
        print("End of bill details.")

    def show_all_bill_records_today(self):
        print("\n--- Today's Sales Bills ---")
        today_date = datetime.today().strftime("%Y-%m-%d")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM salesbill WHERE billdate=%s", (today_date,))
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n---------------------------")
            print(f" Bill Code               : {x[0]}")
            print(f" Date                    : {x[1]}")
            print(f" Branch ID               : {x[6]}")
            print(f" User ID                 : {x[7]}")
            print(f" Total                   : {x[2]}")
            print(f" Discount (%)            : {x[3]}")
            print(f" Final Amount            : {x[4]}")
            print("---------------------------")
        print("End of today's bills.")
