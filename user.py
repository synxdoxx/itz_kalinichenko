import json

class User:
    def __init__(self, username="", password=""):
        """Инициализация класса со статами и списком артефактов игрока"""
        self.username = username
        self.password = password
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.defense = 0
        self.artifacts = []

    def print_stats(self):
        """Функция для вывода всех статов и артефактов (если есть) игрока на данный момент"""
        print(f'''Твоё здоровье: {self.health}/{self.max_health}
Твоя сила атаки: {self.attack}
Твоя защита: {self.defense}''')
        if len(self.artifacts) == 0:
            print('У тебя пока что нет артефактов :(')
        else:
            print('Твои артефакты:', end = ' ')
            for artifact in self.artifacts:
                print(f'{artifact};', end = ' ')
            print('\n')

    def take_damage(self, damage):
        """Функция получения урона игроком."""
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        return actual_damage

    def add_artifact(self, artifact_name):
        """Добавление игроку артефакта. В зависимости от названия артефакта меняет статы и выводит сообщение об этом"""

        if artifact_name not in self.artifacts: #Проверка, на случай, если такой артефакт уже есть у юзера
            self.artifacts.append(artifact_name)
            print(f"＼(＾▽＾)／ Ты получил артефакт: {artifact_name}!")

            # Бонусы от артефактов
            if artifact_name == "Крыса на палке":
                self.attack += 10
                print('Ты получил 10 к атаке!')
                print()
            elif artifact_name == "Теплая куртка":
                self.defense += 8
                print('Ты получил 8 к защите!')
                print()
            elif artifact_name == "Крепкий сон":
                self.max_health += 30
                self.health += 30
                print('Ты получил 30 к максимальному и нынешнему здоровью!')
                print()
            elif artifact_name == "Чиикава":
                self.defense += 5
                self.attack += 10
                print('Ты получил 10 к атаке!')
                print('Ты получил 5 к защите!')
                print()
            elif artifact_name == "Сумка с ноутом":
                self.attack += 15
                print('Тяжелая. Ты получил 15 к атаке!')
                print()
            elif artifact_name == "Колготы":
                self.max_health += 10
                self.health += 10
                print('Ты получил 30 к максимальному и нынешнему здоровью!')
                print()
            elif artifact_name == "Кофе из сезонного меню":
                self.defense += 10
                print('Ты получил 10 к защите!')
                print()
            elif artifact_name == "Котик":
                print('Ты ничего к статам не получил. Ты серьезно думал, что котик тебе чем-то поможет? Он просто милый.')
                print()
            elif artifact_name == "Два котика":
                print('Они точно тебе ничем не помогут. Просто мило играют друг с другом.')
                print()
            elif artifact_name == "Деньги":
                self.health += 20
                self.defense += 5
                print('Ты получил 20 к нынешнему здоровью!')
                print('Ты получил 5 к защите!')
                print()