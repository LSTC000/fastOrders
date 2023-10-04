from datetime import timedelta


class Utils:
    @staticmethod
    def avg_order_complete_time(complete_time: float, complete_orders: int) -> str:
        delta = timedelta(seconds=complete_time)
        return str(delta / complete_orders) if complete_orders else str(delta)

    @staticmethod
    def avg_day_orders(complete_orders: int, works_days: int) -> int:
        return complete_orders // works_days if works_days else complete_orders

    @classmethod
    def get_courier_report(cls, courier_data: dict, active_order_data: dict | None) -> dict:
        return {
            'id': courier_data.get('id'),
            'name': courier_data.get('name'),
            'active_order': {
                'order_id': active_order_data.get('id'),
                'order_name': active_order_data.get('name'),
            } if active_order_data else None,
            'avg_order_complete_time': cls.avg_order_complete_time(
                complete_time=courier_data.get('complete_time'),
                complete_orders=courier_data.get('complete_orders')
            ),
            'avg_day_orders': cls.avg_day_orders(
                complete_orders=courier_data.get('complete_orders'),
                works_days=courier_data.get('works_days')
            )
        }
