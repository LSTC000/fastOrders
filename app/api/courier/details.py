from dataclasses import dataclass

from app.utils.response import Details


@dataclass(frozen=True)
class CourierDetails(Details):
    district_does_not_exist: str = 'One of the districts you specified does not exist'
    get_courier_error: str = ('An error occurred while searching for the courier. Check the specified '
                              'courier id and try again later.')
    get_couriers_error: str = 'No couriers have been created yet.'
    add_courier_error: str = 'An error occurred when adding a courier. Try again later.'
