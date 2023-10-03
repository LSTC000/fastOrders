from datetime import datetime, timedelta


class Utils:
    @staticmethod
    def start_order(courier_data: dict, order_data: dict) -> tuple[dict, dict]:
        new_courier_data = {
            'status': 1
        }

        last_finish_at = courier_data['last_finish_at']

        if last_finish_at is None:
            new_courier_data['work_days'] = 1
        else:
            start_order_at = datetime.utcnow()
            next_work_day_at = last_finish_at + timedelta(days=1)

            if next_work_day_at.date() <= start_order_at.date():
                new_courier_data['work_days'] = courier_data.get('work_days') + 1

        new_order_data = {
            'name': order_data.get('name'),
            'courier_id': courier_data.get('id'),
            'district_id': order_data.get('district')
        }

        return new_courier_data, new_order_data

    @staticmethod
    def finish_order(courier_data: dict, order_data: dict) -> tuple[dict, dict]:
        finish_order_at = datetime.utcnow()
        finish_order_at_tmp = finish_order_at.timestamp()
        start_order_at_tmp = order_data['start_at'].timestamp()

        new_courier_data = {
            'status': 0,
            'complete_orders': courier_data.get('complete_orders') + 1,
            'complete_time': courier_data.get('complete_time') + (finish_order_at_tmp - start_order_at_tmp),
            'last_finish_at': finish_order_at
        }

        new_order_data = {
            'status': 2,
            'finish_at': finish_order_at
        }

        return new_courier_data, new_order_data
