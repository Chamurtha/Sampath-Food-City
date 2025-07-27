class BranchProductService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_branch_product(self):
        print("\n--- Add Branch Product ---")
        bcode = input("Enter Branch Code       : ")
        proid = input("Enter Product ID        : ")
        proqty = input("Enter Product Quantity  : ")

        cursor = self.db_connection.get_cursor()
        sql = "INSERT INTO branchproduct (branchId, productId, branchqty) VALUES (%s, %s, %s)"
        val = (bcode, proid, proqty)
        cursor.execute(sql, val)
        self.db_connection.commit()
        print("Branch Product added successfully.")

    def search_branch_product(self):
        print("\n--- Search Branch Product by Branch Code ---")
        bcode = input("Enter Branch Code: ")
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branchproduct WHERE branchId=%s", (bcode,))
        results = cursor.fetchall()

        if results:
            for x in results:
                print("\n------------------------------")
                print(f" BranchProduct ID : {x[0]}")
                print(f" Branch ID        : {x[1]}")
                print(f" Product ID       : {x[2]}")
                print(f" Quantity         : {x[3]}")
                print("------------------------------")
        else:
            print("No records found.")
        print("End of search result.")

    def search_branch_product_by_product_id(self, pid, bid):
        pid = str(pid)
        bid = str(bid)
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branchproduct WHERE productId=%s AND branchId=%s", (pid, bid))
        myresult = cursor.fetchall()
        for x in myresult:
            return int(x[0])

    def search_branch_product_for_stock(self, pid, bid):
        pid = str(pid)
        bid = str(bid)
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branchproduct WHERE productId=%s AND branchId=%s", (pid, bid))
        myresult = cursor.fetchall()
        for x in myresult:
            pdata = [x[0], x[3]]
            return pdata

    def delete_branch_product(self):
        print("\n--- Delete Branch Product ---")
        bcode = input("Enter Branch Code : ")
        prid = input("Enter Product ID  : ")
        cursor = self.db_connection.get_cursor()
        sql = "DELETE FROM branchproduct WHERE branchId=%s AND productId=%s"
        cursor.execute(sql, (bcode, prid))
        self.db_connection.commit()
        if cursor.rowcount >= 1:
            print(f"{cursor.rowcount} record(s) deleted successfully.")
        else:
            print("No matching record found.")

    def update_branch_product(self):
        print("\n--- Update Branch Product Quantity ---")
        bcode = input("Enter Branch Code         : ")
        proid = input("Enter Product ID          : ")
        proqty = input("Enter New Product Quantity: ")

        cursor = self.db_connection.get_cursor()
        sql = "UPDATE branchproduct SET branchqty=%s WHERE branchId=%s AND productId=%s"
        val = (proqty, bcode, proid)
        cursor.execute(sql, val)
        self.db_connection.commit()
        print("Branch product quantity updated.")

    def update_branch_product_for_stock(self, bpid, proqty):
        cursor = self.db_connection.get_cursor()
        sql = "UPDATE branchproduct SET branchqty=%s WHERE bpid=%s"
        val = (proqty, bpid)
        cursor.execute(sql, val)
        self.db_connection.commit()
        print("Stock quantity updated for branch product.")

    def show_all_branch_products(self):
        print("\n--- All Branch Product Records ---")
        cursor = self.db_connection.get_cursor()
        cursor.execute("SELECT * FROM branchproduct")
        results = cursor.fetchall()

        if results:
            for x in results:
                print("\n---------------------------------------")
                print(f" Branch Product ID : {x[0]}")
                print(f" Branch ID         : {x[1]}")
                print(f" Product ID        : {x[2]}")
                print(f" Quantity          : {x[3]}")
                print("---------------------------------------")
        else:
            print("No branch product records found.")
        print("End of list.")
