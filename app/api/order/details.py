from dataclasses import dataclass

from app.utils.response import Details


@dataclass(frozen=True)
class OrderDetails(Details):
    district_does_not_exist: str = 'The district you specified does not exist'
    get_order_error: str = ('An error occurred while searching for the order. Check the specified '
                            'order id and try again later.')
    add_order_error: str = ('An error occurred while adding an order. '
                            'No couriers were found for this order. Try again later.')
    finish_order_error: str = ('This order could not be found. It may have already been completed.'
                               ' Check the order id and try again later.')
