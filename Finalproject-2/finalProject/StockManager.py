from datetime import datetime

class StockService:
    def __init__(self, db_connection, branch_id, user_id):
        self.db_connection = db_connection
        self.branch_id = branch_id
        self.user_id = 1  # or use: user_id[0][0]

    def search_product_get_id_and_price(self, pcode) -> list:
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM product WHERE pcode=%s", (pcode,))
        results = self.db_connection.get_cursor().fetchall()
        for x in results:
            print("\n------------------------------")
            print(f" Product ID        : {x[0]}")
            print(f" Name              : {x[1]}")
            print(f" Unit              : {x[2]}")
            print(f" Price (Rs.)       : {x[3]}")
            print(f" Discount (%)      : {x[4]}")
            print(f" Final Price       : {x[5]}")
            print(f" Product Code      : {x[6]}")
            print("------------------------------")
            return [x[0], x[3]]

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

    def update_branch_product_for_stock(self, bpid, proqty):
        self.db_connection.connect()
        sql = "UPDATE branchproduct SET branchqty=%s WHERE bpid=%s"
        self.db_connection.get_cursor().execute(sql, (proqty, bpid))
        self.db_connection.commit()
        print("Stock quantity updated for branch product.")

    def add_stock_item(self, grn_id) -> float:
        print("\n--- Add Stock Item ---")
        pcode = input("Enter Product Code    : ")
        pqty = input("Enter Quantity        : ")
        pprice = input("Enter Stock Price     : ")
        ex_date = input("Enter Expiry Date     : ")
        mf_date = input("Enter Manufacture Date: ")

        pdata = self.search_product_get_id_and_price(pcode)
        pid = pdata[0]
        total = float(pprice) * float(pqty)

        pdata = self.search_branch_product_for_stock(pid, self.branch_id)
        pb_id = pdata[0]
        pb_qty_old = pdata[1]
        pb_qty_new = float(pb_qty_old) + float(pqty)

        self.update_branch_product_for_stock(pb_id, pb_qty_new)

        self.db_connection.connect()
        sql = """
            INSERT INTO stockitem (qty, stockPrice, expDate, mfDate, grnBillNo, branchproductid)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (pqty, pprice, ex_date, mf_date, grn_id, pb_id)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("Stock item added successfully.")
        return total

    def search_stock_grn_item_details(self, billcode):
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM stockitem WHERE grnBillNo=%s", (billcode,))
        results = self.db_connection.get_cursor().fetchall()
        for count, x in enumerate(results, start=1):
            total = float(x[2]) * float(x[1])
            print(f"\n--- GRN Item {count} ---")
            print(f" Branch Product ID : {x[6]}")
            print(f" Quantity           : {x[1]}")
            print(f" Unit Price (Rs.)   : {x[2]}")
            print(f" Total              : {total}")
            print(f" Expiry Date        : {x[3]}")
            print(f" Manufacture Date   : {x[4]}")
            print("---------------------------")

    def search_stock_grn_details(self):
        print("\n--- Search GRN Record ---")
        grncode = input("Enter GRN Bill Code: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM grn WHERE grnBillNo=%s", (grncode,))
        results = self.db_connection.get_cursor().fetchall()
        for x in results:
            print("\n---------------------------")
            print(f" GRN Code              : {x[1]}")
            print(f" Date                  : {x[3]}")
            print(f" Total                 : {x[2]}")
            print(f" Discount              : {x[4]}")
            print(f" Final Bill Amount     : {x[5]}")
            print(f" Paid Amount           : {x[6]}")
            print(f" Payment Status        : {x[7]}")
            print(f" Supplier ID           : {x[8]}")
            print("---------------------------")
        self.search_stock_grn_item_details(grncode)
        print("End of GRN Record.")

    def add_stock_details(self):
        print("\n--- Add Stock GRN Entry ---")
        grncode = input("Enter GRN Code        : ")
        supid = input("Enter Supplier ID     : ")
        stock_dis = float(input("Enter Discount (%)    : "))
        paid_amount = float(input("Enter Paid Amount     : "))
        pcount = int(input("Enter No. of Products : "))

        total = 0
        for _ in range(pcount):
            total += self.add_stock_item(grncode)

        bill_date = datetime.today().strftime("%Y-%m-%d")
        final_total = total - (stock_dis * total)
        status = "Payment Complete" if final_total == paid_amount else "Payment Not Complete"

        self.db_connection.connect()
        sql = """
            INSERT INTO grn (grnBillNo, total, date, discount, totalAfterDiscount, paidAmount, status, supplierId)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (grncode, total, bill_date, stock_dis, final_total, paid_amount, status, supid)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        print("New GRN record added successfully.")

    def show_all_stock_grn_records_today(self):
        print("\n--- Today's GRN Records ---")
        bill_date = datetime.today().strftime("%Y-%m-%d")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM grn WHERE date=%s", (bill_date,))
        results = self.db_connection.get_cursor().fetchall()
        for x in results:
            print("\n---------------------------")
            print(f" GRN Code              : {x[1]}")
            print(f" Date                  : {x[3]}")
            print(f" Total Amount          : {x[2]}")
            print(f" Discount              : {x[4]}")
            print(f" Final Amount          : {x[5]}")
            print(f" Paid Amount           : {x[6]}")
            print(f" Payment Status        : {x[7]}")
            print(f" Supplier ID           : {x[8]}")
            print("---------------------------")
        print("End of today's GRNs.")

    def search_stock_grn_payment_details(self, billcode) -> list:
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM grn WHERE grnBillNo=%s", (billcode,))
        result = self.db_connection.get_cursor().fetchall()
        for x in result:
            return [x[6], x[5]]  # paidAmount, totalAfterDiscount

    def update_stock_grn_payment(self):
        print("\n--- Update GRN Payment ---")
        grncode = input("Enter GRN Code: ")
        new_payment = float(input("Enter New Payment Amount: "))

        previous = self.search_stock_grn_payment_details(grncode)
        old_paid = previous[0]
        bill_total = previous[1]
        updated_paid = float(old_paid) + new_payment

        status = "Payment Complete" if updated_paid == bill_total else "Payment Not Complete"

        self.db_connection.connect()
        sql = "UPDATE grn SET paidAmount=%s, status=%s WHERE grnBillNo=%s"
        self.db_connection.get_cursor().execute(sql, (updated_paid, status, grncode))
        self.db_connection.commit()
        print("GRN payment updated successfully.")
