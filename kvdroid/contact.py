from kvdroid import activity
from kvdroid import Phone


def get_contact_details(option: str = "phone_book"):
    """
    option accepts this values : "phone_book", "mobile_no", "names"

    :param option: str: used to determine the return value
    :return: value
    """
    value = None
    PROJECTION = ["contact_id", "display_name", Phone.NUMBER]
    cr = activity.getContentResolver()
    cursor = cr.query(Phone.CONTENT_URI, PROJECTION, None, None, "display_name" + " ASC")
    mobile_no_set: list = []
    phone_book: dict = {}
    if cursor:
        try:
            name_index: int = cursor.getColumnIndex("display_name")
            number_index: int = cursor.getColumnIndex(Phone.NUMBER)

            while cursor.moveToNext():
                name = cursor.getString(name_index)
                number = cursor.getString(number_index)
                number = number.replace(" ", "")
                if number not in mobile_no_set:
                    if name in phone_book:
                        phone_book[name].append(number)
                    else:
                        phone_book.update({name: [number]})
                    mobile_no_set.append(number)
        finally:
            cursor.close()

        if option == "names":
            value = list(phone_book.keys())
        elif option == "mobile_no":
            value = mobile_no_set
        else:
            value = phone_book
    return value
