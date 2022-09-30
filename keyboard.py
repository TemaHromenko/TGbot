from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

menu = ReplyKeyboardMarkup(True,True)
menu.row(KeyboardButton('➕Добавить заметку'))
menu.row(KeyboardButton('🤚Просмотреть заметки'))

cancel = ReplyKeyboardMarkup(True, True)
cancel.row(KeyboardButton('❌Отмена'))

save = ReplyKeyboardMarkup(True, True)
save.row(KeyboardButton('✅Да'))
save.row(KeyboardButton('❌Нет'))
