from datetime import timedelta


class Utils:
    @staticmethod
    def avg_order_complete_time(complete_time: float, complete_orders: int) -> str:
        delta = timedelta(seconds=complete_time)
        return str(delta / complete_orders) if complete_orders else str(delta)

    @staticmethod
    def avg_day_orders(complete_orders: int, works_days: int) -> int:
        return complete_orders // works_days if works_days else complete_orders
