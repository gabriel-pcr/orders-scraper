from robocorp.tasks import task

from src.scraper import RobotCreatorScraper

@task
def order_robots_from_rsb() -> None:
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    scraper = RobotCreatorScraper()
    scraper.insert_orders()
