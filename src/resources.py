class RobotCreatorResources:
    URL = "https://robotsparebinindustries.com/#/robot-order"
    ORDERS_CSV_URL = "https://robotsparebinindustries.com/orders.csv"

    ORDER_NUMBER_LOCATOR = "//*[starts-with(text(), 'RSB-ROBO-ORDER-')]"
    CLOSE_MODAL_LOCATOR = "text=OK"

    HEAD_FORM_LOCATOR = "#head"
    BODY_FORM_LOCATOR = "#id-body-{body}"
    LEGS_FORM_LOCATOR = "input[type='number']"
    ADDRESS_FORM_LOCATOR = "#address"
    FORM_ERROR_LOCATOR = ".alert.alert-danger"
    SUBMIT_FORM_BUTTON_LOCATOR = "#order"
    NEW_ORDER_BUTTON_LOCATOR = "#order-another"

    RECEIPT_LOCATOR = "#receipt"
    IMAGE_PREVIEW_LOCATOR = "#robot-preview-image"
