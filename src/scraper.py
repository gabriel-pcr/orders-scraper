import os

from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive

from src.resources import RobotCreatorResources

class RobotCreatorScraper:

    def __init__(self):
        self.browser = browser
        self.pdf = PDF()
        self.http = HTTP()
        self.archive = Archive()

    def insert_orders(self) -> None:
        """Runs the flow to insert orders"""
        self._open_browser()
        orders = self._get_orders()
        for order in orders:
            self._close_modal()
            self._fill_the_form(order)
            order_number = self._submit_form()
            pdf_path = self._store_receipt_as_pdf(order_number)
            screenshot_path = self._screenshot_robot(order_number)
            self._embed_screenshot_to_receipt(screenshot_path, pdf_path)
            self._go_to_add_another_order()
        self._archive_receipts()

    def _open_browser(self) -> None:
        """Navigates to the robot order website"""
        self.browser.goto(RobotCreatorResources.URL)

    def _download_orders_file(self) -> None:
        """Download orders from remote file"""
        self.http.download(url=RobotCreatorResources.ORDERS_CSV_URL, overwrite=True)

    def _get_orders(self) -> list[dict]:
        """Load orders as table"""
        self._download_orders_file()
        library = Tables()
        table = library.read_table_from_csv(
            "orders.csv",
            columns=["Order number", "Head", "Body", "Legs", "Address"]
        )
        return [row for row in table]

    def _close_modal(self) -> None:
        """Clicks on 'OK' button to close modal"""
        page = self.browser.page()
        page.click(RobotCreatorResources.CLOSE_MODAL_LOCATOR)

    def _fill_the_form(self, row: dict) -> None:
        """Fill the form with row data"""
        page = self.browser.page()

        page.select_option(RobotCreatorResources.HEAD_FORM_LOCATOR, str(row["Head"]))
        page.click(RobotCreatorResources.BODY_FORM_LOCATOR.format(body=row["Body"]))
        page.fill(RobotCreatorResources.LEGS_FORM_LOCATOR, row["Legs"])
        page.fill(RobotCreatorResources.ADDRESS_FORM_LOCATOR, row["Address"])

    def _get_order_number(self) -> str:
        """Once an order is submitted, an order number is generated"""
        page = self.browser.page()
        return page.locator(RobotCreatorResources.ORDER_NUMBER_LOCATOR).inner_text()

    def _submit_form(self) -> str:
        page = self.browser.page()
        page.click(RobotCreatorResources.SUBMIT_FORM_BUTTON_LOCATOR)

        while True:
            if page.locator(RobotCreatorResources.NEW_ORDER_BUTTON_LOCATOR).is_visible():
                break
            elif page.locator(RobotCreatorResources.FORM_ERROR_LOCATOR).is_visible():
                page.click(RobotCreatorResources.SUBMIT_FORM_BUTTON_LOCATOR)
        return self._get_order_number()

    def _go_to_add_another_order(self) -> None:
        """Click on the 'Add another order' button"""
        page = self.browser.page()
        page.click(RobotCreatorResources.NEW_ORDER_BUTTON_LOCATOR)

    def _store_receipt_as_pdf(self, order_number: str) -> str:
        """Store receipt information as PDF file"""
        page = self.browser.page()
        receipt_html = page.locator(RobotCreatorResources.RECEIPT_LOCATOR).inner_html()

        pdf_file_path = f"output/receipts/{order_number}.pdf"
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)
        self.pdf.html_to_pdf(receipt_html, pdf_file_path)
        return pdf_file_path

    def _screenshot_robot(self, order_number: str) -> str:
        """Takes a screenshot of the robot view"""
        page = self.browser.page()

        png_file_path = f"output/previews/{order_number}.png"
        os.makedirs(os.path.dirname(png_file_path), exist_ok=True)
        preview_locator = page.locator(RobotCreatorResources.IMAGE_PREVIEW_LOCATOR)
        image_bytes = self.browser.screenshot(preview_locator)
        with open(png_file_path, "wb") as image_file:
            image_file.write(image_bytes)
        return png_file_path

    def _embed_screenshot_to_receipt(self, screenshot_path: str, pdf_file_path: str) -> None:
        """Embed screenshot taken to the receipt PDF"""
        self.pdf.add_files_to_pdf(
            files=[screenshot_path + ':align=center'],
            target_document=pdf_file_path,
            append=True
        )

    def _archive_receipts(self) -> None:
        """Creates a zip file containing all receipt PDF files"""
        self.archive.archive_folder_with_zip("./output/receipts", "output/receipts.zip")
