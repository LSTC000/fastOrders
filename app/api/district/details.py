from dataclasses import dataclass

from app.utils.response import Details


@dataclass(frozen=True)
class DistrictDetails(Details):
    district_name_exist: str = 'This district already exist'
    get_district_error: str = ('An error occurred while searching for the district. Check the specified '
                               'district id and try again later.')
    get_districts_error: str = 'No districts have been created yet.'
    add_district_error: str = 'An error occurred when adding a district. Try again later.'
