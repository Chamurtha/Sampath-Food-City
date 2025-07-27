class BranchService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_branch(self):
        print("\n--- Add New Branch ---")
        bcode = input("Enter Branch Code         : ")
        bname = input("Enter Branch Name         : ")
        badd = input("Enter Branch Address      : ")
        bmanager = input("Enter Branch Manager Name : ")
        bemp = input("Enter Total Employees     : ")

        self.db_connection.connect()
        sql = "INSERT INTO branch (brid, branchName, address, branchManager, totalEmployees) VALUES (%s, %s, %s, %s, %s)"
        val = (bcode, bname, badd, bmanager, bemp)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        self.db_connection.close()

        print("Branch added successfully.")

    def delete_branch(self):
        print("\n--- Delete Branch ---")
        bcode = input("Enter Branch Code to Delete: ")
        self.db_connection.connect()
        sql = "DELETE FROM branch WHERE brid=%s"
        self.db_connection.get_cursor().execute(sql, (bcode,))
        self.db_connection.commit()
        if self.db_connection.get_cursor().rowcount >= 1:
            print(f"{self.db_connection.get_cursor().rowcount} branch record(s) deleted.")
        else:
            print("No matching branch found. Nothing deleted.")
        self.db_connection.close()

    def update_branch(self):
        print("\n--- Update Branch ---")
        bcode = input("Enter Branch Code         : ")
        bname = input("Enter New Branch Name     : ")
        badd = input("Enter New Address         : ")
        bmanager = input("Enter New Manager Name    : ")
        bemp = input("Enter Updated Employee Count: ")

        self.db_connection.connect()
        sql = "UPDATE branch SET branchName=%s, address=%s, branchManager=%s, totalEmployees=%s WHERE brid=%s"
        val = (bname, badd, bmanager, bemp, bcode)
        self.db_connection.get_cursor().execute(sql, val)
        self.db_connection.commit()
        self.db_connection.close()

        print("Branch information updated successfully.")

    def search_branch(self):
        print("\n--- Search Branch ---")
        bcode = input("Enter Branch Code: ")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM branch WHERE brid=%s", (bcode,))
        results = self.db_connection.get_cursor().fetchall()
        self.db_connection.close()

        if results:
            for branch in results:
                print("\n-------------------------------")
                print(f" Branch Code     : {branch[0]}")
                print(f" Name            : {branch[1]}")
                print(f" Address         : {branch[2]}")
                print(f" Manager         : {branch[3]}")
                print(f" Employee Count  : {branch[4]}")
                print("-------------------------------")
        else:
            print("No branch found with the provided code.")
        print("End of search result.")

    def show_all_branches(self):
        print("\n--- All Branch Records ---")
        self.db_connection.connect()
        self.db_connection.get_cursor().execute("SELECT * FROM branch")
        results = self.db_connection.get_cursor().fetchall()
        self.db_connection.close()

        if results:
            for branch in results:
                print("\n-------------------------------")
                print(f" Branch Code     : {branch[0]}")
                print(f" Name            : {branch[1]}")
                print(f" Address         : {branch[2]}")
                print(f" Manager         : {branch[3]}")
                print(f" Employee Count  : {branch[4]}")
                print("-------------------------------")
        else:
            print("No branches found.")
        print("End of branch list.")
