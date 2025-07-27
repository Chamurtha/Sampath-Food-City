import pytest
from unittest.mock import patch, MagicMock

# Services and main menu imports
from DBConnection import DatabaseConnection, AuthenticationService
from BranchManager import BranchService
from ProductManager import ProductService
from BranchProductManger import BranchProductService
from SalesManager import SalesService
from SupplierManager import SupplierService
from StockManager import StockService
from ReportManager import ReportService

from finalproject import (
    main_menu,
    manage_products,
    manage_sales,
    manage_branch,
    manage_stock_details,
    manage_branch_product,
    manage_supplier_details,
    manage_reports
)

# ----------------------------- #
# Test for main_menu() function
# ----------------------------- #
@patch('builtins.input', side_effect=['Admin', '111', '8'])
@patch('DBConnection.DatabaseConnection.connect')
@patch('DBConnection.DatabaseConnection.close')
@patch('DBConnection.AuthenticationService.authenticate', return_value=True)
def test_main_menu(mock_auth, mock_close, mock_connect, mock_input):
    db_connection = MagicMock(spec=DatabaseConnection)

    with patch('DBConnection.DatabaseConnection', return_value=db_connection):
        with patch('DBConnection.AuthenticationService', return_value=MagicMock(spec=AuthenticationService)):
            with patch('ProductManager.ProductService', return_value=MagicMock(spec=ProductService)):
                with patch('BranchManager.BranchService', return_value=MagicMock(spec=BranchService)):
                    with patch('BranchProductManger.BranchProductService', return_value=MagicMock(spec=BranchProductService)):
                        with patch('SupplierManager.SupplierService', return_value=MagicMock(spec=SupplierService)):
                            with patch('SalesManager.SalesService', return_value=MagicMock(spec=SalesService)):
                                with patch('StockManager.StockService', return_value=MagicMock(spec=StockService)):
                                    with patch('ReportManager.ReportService', return_value=MagicMock(spec=ReportService)):
                                        main_menu()

    mock_connect.assert_called_once()
    mock_auth.assert_called_once_with('Admin', '111')
    mock_close.assert_called_once()

# ----------------------------- #
# Test for manage_products()
# ----------------------------- #
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6', '7'])
def test_manage_products(mock_input):
    service = MagicMock(spec=ProductService)
    manage_products(service)
    service.add_product.assert_called_once()

# ----------------------------- #
# Test for manage_sales()
# ----------------------------- #
@patch('builtins.input', side_effect=['1', '2', '3', '4'])
def test_manage_sales(mock_input):
    service = MagicMock(spec=SalesService)
    manage_sales(service)
    service.add_sales.assert_called_once()

# ----------------------------- #
# Test for manage_branch()
# ----------------------------- #
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
def test_manage_branch(mock_input):
    service = MagicMock(spec=BranchService)
    manage_branch(service)
    service.add_branch.assert_called_once()

# ----------------------------- #
# Test for manage_stock_details()
# ----------------------------- #
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5'])
def test_manage_stock_details(mock_input):
    service = MagicMock(spec=StockService)
    manage_stock_details(service)
    service.add_stock_details.assert_called_once()

# ----------------------------- #
# Test for manage_branch_product()
# ----------------------------- #
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
def test_manage_branch_product(mock_input):
    service = MagicMock(spec=BranchProductService)
    manage_branch_product(service)
    service.add_branch_product.assert_called_once()

# ----------------------------- #
# Test for manage_supplier_details()
# ----------------------------- #
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
def test_manage_supplier_details(mock_input):
    service = MagicMock(spec=SupplierService)
    manage_supplier_details(service)
    service.add_supplier.assert_called_once()

# ----------------------------- #
# Test for manage_reports()
# ----------------------------- #
@patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
def test_manage_reports(mock_input):
    service = MagicMock(spec=ReportService)
    manage_reports(service)
    service.monthly_sales_analysis.assert_called_once()
