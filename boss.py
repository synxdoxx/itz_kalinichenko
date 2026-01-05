class Boss:
    def __init__(self, name = "Зомби", hp = 200, max_hp = 200, strength = 5):
        """Инициализация со статами"""
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.strength = strength


    def take_damage(self, damage):
        """Функция получения врагом урона"""
        self.hp -= damage

    def attack(self, target):
        """Функция атаки цели. Также выводит сообщение с информацией об уроне """
        damage = self.strength
        print(f"(°ロ°) ! {self.name} атакует и наносит {damage} урона!")
        target.take_damage(damage)

    def strong_attack(self, target):
        """Функция сильной атаки цели. Также выводит сообщение с информацией об уроне """
        damage = self.strength + 20
        print(f"(°ロ°) !! {self.name} сильно атакует и наносит {damage} урона!")
        target.take_damage(damage)
