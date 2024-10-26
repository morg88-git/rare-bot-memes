import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = 'YOUR_BOT_API_TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Путь к папке с изображениями
IMAGE_PATH = "images/"

# Редкость и путь к папкам
RARITY = {
    "common": os.path.join(IMAGE_PATH, "common"),
    "rare": os.path.join(IMAGE_PATH, "rare"),
    "legendary": os.path.join(IMAGE_PATH, "legendary")
}

# Вероятности показа картинок в зависимости от редкости
RARITY_CHANCES = {
    "common": 70,   # 70% шанс
    "rare": 25,     # 25% шанс
    "legendary": 5  # 5% шанс
}

# Функция для получения случайной картинки по редкости
def get_random_image():
    rarity = random.choices(
        list(RARITY.keys()), 
        weights=RARITY_CHANCES.values(), 
        k=1
    )[0]
    images = os.listdir(RARITY[rarity])
    image_path = os.path.join(RARITY[rarity], random.choice(images))
    return image_path

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Вывести мем"))
    await message.answer("Привет! Нажми на кнопку, чтобы получить мем!", reply_markup=markup)

# Обработка запроса на вывод мема
@dp.message_handler(lambda message: message.text == "Вывести мем")
async def send_meme(message: types.Message):
    image_path = get_random_image()
    photo = InputFile(image_path)
    await message.answer_photo(photo)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)