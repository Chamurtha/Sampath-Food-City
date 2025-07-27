from DBConnection import DatabaseConnection, AuthenticationService
from BranchManager import BranchService
from ProductManager import ProductService
from BranchProductManger import BranchProductService
from SalesManager import SalesService
from SupplierManager import SupplierService
from StockManager import StockService
from ReportManager import ReportService

def main_menu():
    db_connection = DatabaseConnection()
    db_connection.connect()

    auth_service = AuthenticationService(db_connection)
    product_service = ProductService(db_connection)
    branch_service = BranchService(db_connection)
    branch_product_service = BranchProductService(db_connection)
    supplier_service = SupplierService(db_connection)
    report_service = ReportService(db_connection)

    username = input("Enter username: ")
    password = input("Enter password: ")
    mybranch_id = 1

    user = auth_service.authenticate(username, password)
    sales_service = SalesService(db_connection, mybranch_id, user)
    stock_service = StockService(db_connection, mybranch_id, user)

    if user:
        print("\n===============================================================")
        print("                SAMPATH FOOD CITY - MAIN MENU                  ")
        print("===============================================================")
        while True:
            print("\n+-------------------------------------------------------------+")
            print("| OPTION |                 FUNCTION                           |")
            print("+--------+----------------------------------------------------+")
            print("|   1    | Manage Product Details                             |")
            print("|   2    | Manage Sales Details                               |")
            print("|   3    | Manage Branch Details                              |")
            print("|   4    | Manage Stock Details                               |")
            print("|   5    | Manage Branch Product Details                      |")
            print("|   6    | Manage Supplier Details                            |")
            print("|   7    | Reports                                            |")
            print("|   8    | Exit                                               |")
            print("+-------------------------------------------------------------+")
            choice = input("Select an option (1–8): ")

            if choice == "1":
                manage_products(product_service)
            elif choice == "2":
                manage_sales(sales_service)
            elif choice == "3":
                manage_branch(branch_service)
            elif choice == "4":
                manage_stock_details(stock_service)
            elif choice == "5":
                manage_branch_product(branch_product_service)
            elif choice == "6":
                manage_supplier_details(supplier_service)
            elif choice == "7":
                manage_reports(report_service)
            elif choice == "8":
                print("\nSystem exiting... Thank you for using Sampath Food City.")
                break
            else:
                print("Invalid option. Please enter a number between 1 and 8.")
    else:
        print("Login failed. Invalid username or password.")

    db_connection.close()

def manage_products(product_service):
    print("\n================= PRODUCT MANAGEMENT =================")
    print("| 1 - Add a New Product                              |")
    print("| 2 - Find an Existing Product                       |")
    print("| 3 - Remove a Product from the System               |")
    print("| 4 - Modify Product Information                     |")
    print("| 5 - Change Product Pricing                         |")
    print("| 6 - Display All Available Products                 |")
    print("| 7 - Return to the Main Menu                        |")
    print("======================================================")

    choice = input("Select an option (1–7): ")

    if choice == "1":
        print("Opening Add Product Interface...")
        product_service.add_product()
        manage_products(product_service)
    elif choice == "2":
        print("Opening Product Search...")
        product_service.search_product()
        manage_products(product_service)
    elif choice == "3":
        print("Opening Delete Product Interface...")
        product_service.delete_product()
        manage_products(product_service)
    elif choice == "4":
        print("Opening Update Product Details...")
        product_service.update_product()
        manage_products(product_service)
    elif choice == "5":
        print("Opening Product Price Update...")
        product_service.update_product_price_level()
        manage_products(product_service)
    elif choice == "6":
        print("Retrieving All Product Records...")
        product_service.show_all_products()
        manage_products(product_service)
    elif choice == "7":
        print("Returning to Main Menu...")
    else:
        print("Invalid selection. Please choose a number from 1 to 7.")
        manage_products(product_service)

def manage_branch(branch_service):
    print("\n================= BRANCH MANAGEMENT =================")
    print("| 1 - Add New Branch Information                    |")
    print("| 2 - Search for a Branch                           |")
    print("| 3 - Delete an Existing Branch                     |")
    print("| 4 - Update Branch Details                         |")
    print("| 5 - Display All Branches                          |")
    print("| 6 - Return to the Main Menu                       |")
    print("=====================================================")

    choice = input("Select an option (1–6): ")

    if choice == "1":
        print("Opening Add Branch Form...")
        branch_service.add_branch()
        manage_branch(branch_service)
    elif choice == "2":
        print("Searching Branch Records...")
        branch_service.search_branch()
        manage_branch(branch_service)
    elif choice == "3":
        print("Proceeding to Delete Branch...")
        branch_service.delete_branch()
        manage_branch(branch_service)
    elif choice == "4":
        print("Opening Branch Update Module...")
        branch_service.update_branch()
        manage_branch(branch_service)
    elif choice == "5":
        print("Retrieving All Branches...")
        branch_service.show_all_branches()
        manage_branch(branch_service)
    elif choice == "6":
        print("Returning to Main Menu...")
    else:
        print("Invalid input. Please select a number between 1 and 6.")
        manage_branch(branch_service)

def print_product(product):
    print("\n--------------------------------------------------")
    print(" Product Details")
    print("--------------------------------------------------")
    print(f" Product Code             : {product[0]}")
    print(f" Product Name             : {product[1]}")
    print(f" Unit                     : {product[2]}")
    print(f" Price (Rs.)             : {product[3]}")
    print(f" Discount (%)            : {product[4]}")
    print(f" Price After Discount    : {product[5]}")
    print("--------------------------------------------------")

def print_branch(branch):
    print("\n--------------------------------------------------")
    print(" Branch Information")
    print("--------------------------------------------------")
    print(f" Branch ID               : {branch[0]}")
    print(f" Branch Name             : {branch[1]}")
    print(f" Address                 : {branch[2]}")
    print(f" Manager Name            : {branch[3]}")
    print(f" Total Employees         : {branch[4]}")
    print("--------------------------------------------------")


def manage_branch_product(branch_product_service):
    print("\n============= BRANCH PRODUCT MANAGEMENT =============")
    print("| 1 - Assign Product to Branch                       |")
    print("| 2 - Search Branch Product Details                  |")
    print("| 3 - Remove Product from Branch                     |")
    print("| 4 - Update Branch Product Info                     |")
    print("| 5 - List All Branch Products                       |")
    print("| 6 - Return to Main Menu                            |")
    print("======================================================")

    choice = input("Select an option (1–6): ")

    if choice == "1":
        print("Adding Product to Branch...")
        branch_product_service.add_branch_product()
        manage_branch_product(branch_product_service)
    elif choice == "2":
        print("Searching Branch Product Records...")
        branch_product_service.search_branch_product()
        manage_branch_product(branch_product_service)
    elif choice == "3":
        print("Removing Product from Branch...")
        branch_product_service.delete_branch_product()
        manage_branch_product(branch_product_service)
    elif choice == "4":
        print("Updating Branch Product Info...")
        branch_product_service.update_branch_product()
        manage_branch_product(branch_product_service)
    elif choice == "5":
        print("Displaying All Branch Product Records...")
        branch_product_service.show_all_branch_products()
        manage_branch_product(branch_product_service)
    elif choice == "6":
        print("Returning to Main Menu...")
    else:
        print("Invalid option. Please enter a number from 1 to 6.")
        manage_branch_product(branch_product_service)


def manage_sales(sales_service):
    print("\n================= SALES MANAGEMENT =================")
    print("| 1 - Record a New Sale                            |")
    print("| 2 - View a Specific Sales Bill                   |")
    print("| 3 - View All Sales Bills for Today               |")
    print("| 4 - Return to the Main Menu                      |")
    print("====================================================")

    choice = input("Select an option (1–4): ")

    if choice == "1":
        print("Redirecting to Add Sales Entry...")
        sales_service.add_sales()
        manage_sales(sales_service)
    elif choice == "2":
        print("Opening Search for Sales Bill...")
        sales_service.search_sales_bill()
        manage_sales(sales_service)
    elif choice == "3":
        print("Displaying Today's Sales Bills...")
        sales_service.show_all_bill_records_today()
        manage_sales(sales_service)
    elif choice == "4":
        print("Returning to Main Menu...")
    else:
        print("Invalid selection. Please enter a number from 1 to 4.")
        manage_sales(sales_service)


def manage_supplier_details(supplier_service):
    print("\n================= SUPPLIER MANAGEMENT =================")
    print("| 1 - Add New Supplier                                 |")
    print("| 2 - Search for Supplier                              |")
    print("| 3 - Delete a Supplier                                |")
    print("| 4 - Update Supplier Details                          |")
    print("| 5 - View All Suppliers                               |")
    print("| 6 - Return to Main Menu                              |")
    print("========================================================")

    choice = input("Select an option (1–6): ")

    if choice == "1":
        print("Opening Add Supplier Module...")
        supplier_service.add_supplier()
        manage_supplier_details(supplier_service)
    elif choice == "2":
        print("Searching Supplier Records...")
        supplier_service.search_supplier()
        manage_supplier_details(supplier_service)
    elif choice == "3":
        print("Proceeding to Delete Supplier...")
        supplier_service.delete_supplier()
        manage_supplier_details(supplier_service)
    elif choice == "4":
        print("Opening Supplier Update Module...")
        supplier_service.update_supplier()
        manage_supplier_details(supplier_service)
    elif choice == "5":
        print("Displaying All Suppliers...")
        supplier_service.show_all_supplier_details()
        manage_supplier_details(supplier_service)
    elif choice == "6":
        print("Returning to Main Menu...")
    else:
        print("Invalid input. Please select a number from 1 to 6.")
        manage_supplier_details(supplier_service)


def manage_stock_details(stock_service):
    print("\n================= STOCK MANAGEMENT =================")
    print("| 1 - Add New Stock Record                          |")
    print("| 2 - Search GRN Details                            |")
    print("| 3 - View Today's GRN Records                      |")
    print("| 4 - Update GRN Payment Information                |")
    print("| 5 - Return to Main Menu                           |")
    print("====================================================")

    choice = input("Select an option (1–5): ")

    if choice == "1":
        print("Opening Add Stock Module...")
        stock_service.add_stock_details()
        manage_stock_details(stock_service)
    elif choice == "2":
        print("Searching GRN Details...")
        stock_service.search_stock_grn_details()
        manage_stock_details(stock_service)
    elif choice == "3":
        print("Showing Today's GRN Records...")
        stock_service.show_all_stock_grn_records_today()
        manage_stock_details(stock_service)
    elif choice == "4":
        print("Updating GRN Payment Info...")
        stock_service.update_stock_grn_payment()
        manage_stock_details(stock_service)
    elif choice == "5":
        print("Returning to Main Menu...")
    else:
        print("Invalid input. Please select a number from 1 to 5.")
        manage_stock_details(stock_service)


def manage_reports(report_service):
    print("\n================= REPORTING & ANALYTICS =================")
    print("| 1 - Monthly Sales Analysis by Branch                   |")
    print("| 2 - Product Price Evaluation                           |")
    print("| 3 - Weekly Sales Summary (All Branches)                |")
    print("| 4 - Product Preference Insights                        |")
    print("| 5 - Total Sales Value Distribution                     |")
    print("| 6 - Return to Main Menu                                |")
    print("==========================================================")

    choice = input("Select a report option (1–6): ")

    if choice == "1":
        print("Generating Monthly Sales Report...")
        report_service.monthly_sales_analysis()
        manage_reports(report_service)
    elif choice == "2":
        print("Generating Product Price Analysis...")
        report_service.price_analysis()
        manage_reports(report_service)
    elif choice == "3":
        print("Compiling Weekly Sales Summary...")
        report_service.weekly_sales_analysis()
        manage_reports(report_service)
    elif choice == "4":
        print("Analyzing Product Preferences...")
        report_service.sales_product_preferences()
        manage_reports(report_service)
    elif choice == "5":
        print("Generating Sales Distribution Overview...")
        report_service.final_sales_analysis()
        manage_reports(report_service)
    elif choice == "6":
        print("Returning to Main Menu...")
    else:
        print("Invalid input. Please enter a number between 1 and 6.")
        manage_reports(report_service)


if __name__ == "__main__":
    main_menu()

# ---------------------------------------------End-------------------------------------------------


