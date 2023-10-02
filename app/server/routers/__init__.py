__all__ = ['__routers__']


from .routers import Routers

from app.api import courier_router, order_router, district_router


__routers__ = Routers(
    routers=(
        courier_router,
        order_router,
        district_router,
    )
)
