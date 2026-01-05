import json
import random
import os


from user import *
from arts import *
from boss import *

USERS_FILE = "saves/users.json" #Хранит путь к файлу со всеми юзерами
ARTS_FILE = "saves/arts.json" #Хранит путь к файлу со списком всех артифактов
SAVE_FOLDER = "saves" #Хранит путь к папке с сохранениями

def generate_arts():
    """Создает файл с артефактами"""
    os.makedirs(SAVE_FOLDER, exist_ok=True)  # Создает папку, если её еще нет

    data = [
  "Крыса на палке",
  "Теплая куртка",
  "Крепкий сон",
  "Чиикава",
  "Сумка с ноутом",
  "Колготы",
  "Кофе из сезонного меню",
  "Котик",
  "Два котика",
  "Деньги"
]  # Записывает все данные в файл в нужном формате

    with open(ARTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_users():
    """Считывает информацию о всех юзерах (имя и пароль), записанных в users.json, если этот файл уже существует"""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    """Записывает информацию о юзерах (имя и пароль) в users.json"""
    os.makedirs("saves", exist_ok=True) #Создает папку если её еще нет
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def register():
    """Функция для регистрации новых пользователей"""
    users = load_users() #Читаем инфоомацию об уже существующих аккаунтах

    name = input("Имя: ")
    if name in users: #Проверка на уникальность имени
        print("ヽ(°〇°)ﾉСИСТЕМА: Пользователь уже существует")
        return None

    password = input("Пароль: ")
    users[name] = password #Привязка пароля к имени
    save_users(users) #Обновление записи о всех юзерах

    user = User() #Создание нового объекта с новыми именем и паролем
    user.username = name
    user.password = password

    print("ヽ(°〇°)ﾉСИСТЕМА: Регистрация успешна") #Оповещение системы
    return user #Возвращаем новый объект


def login():
    """Функция входа в 'аккаунт'"""
    users = load_users() #Читаем инфоомацию об уже существующих аккаунтах

    name = input("Имя: ")
    password = input("Пароль: ")

    if name in users and users[name] == password: #Проверка на существование такого аккаунта и правильность пароля
        user = User() #Создание объекта класса. Впоследствии в него мы загрузим последнее сохранение
        user.username = name
        user.password = password
        print("ヽ(°〇°)ﾉСИСТЕМА: Вход выполнен")
        return user

    print("ヽ(°〇°)ﾉСИСТЕМА: Неверные данные")
    return None

def get_choice(options, text="Твой выбор: "):
    """Функция для проверки правильности ввода пользователя.
    В случае, если такого варианта ответа нет, или если пользователь ввёл не число, функция об этом сообщает и просит ввести снова,
    пока пользователь не введет правильно."""
    fl = False
    while fl == False:
        try:
            choice = int(input(text))
            if choice in options:
                fl = True
            else:
                print("ヽ(°〇°)ﾉСИСТЕМА: Такого варианта ответа нет >:(")
        except ValueError:
            print("ヽ(°〇°)ﾉСИСТЕМА: Такого варианта ответа нет >:(")
    print('')
    return choice #Возвращает выбранное число

class Game: #класс самой игры
    def __init__(self):
        """Инициализация класса"""
        self.artifact_bank = ArtifactBank() #Создаем банк артефактов
        self.player = User() #Создаем игрока
        self.game_active = False #Флаг работы игры
        self.users_file = "users.json" #Файл с юзерами и паролями
        self.arts_file = "arts.json" #Файл с артефактами

    def load_arts(self):
        """Функция для загрузки артефактов из файла"""
        path = f"{SAVE_FOLDER}/{self.arts_file}"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for art in data:
            if art not in self.player.artifacts and art not in self.artifact_bank.available_artifacts: #Если это не первая игра пользователя, артефакты повторно не загрузятся
                self.artifact_bank.available_artifacts.append(art)


    def death_check(self, mob):
        """Функция, запускающая бой и обрабатывающая его результаты. Если игрок побеждает или сбегает, то история просто идет дальше со соответствующими последствиями.
         В случае проигрыша редлагает либо попробовать снова (игрок возвращается в тот же бой, но с теми артефакьтами, которые сохранил в последний раз)
         либо выйти из игры (= плохая концовка). Пробовать снова можно сколько угодно раз."""
        res = False #Флаг, обозначающий результат боя
        while res == False: #Продолжается либо до победы (побега) либо до того, как игрок сдается
            res = self.battle(mob) #Выполняется бой
            if res == True:
                break #При победе работа функции окончена
            print('''ヽ(°〇°)ﾉСИСТЕМА: Загрузить сохранение и попробовать снова?
            
    1. Да
    2. Нет''')

            choice = get_choice([1, 2])

            if choice == 1:
                self.load_game() #Загрузка сохранения
                mob.hp = mob.max_hp #Обновление хп врага
            else:
                print('Плохая концовка :(')
                self.game_active = False #Игра заканчивается


    def save_game(self):
        """Сохранение игры в персональный json файл.
        В файл игрока сохраняются все его статы и список имеющихся артефактов, а также артефактов, оставшихся в банке"""
        os.makedirs(SAVE_FOLDER, exist_ok=True) #Создает папку, если её еще нет

        data = {
            "player": {
                "username": self.player.username,
                "password": self.player.password,
                "health": self.player.health,
                "max_health": self.player.max_health,
                "attack": self.player.attack,
                "defense": self.player.defense,
                "artifacts": self.player.artifacts
            },
            "artifact_bank": {
                "available_artifacts": self.artifact_bank.available_artifacts
            }
        } #Записывает все данные в файл в нужном формате

        with open(f"{SAVE_FOLDER}/{self.player.username}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("ヽ(°〇°)ﾉСИСТЕМА: Игра сохранена")


    def save_game_sys(self):
        """Та же самая функция, что и предыдущая, но без системного сообщения.
        Для случаев, когда нужно сохранить данные, но оповещать пользователя об этом не надо"""
        os.makedirs(SAVE_FOLDER, exist_ok=True)

        data = {
            "player": {
                "username": self.player.username,
                "password": self.player.password,
                "health": self.player.health,
                "max_health": self.player.max_health,
                "attack": self.player.attack,
                "defense": self.player.defense,
                "artifacts": self.player.artifacts
            },
            "artifact_bank": {
                "available_artifacts": self.artifact_bank.available_artifacts
            }
        }

        with open(f"{SAVE_FOLDER}/{self.player.username}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def save_game_sys_FOR_BATTLE(self):
        """Та же самая функция, что и предыдущая, но без системного сообщения и не перезаписывает сохранение артефактов.
        Нужна, чтобы после боя сохранять потерю здоровья, но при этом не сохранять изменение артефактов"""
        os.makedirs(SAVE_FOLDER, exist_ok=True)

        with open(f"{SAVE_FOLDER}/{self.player.username}.json", "r", encoding="utf-8") as f:
            old_data = json.load(f) #Временно храним старые данные тут

        data = {
            "player": {
                "username": self.player.username,
                "password": self.player.password,
                "health": self.player.health,
                "max_health": old_data['player']['max_health'],
                "attack": old_data['player']['attack'],
                "defense": old_data['player']['defense'],
                "artifacts": old_data['player']['artifacts']
            },
            "artifact_bank": {
                "available_artifacts": old_data['artifact_bank']['available_artifacts']
            }
        }

        with open(f"{SAVE_FOLDER}/{self.player.username}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_game(self):
        """Функция загрузки сохранения из файла"""
        path = f"{SAVE_FOLDER}/{self.player.username}.json"
        if not os.path.exists(path): #Проверяет наличие сохранения
            print("ヽ(°〇°)ﾉСИСТЕМА: Сохранение не найдено")
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f) #Берем данные из файла

        p = data["player"] #Тут берем именно данные игрока, без данныз о банке артефактов
        self.player.health = p["health"]
        self.player.max_health = p["max_health"]
        self.player.attack = p["attack"]
        self.player.defense = p["defense"]
        self.player.artifacts = p["artifacts"]

        self.artifact_bank.available_artifacts = data["artifact_bank"]["available_artifacts"] #Загружаем данные о банке артефактов
        print("ヽ(°〇°)ﾉСИСТЕМА: Игра загружена")


    def load_game_sys(self):
        """Та же самая функция, что и предыдущая, но без системного сообщения.
        Для случаев, когда нужно загрузить сохранение, но оповещать пользователя об этом не надо"""
        path = f"{SAVE_FOLDER}/{self.player.username}.json"
        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        p = data["player"]
        self.player.health = p["health"]
        self.player.max_health = p["max_health"]
        self.player.attack = p["attack"]
        self.player.defense = p["defense"]
        self.player.artifacts = p["artifacts"]

        self.artifact_bank.available_artifacts = data["artifact_bank"]["available_artifacts"]

    def battle(self, mob):
        """Функция самого боя, которую вызываем в death_check. Есть возможность атаковать или сбежать."""
        print(f'Ты вступил в бой! Здоровье монтра: {mob.hp}')
        self.player.print_stats() #Вывод статов игрока, чтобы он мог оценить свои шансы
        dice_flag = 0 #Флаг для побега
        while mob.hp > 0 and self.player.health > 0:
            print('''
    1. Атаковать
    2. Бежать 
    ''')
            choice = get_choice([1, 2])
            if choice == 1:
                mob.hp-=self.player.attack
                print(f'Здоровье монтра: {mob.hp} Твое здоровье: {self.player.health}')

            if choice == 2: #Возможность побега определяется 'броском кубика' Больше 4 - смог сбежать, иначе - нет.
                dice = random.randint(1, 6)
                dice_flag = 0 #Обновление флага, на случай повторного использования
                if dice < 5:
                    print('Ты не смог сбежать')
                else:
                    print('Ты смог сбежать!')
                    dice_flag = 1 #Смена флага на удачный для побега
                    self.save_game_sys_FOR_BATTLE() #Сохранение статов на момент побега, чтобы весь урон, полученный от врага, остался
                    break

            dice_m = random.randint(1, 6) #Рандом для определения силы атаки врага. Меньше 5 - обычная атака, больше - сильная атака
            if dice_m < 5:
                mob.attack(self.player)
            else:
                mob.strong_attack(self.player)

            print(f'Здоровье монтра: {mob.hp} Твое здоровье: {self.player.health}') #Вывод обновленного здоровья после ходов игрока и врага

        if dice_flag == 1: #Вывод сообщения в случае побега и выход из боя
            print('''Но артефакт за такое не получишь)
            ''')
            return True

        if self.player.health <= 0: #Условие проигрыша
            print('Ты умер!')
            return False

        elif mob.hp <= 0: #Условие выигрыша
            print('Ты выиграл!')
            self.save_game_sys_FOR_BATTLE()
            prize = self.artifact_bank.get_random_artifact()
            self.player.add_artifact(prize)
            return True



    def story(self):
        """Функция самой истории. Пока флаг self.game_active == True ,игра продолжается."""
        self.game_active = True
        print('\n')
        self.load_arts() #Загрузка артефактов из файла
        self.load_game_sys() #Загрузка последнего сохранения этого пользователя
        self.save_game_sys() #Повторное сохранение для перестраховки, в случае, если это новый пользователь, и до этого записей не было
        
        self.player.print_stats() #Вывод статов на начало игры
        print('\n')

        while self.game_active: #Здесь на протяжении всего цикла чередуется текст повествования и выборы для пользователя.
            print('На часах 5:00. Сегодня четверг - первой парой лекция по матанализу. Надо бы пойти, но ты всю ночь дописывал лабу по информатике.')
            print('Что будешь делать?')
            print('')
            print('    1. Встану и поеду в уник')
            print('    2. Ещё немного полежу и пойду.. На всякий заведу будильник на чуть позже')
            print('    3. Не чето не хочу пока (остаться дома)')
            print('    4. Сохраниться')
            print('')

            choice = get_choice([1, 2, 3, 4]) #Используем функцию для проверки ответа

            if choice == 4: #Такая конструкция встречается на протяжении всей истории. При каждом выборе игроку предлагают сохраниться.
                #Если он выбирает сохраниться, то игра сначала сохраняет, а потом предлагает выбрать что-то из оставшихся опций
                #(либо пойти дальше, нажав Enter, если опция осталась одна)
                self.save_game()
                print('')
                print('    1. Встану и поеду в уник')
                print('    2. Ещё немного полежу и пойду.. На всякий заведу будильник на чуть позже')
                print('    3. Не чето не хочу пока (остаться дома)')
                print('')
                choice = get_choice([1, 2, 3])

            if choice == 1:
                print('''ого
За такое проявление силы воли ты получаешь награду!''')
                prize = self.artifact_bank.get_random_artifact()
                self.player.add_artifact(prize) #Система получения артефактов. Сначала выбирается рандомный артефакт из банка артефактов, затем отдается игроку с помощью специальной функции
                print('''Собравшись с силами, ты встаешь и идешь на электричку. Сегодня в ней подозрительно пусто...
Даже место нашлось сразу. Смотря в окно, ты замечаешь что-то странное - небо стало совсем черным (сейчас же утро?), а электричка едет очень медленно.''')
                print('''
    1. Ехать дальше
    2. Сохраниться
''')
                next = get_choice([1, 2])

                if next == 2:
                    self.save_game()
                    print('\n')
                    next = input('(Enter) Ехать дальше')
                    print('\n')
                print('''Решив, что это вполне обычное явление для ярославского направления (кроме, разве что, свободных мест), ты без единой мысли в голове как обычно засыпаешь.
Добравшись до Москвы и пересев на метро, ты замечаешь, что людей побольше не стало. Ну, тебе же лучше.''')
                print('''
    1. Ехать дальше
    2. Сохраниться
    ''')
                next = get_choice([1, 2])

                if next == 2:
                    self.save_game()
                    print('\n')
                    next = input('(Enter) Ехать дальше')
                    print('\n')
                print('''Наконец-то ты в своем самом любимом университете на свете! Заходишь в аудиторию... а там никого.
Неужели первую пару отменили?
А, нет, всего лишь чет пошло не так и начался апокалипсис. Теперь тебе нужно победить какую-то заразу, которая прямо сейчас вломилась в дверь.''')
                print('''
    1. Сразиться
    2. Сохраниться
    ''')
                choice = get_choice([1, 2])
                if choice == 2:
                    self.save_game()
                    print('\n')
                    next = input('(Enter) Сразиться')
                    print('\n')
                mob = Boss('Зомби', 100, 100, 5) #Система боя. Сначала создается противник с помощью класса Boss, затем вызывается функция для боя с ним
                self.death_check(mob) #Результаты боя печатаются в функции

                print('Это было... сомнительное развлечение. Кажется, это был кто-то из студентов, превращенный в зомби.')
                print('''Тебя только что осенило! Как же твои любюимые преподаватели 317 кафедры? Они же в порядке?
Выйдя в коридор, ты услышал странные звуки из подвала. Куда пойдешь?

    1. На кафедру
    2. В подвал
    3. Сохраниться
    ''')
                choice = get_choice([1, 2, 3])
                if choice == 3:
                    self.save_game()
                    print(''' 
    1. На кафедру
    2. В подвал
                    ''')
                    choice = get_choice([1, 2])

                if choice == 1:
                    print('''Действительно, стоит проверить, есть ли кто-то там.''')
                    print('''
    1. Подняться на 5 этаж
    2. Сохраниться
    ''')
                    choice = get_choice([1, 2])
                    if choice == 2:
                        self.save_game()
                        print('\n')
                        next = input('(Enter) Подняться на 5 этаж')
                        print('\n')

                    print('''На этаже тихо. Ты подходишь к кабинету... дверь открыта нараспашку, внутри погром. Никого нет.
Как так? неужели их съели зомби?''')
                    print('''
    1. Осмотреться
    2. Сохраниться
                        ''')
                    choice = get_choice([1, 2])
                    if choice == 2:
                        self.save_game()
                        print('\n')
                        next = input('(Enter) Осмотреться')
                        print('\n')

                    print('Ты нашёл артефакт!')
                    prize = self.artifact_bank.get_random_artifact()
                    self.player.add_artifact(prize)
                    print('''На полу ты заметил рассыпанный чай. Он образует дорожку куда-то.''')
                    print('''
    1. Пойти по дорожке
    2. Сохраниться
                        ''')
                    choice = get_choice([1, 2])
                    if choice == 2:
                        self.save_game()
                        print('\n')
                        next = input('(Enter) Пойти по дорожке')
                        print('\n')
                    print('''Пройдя по дорожке, ты оказался всё у того же подвала.''')
                    print('''
    1. Зайти
    2. Сохраниться
                        ''')
                    choice = get_choice([1, 2])
                    if choice == 2:
                        self.save_game()
                        print('\n')
                        next = input('(Enter) Зайти')
                        print('\n')

                print('''Оказавшись внутри, ты находишь... Своих любимых преподавателей!
Светлана Сергеевна в порядке, однако с Алексеем Владимировичем что-то не так. Он стал зомби!''')
                print('''
    1. Сразиться
    2. Сохраниться
    ''')
                choice = get_choice([1, 2])
                if choice == 2:
                    self.save_game()
                    print('\n')
                    next = input('(Enter) Сразиться')
                    print('\n')
                mob = Boss('Алексей Владимирович??', 200, 200, 15)
                self.death_check(mob)

                print('После победы ты и Светлана Сергеевна решаете выбраться из подвала. Однако на входе вы встречаете... настоящего Алексея Владимировича?')
                print('Оказывается тот зомби был просто похожим студентом. За такую героическую победу твои преподаватели решают поставить тебе 5 автоматом за все экзамены!')
                print('''Вы все выбираетесь из университета и находите ближайщий эвакуационный пункт. А главное, что теперь у тебя в зачетке стоит 5!

Хорошая концовка :)''')
                self.save_game_sys()
                self.game_active = False
                break
                #Конец 1 ветки. Программа заканчивает работу.


            if choice == 2:
                print('''Ну, было очевидно, что ты снова заснешь и проспишь. Хорошо, что ты поставил запасной будильник. 
Ты может даже успеешь ко второй паре!''')
                print('''
    1. Встать
    2. Сохраниться
    ''')
                next = get_choice([1, 2])
                if next == 2:
                    self.save_game()
                    print('\n')
                    next = input('(Enter) Встать')
                    print('\n')
                print('''Собравшись с силами ты встаешь, собираешься и идешь на электричку. Сегодня в ней подозрительно пусто...
Точнее вообще никого нет. И едет она странно.
Пройдясь по всей элке, ты дошел до головного вагона...''')
                print('''
    1. Открыть дверь
    2. Сохраниться
    ''')
                next = get_choice([1, 2])
                if next == 2:
                    self.save_game()
                    print('\n')
                    next = input('(Enter) Открыть дверь')
                    print('\n')
                print('''За дверью оказался не машинист, а какой-то зомби!''')
                print('''
    1. Сразиться
    2. Сохраниться
    ''')
                choice = get_choice([1, 2])
                if choice == 2:
                    self.save_game()
                    print('\n')
                    next = input('(Enter) Сразиться')
                    print('\n')
                mob = Boss('Зомби', 100, 100, 5)
                self.death_check(mob)
                print('''Битва битвой, а идти куда-то надо - не скрываться же в холодной электричке. Как раз она остановилась на одной из станций.''')
                print('''
    1. Выйти из электрички
    2. Сохраниться
                    ''')
                choice = get_choice([1, 2])
                if choice == 2:
                    self.save_game()
                    print('\n')
                    next = input('(Enter) Выйти из электрички')
                    print('\n')
                print('''Это станция Москва-3. Почему вообще 3..? Хорошо, что хотя бы Москва.
Прямо на лавочке ты видишь подозрительный свёрток, который кто-то в спешке оставил. Что обычно делают с такими свёртками на вокзалах?

    1. Оставить и уйти
    2. Взять
    3. Сохраниться
    ''')

                choice = get_choice([1, 2, 3])
                if choice == 3:
                    self.save_game()
                    print(''' 
    1. Оставить и уйти
    2. Взять
                                        ''')
                    choice = get_choice([1, 2])
                if choice == 1:
                    print('''К сожалению, в свертке окажутся важные документы, которые могли бы помочь остановить нашествие зомби. 
Теперь ты вынужден эвакуироваться вместе со всеми и пытаться жить дальше в новых условиях.

Плохая концовка :(''')
                    self.game_active = False
                    break  #Плохой конец 2 ветки

                if choice == 2:
                    prize = self.artifact_bank.get_random_artifact()
                    self.player.add_artifact(prize)
                    print('Повезло) В свертке оказался артефакт и какие-то бумажки. Просмотрев их внимательно, Ты обнаружил, что это какие-то важные документы о вирусе.')
                    print('Кажется, стоит вернуть их владельцам. На титульнике написан адрес научно-исследовательского центра.')
                    print('''
    1. Поехать туда на метро
    2. Пойти пешком
    3. Сохраниться
    ''')
                    choice = get_choice([1, 2, 3])
                    if choice == 3:
                        self.save_game()
                        print(''' 
    1. Поехать туда на метро
    2. Пойти пешком
                                                            ''')
                        choice = get_choice([1, 2])
                    if choice == 1:
                        print('''Удивительно, но метро все еще работает - надо же как-то добираться до точек эвакуации.''')
                    if choice == 2:
                        print('''Кто знает, может метро заполонили зомби? К счастью, этот центр расположен недалеко.
К несчастью, бегаешь ты не очень быстро. Надо было закрывать физру самому, а не покупать справку) Тебя загнал в тупик зомби.''')
                        print('''
    1. Сразиться
    2. Сохраниться
                            ''')
                        choice = get_choice([1, 2])
                        if choice == 2:
                            self.save_game()
                            print('\n')
                            next = input('(Enter) Сразиться')
                            print('\n')
                        mob = Boss('Зомби', 100, 100, 5)
                        self.death_check(mob)

                        print('''Теперь ты можешь дойти до этого центра.''')
                    print('''Когда ты добрался до центра, на КПП тебя встретила куча охранников. Они начали тебя прогонять, но тут ты всучил им бумаги
Переглянувшись, они забрали внутрь и бумаги, и тебя. Теперь ты сидишь перед каким-то важным дядей, рассказывая о том, где ты их нашел.''')
                    print('''
    1. Спросить про значимость бумаг
    2. Сохраниться
                        ''')
                    choice = get_choice([1, 2])
                    if choice == 2:
                        self.save_game()
                        print('\n')
                        next = input('(Enter) Спросить про значимость бумаг')
                        print('\n')
                    print('''Важный дядя в награду за возвращение документов рассказал тебе об их предназначении.
Это самое полное исследование вируса, который прямо сейчас захватывает мир. С его помощью возможно остановить апокалипсис.
Тебе говорят спасибо (и больше ничего:( ) и отправляют в пункт эвакуации.

Хорошая концовка :)''')
                    self.save_game_sys()
                    self.game_active = False
                    break   #Конец 2 ветки. Программа заканчивает свою работу



            if choice == 3:
                print('''Вот и славно. В итоге ты встал в 14:00, поел, зашёл в тикток...
А там видео с какими-то зомби, которые терроризируют мир.
Благодаря тому, что ты решил прогулять, ты остался в безопасности!

Очень хорошая концовка :)''')
                self.save_game_sys()
                self.game_active = False
                break   #Конец 3 ветки. Короткая ветка для вайба

generate_arts()
player = None
while not player: #цикл, чтобы в конечном итоге точно зарегестрировать/залогинить пользователя
    print("1. Вход")
    print("2. Регистрация")
    choice = get_choice([1, 2])

    if choice == 1:
        player = login()
    elif choice == 2:
        player = register()

game = Game() #Создание объекта самой игры
game.player = player #Присваивание того игрока, который только что ввел свои данные
game.story() #Запуск истории
