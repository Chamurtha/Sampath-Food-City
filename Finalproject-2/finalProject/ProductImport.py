import json
import os
from DBConnection import DatabaseConnection
from decimal import Decimal, InvalidOperation


class ProductImporter:
    def __init__(self):
        self.db_connection = DatabaseConnection()
        self.required_fields = ['pname', 'unit', 'price', 'discount', 'priceAfterDiscount', 'pcode']
        self.valid_units = ['kg', 'liter', 'piece', 'dozen', 'box', 'gram', 'ml', 'pack']
    
    def validate_file_exists(self, filename):
        """Check if the file exists in the current directory"""
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found in the current directory.")
            return False
        return True
    
    def validate_json_format(self, filename):
        """Validate if the file is a valid JSON format"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in file '{filename}'.")
            print(f"JSON Error: {e}")
            return None
        except Exception as e:
            print(f"Error: Unable to read file '{filename}'.")
            print(f"Error details: {e}")
            return None
    
    def validate_data_structure(self, data):
        """Validate the structure of the JSON data"""
        if not isinstance(data, dict):
            print("Error: JSON data must be a dictionary/object.")
            return False
        
        if 'products' not in data:
            print("Error: JSON data must contain a 'products' array.")
            return False
        
        if not isinstance(data['products'], list):
            print("Error: 'products' must be an array/list.")
            return False
        
        if len(data['products']) == 0:
            print("Error: Products array is empty.")
            return False
        
        return True
    
    def validate_product_data(self, products):
        """Validate individual product data"""
        valid_products = []
        errors = []
        
        for i, product in enumerate(products, 1):
            product_errors = []
            
            # Check required fields
            for field in self.required_fields:
                if field not in product or product[field] is None:
                    product_errors.append(f"Missing required field: {field}")
            
            if product_errors:
                errors.append(f"Product {i}: {', '.join(product_errors)}")
                continue
            
            # Validate data types and values
            try:
                # Validate pname (product name)
                if not isinstance(product['pname'], str) or len(product['pname'].strip()) == 0:
                    product_errors.append("Product name must be a non-empty string")
                
                # Validate unit
                if not isinstance(product['unit'], str) or product['unit'].lower() not in self.valid_units:
                    product_errors.append(f"Unit must be one of: {', '.join(self.valid_units)}")
                
                # Validate price
                price = Decimal(str(product['price']))
                if price < 0:
                    product_errors.append("Price cannot be negative")
                
                # Validate discount
                discount = Decimal(str(product['discount']))
                if discount < 0:
                    product_errors.append("Discount cannot be negative")
                
                # Validate priceAfterDiscount
                price_after_discount = Decimal(str(product['priceAfterDiscount']))
                if price_after_discount < 0:
                    product_errors.append("Price after discount cannot be negative")
                
                # Validate pcode (product code)
                if not isinstance(product['pcode'], str) or len(product['pcode']) > 20:
                    product_errors.append("Product code must be a string with max 20 characters")
                
                # Validate price calculation
                expected_price = price - (price * discount / 100)
                if abs(float(price_after_discount) - float(expected_price)) > 0.01:
                    product_errors.append("Price after discount calculation is incorrect")
                
            except (ValueError, InvalidOperation, TypeError) as e:
                product_errors.append(f"Invalid data type: {e}")
            
            if product_errors:
                errors.append(f"Product {i} ({product.get('pname', 'Unknown')}): {', '.join(product_errors)}")
            else:
                valid_products.append(product)
        
        return valid_products, errors
    
    def check_duplicate_codes(self, products):
        """Check for duplicate product codes in the import data"""
        codes = [product['pcode'] for product in products]
        duplicates = []
        seen = set()
        
        for code in codes:
            if code in seen:
                duplicates.append(code)
            seen.add(code)
        
        return duplicates
    
    def check_existing_codes_in_db(self, products):
        """Check if product codes already exist in database"""
        try:
            cursor = self.db_connection.get_cursor()
            existing_codes = []
            
            for product in products:
                cursor.execute("SELECT pcode FROM product WHERE pcode = %s", (product['pcode'],))
                if cursor.fetchone():
                    existing_codes.append(product['pcode'])
            
            return existing_codes
        except Exception as e:
            print(f"Error checking existing codes: {e}")
            return []
    
    def import_products_to_database(self, products):
        """Import validated products to database"""
        success_count = 0
        failed_imports = []
        
        try:
            cursor = self.db_connection.get_cursor()
            
            for product in products:
                try:
                    # Insert product (pid is auto-increment, so we don't include it)
                    cursor.execute("""
                        INSERT INTO product (pname, unit, price, discount, priceAfterDiscount, pcode)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        product['pname'],
                        product['unit'],
                        product['price'],
                        product['discount'],
                        product['priceAfterDiscount'],
                        product['pcode']
                    ))
                    success_count += 1
                    
                except Exception as e:
                    failed_imports.append(f"Product '{product['pname']}' ({product['pcode']}): {e}")
            
            # Commit all successful imports
            self.db_connection.commit()
            
        except Exception as e:
            print(f"Database error during import: {e}")
            # MySQL connector doesn't have rollback on connection, we'll handle it differently
            return 0, [f"Database transaction failed: {e}"]
        
        return success_count, failed_imports
    
    def run_import(self):
        """Main import process"""
        print("=" * 50)
        print("         PRODUCT IMPORT SYSTEM")
        print("=" * 50)
        
        # Get filename from user
        filename = input("Enter JSON file name (e.g., Test_sample_products.json): ").strip()
        
        if not filename:
            print("Error: No filename provided.")
            return
        
        print(f"\nProcessing file: {filename}")
        print("-" * 30)
        
        # Step 1: Check if file exists
        if not self.validate_file_exists(filename):
            return
        
        # Step 2: Validate JSON format and load data
        data = self.validate_json_format(filename)
        if data is None:
            return
        
        # Step 3: Validate data structure
        if not self.validate_data_structure(data):
            return
        
        products = data['products']
        print(f"Found {len(products)} products in the file.")
        
        # Step 4: Validate individual product data
        print("\nValidating product data...")
        valid_products, validation_errors = self.validate_product_data(products)
        
        if validation_errors:
            print("\nValidation Errors Found:")
            for error in validation_errors:
                print(f"  • {error}")
        
        if not valid_products:
            print("\nError: No valid products found. Import cancelled.")
            return
        
        print(f"\nValid products: {len(valid_products)}")
        
        # Step 5: Check for duplicate codes in import data
        duplicate_codes = self.check_duplicate_codes(valid_products)
        if duplicate_codes:
            print(f"\nError: Duplicate product codes found in import data: {', '.join(duplicate_codes)}")
            print("Please fix duplicate codes and try again.")
            return
        
        # Step 6: Connect to database
        try:
            self.db_connection.connect()
            print("\nDatabase connection established.")
        except Exception as e:
            print(f"\nError: Unable to connect to database: {e}")
            return
        
        # Step 7: Check for existing codes in database
        existing_codes = self.check_existing_codes_in_db(valid_products)
        if existing_codes:
            print(f"\nWarning: The following product codes already exist in database:")
            for code in existing_codes:
                print(f"  • {code}")
            
            choice = input("\nDo you want to continue with remaining products? (y/n): ").lower()
            if choice != 'y':
                print("Import cancelled by user.")
                self.db_connection.close()
                return
            
            # Remove products with existing codes
            valid_products = [p for p in valid_products if p['pcode'] not in existing_codes]
            
            if not valid_products:
                print("No new products to import.")
                self.db_connection.close()
                return
        
        # Step 8: Import products to database
        print(f"\nImporting {len(valid_products)} products to database...")
        success_count, failed_imports = self.import_products_to_database(valid_products)
        
        # Step 9: Display results
        print("\n" + "=" * 50)
        print("           IMPORT RESULTS")
        print("=" * 50)
        
        if success_count > 0:
            print(f" Successfully imported: {success_count} products")
        
        if failed_imports:
            print(f" Failed imports: {len(failed_imports)}")
            for error in failed_imports:
                print(f"  • {error}")
        
        if validation_errors:
            print(f" Validation errors: {len(validation_errors)} products skipped")
        
        print(f"\nTotal products processed: {len(products)}")
        print(f"Successfully imported: {success_count}")
        print(f"Failed/Skipped: {len(products) - success_count}")
        
        # Close database connection
        self.db_connection.close()
        print("\nDatabase connection closed.")
        
        if success_count > 0:
            print("\n Import completed successfully!")
        else:
            print("\n Import failed. Please check the errors above.")


def main():
    """Main function to run the product importer"""
    try:
        importer = ProductImporter()
        importer.run_import()
    except KeyboardInterrupt:
        print("\n\nImport cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        print("Please check your database connection and file format.")


if __name__ == "__main__":
    main()