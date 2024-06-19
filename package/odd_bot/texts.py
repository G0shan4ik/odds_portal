from aiogram.utils.markdown import hbold


START_TEXT = hbold('Добро пожаловать в наш бот!')
MAIN_MENU_TEXT = 'Главное меню'

ADD_USERS_TEXT = 'Добавить игрока 👤'
CHANGE_LIST_TEXT = 'Редакстировать список 🗒'

SEND_BETTER_NAME_TEXT = f'Введите {hbold("nickname")} беттора.'
INSTALL_KEY_TEXT = 'Добавить ключевые слова 🔑'

SUCCESS_TEXT = lambda name: f'Nickname "{hbold(name)}" был успешно установлен!'
SUCCESS_ENTER_KEYS_TEXT = lambda name: f'Ключевые слова для "{hbold(name)}" были успешно установлены!'
SUCCESS_DELETE_KEYS_TEXT = lambda name: f'Все ключевые слова для "{hbold(name)}" были успешно удалены!'
NO_INSTALLED_BETTORS_TEXT = f'У вас нет установленных беттеров.\nЧтобы установить беттора, нажмите на кнопку "{hbold(ADD_USERS_TEXT)}"'

WRONG_TEXT = hbold('Что-то пошло не так(')

SUCCESS_DELETING_BETTOR = lambda name: f'Беттор, {name}, успешно удалён 💥'

ENTER_KEYS_TEXT = lambda name: (f'Введите {hbold("keywords")} для беттора > {hbold(name)}\n• Если ключевых слов больше '
                                f'''чем 1, то введите их {hbold('разделяя запятой > ","')}\n'''
                                f"""•Если вы хотите сделать несколько групп ключевых слов, то {hbold('разделите их > "+"')}\n"""
                                f'• Если вы хотите {hbold("удалить все ключевые слова")}, то введите цифру "{hbold(1)}"')
ENTER_ROI_TEXT = lambda name: f'Введите {hbold("ROI")} для беттора > {hbold(name)}.\nПример ввода: 100'

UNSUCCESS_SAVE_ROI = 'Не корректный ввод!!!'
SUCCESS_SAVE_ROI = 'ROi был успешно сохранен!'

WRONG_BETTORS_NAME = lambda name: f'‼️Беттор, {hbold(name)}, уже зарегистрирован‼️\nВведите другого беттора!'