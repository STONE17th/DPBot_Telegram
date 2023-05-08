

from Keyboards import ikb_user_notification
from loader import users_db, bot


async def user_notify(type_alert: str, message: tuple[str, str], table: str = None) -> None:
    keyboard = ikb_user_notification(type_alert, table)
    poster, caption = message
    user_list = users_db.alerts(alert=f'alert_{type_alert}', table=table)
    if user_list:
        for user in set(user_list):
            try:
                await bot.send_photo(int(user[0]), photo=poster, caption=caption, reply_markup=keyboard)
            except Exception as e:
                pass




