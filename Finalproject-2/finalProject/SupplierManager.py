class SupplierService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def search_supplier(self):
        print("\n--- Search Supplier ---")
        sid = input("Enter Supplier ID: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM supplier WHERE supid=%s", (sid,))
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n----------------------------")
            print(f" Supplier ID     : {x[0]}")
            print(f" Name            : {x[1]}")
            print(f" Address         : {x[2]}")
            print(f" NIC             : {x[3]}")
            print(f" Telephone       : {x[4]}")
            print(f" Email           : {x[5]}")
            print("----------------------------")
        print("End of supplier search.")

    def show_all_supplier_details(self):
        print("\n--- All Supplier Records ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM supplier")
        results = self.db_connection.get_cursor().fetchall()

        for x in results:
            print("\n----------------------------")
            print(f" Supplier ID     : {x[0]}")
            print(f" Name            : {x[1]}")
            print(f" Address         : {x[2]}")
            print(f" NIC             : {x[3]}")
            print(f" Telephone       : {x[4]}")
            print(f" Email           : {x[5]}")
            print("----------------------------")
        print("End of supplier list.")

    def update_supplier(self):
        print("\n--- Update Supplier ---")
        sid = input("Enter Supplier ID       : ")
        supname = input("Enter Name              : ")
        sup_address = input("Enter Address           : ")
        sup_nic = input("Enter NIC               : ")
        sup_tel = input("Enter Telephone         : ")
        sup_email = input("Enter Email             : ")

        self.db_connection.connect()
        sql = """
            UPDATE supplier 
            SET supName=%s, supAddress=%s, supNic=%s, supTel=%s, supEmail=%s 
            WHERE supid=%s
        """
        val = (supname, sup_address, sup_nic, sup_tel, sup_email, sid)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()

        print("Supplier information updated successfully.")

    def delete_supplier(self):
        print("\n--- Delete Supplier ---")
        sid = input("Enter Supplier ID: ")
        self.db_connection.connect()
        sql = "DELETE FROM supplier WHERE supid=%s"
        self.db_connection.get_cursor().execute(sql, (sid,))
        self.db_connection.commit()

        if self.db_connection.get_cursor().rowcount >= 1:
            print(f"{self.db_connection.get_cursor().rowcount} supplier record deleted successfully.")
        else:
            print("No matching supplier found to delete.")

    def add_supplier(self):
        print("\n--- Add New Supplier ---")
        supname = input("Enter Name              : ")
        sup_address = input("Enter Address           : ")
        sup_nic = input("Enter NIC               : ")
        sup_tel = input("Enter Telephone         : ")
        sup_email = input("Enter Email             : ")

        self.db_connection.connect()
        sql = """
            INSERT INTO supplier (supName, supAddress, supNic, supTel, supEmail) 
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (supname, sup_address, sup_nic, sup_tel, sup_email)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()

        print("New supplier added to the system successfully.")
