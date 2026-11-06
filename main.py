import os
from random import choice


class Weapon:
    def __init__(self,name, power, gold_price, loot_price):
        self.name = name
        self.power = power
        self.gold_price = gold_price
        self.loot_price = loot_price

class Character:

    def __init__(self, name, hp, power):
        self.name = name
        self.__hp = hp
        self.max_hp = hp
        self.power = power
        self.inventory = []

    @property
    def hp(self):
        return self.__hp

    def take_damage(self, damage, cause):
        self.__hp -= damage
        print(f"{self.name} получил {damage} урона. Осталось {self.__hp} HP")
        if self.__hp <= 0:
            print(f"{self.name} погиб,{cause}")

    def heal(self, amount):
        self.__hp += amount
        if self.__hp > self.max_hp:
            self.__hp = self.max_hp
        print(f"{self.name} восстановил {amount} здоровья! Теперь у него {self.__hp} HP")

class Hero(Character):
    def __init__(self, name, hp, power, gold, mob_loot):
        super().__init__(name, hp, power)
        self.mob_loot = mob_loot
        self.gold = gold
        self.level = 1
        self.inventory = []
        self.equipped_weapon = Weapon("Кулаки", 0,0,0)

    def attack(self, enemy):
        if self.hp > 0 and enemy.hp > 0:
            print(f"Герой {self.name} наносит удар")
            total_damage = self.power + self.equipped_weapon.power
            enemy.take_damage(total_damage, f"от удара героя {self.name}")

class Monster(Character):
    def __init__(self, name, hp, power, reward, loot):
        super().__init__(name, hp, power)
        self.reward = reward
        self.loot = loot
    def attack(self, enemy):
        if self.hp > 0 and enemy.hp > 0:
            print(f"Монстр {self.name} атакует")
            enemy.take_damage(self.power, f"от атаки монстра {self.name}")

monsters = [
Monster("Гоблин", 40,10, 10, 5),
Monster("Паук", 60,15, 20, 5),
Monster("Скелет", 80,20, 30, 5),
Monster("Зомби", 100,25, 40, 5),
Monster("Голем(Босс #1)", 150,40, 100, 15),
Monster("Заклинатель Скверны", 180,80, 150, 20),
Monster("Некромант", 250,150, 200, 20),
Monster("Падший Маг Скверны", 300,200, 230, 20),
Monster("Рыцарь смерти", 600,200, 250, 20),
Monster("Король Скверны(Босс №2)", 800,250, 400, 30),
Monster("Бес", 1000,350, 600, 35),
Monster("Демон", 1200,400, 750, 35),
Monster("Принц Ада", 1500,700, 1000, 35),
Monster("Убийца богов", 1750,850, 1250, 35),
Monster("Король Ада(Босс #3)", 2000,1000, 5000, 100),
Monster("&#$@?#}&%", 2500,1500, 5000, 1000)]

#test_sword = Weapon("тестовый меч", 10, 50, 0)

weapon_shop = [
Weapon("Лопата",  10,  10,  0),
Weapon("Ржавый меч",  60,  40,  0),
Weapon("Катана", 100, 100, 0),
Weapon('Меч "Убийца Демонов"', 1000, 500, 0)
]

workbench = [
Weapon("Костяной меч", 30, 0, 15),
Weapon("Сабля утопленика", 150, 0, 55),
Weapon("Посох скверны", 200, 0, 130)
]

def open_inventory(hero):
    while True:
        print(f"---------------------------\nВ руках:{hero.equipped_weapon.name} (Урон:{hero.equipped_weapon.power})")
        print("Инвентарь:")
        if not hero.inventory:
            print("Пусто")
        else:
            for weapon in hero.inventory:
                print(f"- {weapon.name}, Урон: {weapon.power}")
        print("1.Применить лучшее оружие")
        print("2.Выйти из инвентаря")
        choice = input("Выберите действие: ")
        if choice == "1":
            best_weapon = hero.equipped_weapon
            for weapon in hero.inventory:
                if weapon.power > best_weapon.power:
                    best_weapon = weapon
            print(f"{best_weapon.name} применен")
            hero.equipped_weapon = best_weapon
        if choice == "2":
            break

def open_weapon_shop(hero):
    while True:
        print(f"---------------------------\nТвое золото: {hero.gold}")
        print("0.Выход")
        for i, weapon in enumerate(weapon_shop, start=1):
            print(f"{i}.{weapon.name}, Урон:{weapon.power}, Цена: {weapon.gold_price} Золота")
        choice = input(f"Выберите действие(0-{len(weapon_shop)})")
        if choice == "0":
            break

        try:
            weapon = weapon_shop[int(choice) - 1]
            if hero.gold >= weapon.gold_price:
                if weapon in hero.inventory:
                    print(f"Меч {weapon.name} уже есть в инвенторе")
                else:
                    hero.gold -= weapon.gold_price
                    hero.inventory.append(weapon)
                    hero.equipped_weapon = weapon
                    print(f"Вы успешно приобрели и экипировали {weapon.name}")
            else:
                print("Недостаточно золота")
        except:
            print("Неверный ввод :( ")

def open_workbench(hero):
    while True:
        print(f"---------------------------\nТвой Моб-Лут: {hero.mob_loot}")
        print("0.Выход")
        for i, weapon in enumerate(workbench, start=1):
            print(f"{i}.{weapon.name}, Урон:{weapon.power}, Цена: {weapon.loot_price} Моб-Лута")
        choice = input(f"Выберите действие(0-{len(workbench)})")
        if choice == "0":
            break
        try:
            weapon = workbench[int(choice) - 1]
            if hero.mob_loot >= weapon.loot_price:
                if weapon in hero.inventory:
                    print(f"Меч {weapon.name} уже есть в инвенторе")
                else:
                    hero.mob_loot -= weapon.loot_price
                    hero.inventory.append(weapon)
                    hero.equipped_weapon = weapon
                    print(f"Вы успешно создали и экипировали {weapon.name}")
            else:
                print("Недостаточно Моб-Лута")
        except:
            print("Неверный ввод :( ")

def open_shop(hero, current_level):
    while True:
        print("\n---Магазин---")
        print(f"Твои ресурсы:{hero.gold} Золота, {hero.mob_loot} Моб-Лута")
        print("1.Купить зелье Регенерации(+50 HP) - 10 Золота")
        print("2.Купить зелье Здоровья(+30 к макс.HP) - 20 Золота")
        print("3.Верстак(Моб-Лут)")
        print('4.Магазин оружия(Золото)')
        print('5.Открыть инвентарь')
        print("6.Покинуть магазин")
        print("7.Сохранить и выйти")
        choice = input("Выбери действие(1-7)")

        if choice == "1":
            if hero.gold >= 10:
                hero.gold -= 10
                hero.heal(50)
                print("Приобретено зелье Регенерации(+50HP)")
            else:
                print("Недостаточно золота!")
        elif choice == "2":
            if hero.gold >= 20:
                hero.gold -= 20
                hero.max_hp += 30
                print(f"Приобретено зелье Здоровья. Теперь у него {my_hero.max_hp} макс.HP")
            else:
                print("Недостаточно золота!")
        elif choice == "3":
            open_workbench(hero)
        elif choice == "4":
            open_weapon_shop(hero)
        elif choice == "5":
            open_inventory(hero)
        elif choice == "6":
            print("Вы вышли из магазина\n---------------------------")
            break
        elif choice == "7":
            with open("save.txt", "w", encoding="utf8") as file:
                file.write(f"{hero.gold},{hero.power}, {hero.max_hp}, {current_level}, {hero.mob_loot}, {hero.equipped_weapon.name}")
            quit()
        else:
            print("Неверный ввод >=( ")

#my_hero = Hero(input("Придумайте имя герою: "), 100, 20, 50)
try:
     with (open("save.txt", "r", encoding="utf8") as file):
        data = file.read().split(",")
        gold = int(data[0])
        power = int(data[1])
        max_hp = int(data[2])
        level_index = int(data[3])
        mob_loot = int(data[4])
        weapon_name = data[5]
        my_hero = Hero("Хиро", max_hp, power, gold, mob_loot)
        for w in weapon_shop + workbench:
            if w.name == weapon_name:
                my_hero.equipped_weapon = w
                break
except:
    my_hero = Hero("Хиро", 100, 20, 50, 0)
    print(f"---------------------------\nСоздан герой {my_hero.name}, у него {my_hero.gold} золота\n---------------------------")
    input("Нажмите Enter чтобы начать бой...\n---------------------------")

    level_index = 0
while level_index < len(monsters):
    if level_index == 5:
        print("---------------------------\nВнимание! Достигнута Арена Скверны\n---------------------------")
    if level_index == 10:
        print("---------------------------\nВнимание! Достигнута Демоническая Арена\n---------------------------")
    if level_index == 15:
        print("---------------------------\nВнимание! Достигнута Арена c Финальным боссом\n---------------------------")
    current_enemy=monsters[level_index]
    print(f"На арену выходит {current_enemy.name}")
    while my_hero.hp > 0 and  current_enemy.hp > 0:
        my_hero.attack(current_enemy)
        if current_enemy.hp > 0:
            current_enemy.attack(my_hero)
        input("Нажмите Enter чтобы продолжить...\n---------------------------")
    if my_hero.hp > 0:
        print(f"Победа! Ты получаешь {current_enemy.reward} золота\n---------------------------")
        my_hero.gold += current_enemy.reward
        my_hero.mob_loot += current_enemy.loot
        level_index += 1
        open_shop(my_hero, level_index)
    else:
        print("Поражение. Игра окончена...")
        break
if my_hero.hp > 0:
    print("Вы прошли все арены и победили всех боссов. Поздравляю с победой")
