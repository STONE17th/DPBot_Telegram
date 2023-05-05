from aiogram import Dispatcher
from .middleware import AdvancedData


def setup(dp: Dispatcher):
    dp.middleware.setup(AdvancedData())