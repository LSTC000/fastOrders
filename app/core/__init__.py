__all__ = [
    'Base',
]


from app.db import Base

from app.api.user.models import User
from app.api.post.models import Post
from app.api.courier.models import Courier
from app.api.order.models import Order
from app.api.district.models import District
