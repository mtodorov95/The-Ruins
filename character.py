import random


class Player:

    def __init__(self, name, type, manager):
        self.name = name
        self.type = type
        self.level = 1
        self.xp = 0
        self.next_level = 55
        self.inv = {}
        self.moves = ['Attack']
        self.manager = manager
        self.skill_points = 0
        self.head = ['Head', 0, 'assets/items/item_empty.png']
        self.chest = ['Chest', 0, 'assets/items/item_empty.png']
        self.hands = ['Hands', 0, 'assets/items/item_empty.png']
        self.weapon = ['Weapon', 0, 'assets/items/item_empty.png']

    def __str__(self):
        return f'{self.name}\n\n\nLevel: {self.level} ({self.xp}/{self.next_level} XP)\nClass:{self.type}\nHP:{self.hp}/{self.max_hp}\nATT:{self.att}\nDEF:{self.deff}'

    def eq_armor(self, item):
        if 'Gauntlets' in item[0] or 'Gloves' in item[0]:
            self.deff -= self.hands[1]
            self.hands = item
            self.deff += self.hands[1]
        elif 'Helmet' in item[0] or 'Hood' in item[0]:
            self.deff -= self.head[1]
            self.head = item
            self.deff += self.head[1]
        elif 'Armor' in item[0] or 'Robes' in item[0]:
            self.deff -= self.chest[1]
            self.chest = item
            self.deff += self.chest[1]

    def eq_weapon(self, item):
        self.att -= self.weapon[1]
        self.weapon = item
        self.att += self.weapon[1]

    def add_to_inv(self, to_add):
        new_coin_val = self.inv.get('Coins', 0) + to_add.get('Coins', 0)
        new_pot_val = self.inv.get('Potions', 0) + to_add.get('Potions', 0)
        new_inv = {'Coins': new_coin_val, 'Potions': new_pot_val}
        self.inv.update(new_inv)

    def use_potion(self):
        if self.hp != self.max_hp:
            if self.inv.get('Potions') > 0:
                new_val = self.inv.get('Potions') - 1
                self.inv['Potions'] = new_val
                self.hp += 20
                self.manager.fight.ids.char_heal.text = '+20'
                self.manager.fight.heal_anim(self.manager.fight.ids.char_heal)
                if self.hp > self.max_hp:
                    self.hp = self.max_hp

    def basic_attack(self, enemy):
        self.manager.fight.ids.enemy_nums.font_size = 32
        crit = False
        crit_chance = random.randint(1, 12)
        if crit_chance == 1 or crit_chance == 2:
            crit = True
            self.manager.fight.ids.enemy_nums.font_size = 52
        attack = (self.att - enemy.deff // 2) + random.randint(0, self.att//2)
        if attack < 0:
            attack = 0
        if crit:
            attack += self.att // 2
        miss = False
        lvl_diff = enemy.level - self.level
        miss_chance = random.randint(1, 15 - lvl_diff)
        if miss_chance == 1:
            miss = True
            self.manager.fight.ids.enemy_nums.font_size = 32
        if miss:
            self.manager.fight.ids.enemy_nums.text = 'Miss'
            self.manager.fight.dmg_anim(self.manager.fight.ids.enemy_nums)
        else:
            if crit:
                if isinstance(self, Mage):
                    self.mp += self.max_mp//10
                    if self.mp > self.max_mp:
                        self.mp = self.max_mp
            enemy.hp -= attack
            if self.type == 'Rogue':
                self.passive(enemy, attack)
            if enemy.hp <= 0:
                self.manager.reward()
            else:
                self.manager.fight.ids.enemy_nums.text = f'-{attack}'
                self.manager.fight.dmg_anim(self.manager.fight.ids.enemy_nums)

    def level_up(self):
        if self.xp == self.next_level:
            self.level += 1
            self.xp = 0
        elif self.xp > self.next_level:
            extra_xp = self.xp - self.next_level
            self.level += 1
            self.xp = 0 + extra_xp
        self.next_level += self.level * 12
        self.max_hp += self.level * 2
        if hasattr(self.manager.player, 'max_mp'):
            self.max_mp += self.level * 2
            self.mp = self.max_mp
        self.att += 1
        self.deff += 1
        self.hp = self.max_hp
        self.skill_points += 1

    def stat_increase(self, spec):
        if spec == 'hp':
            self.max_hp += self.level * 2
        elif spec == 'mp':
            self.max_mp += self.level * 2
        elif spec == 'att':
            self.att += 1
        elif spec == 'def':
            self.deff += 1
        self.hp = self.max_hp
        if hasattr(self.manager.player, 'max_mp'):
            self.mp = self.max_mp
        self.skill_points -= 1
        if self.skill_points == 0:
            self.manager.main.specs.dismiss()


class Berserker(Player):
    def __init__(self, name, type, manager):
        self.hp = 120
        self.att = 8
        self.deff = 12
        self.max_hp = self.hp
        super().__init__(name, type, manager)
        self.moves.append('Enrage')
        self.rage = False

    def spec_skill(self, enemy=None):
        hp_cost = self.max_hp // 5
        rage_att = self.att * 2
        if not self.rage:
            if self.hp > hp_cost:
                self.rage = True
                self.att = rage_att
                self.hp -= hp_cost
                self.manager.fight.ids.char_heal.text = f'Enraged\n-{hp_cost} HP'
                self.manager.fight.buff_anim(self.manager.fight.ids.char_heal)
                enemy.fight(self)
            else:
                self.manager.fight.ids.char_nums.text = 'Not enough HP'
                self.manager.fight.dmg_anim(self.manager.fight.ids.char_nums)
                self.manager.enable()
        elif self.rage:
            self.manager.fight.ids.char_heal.text = 'Already enraged'
            self.manager.fight.buff_anim(self.manager.fight.ids.char_heal)
            self.manager.enable()


class Rogue(Player):

    def __init__(self, name, type, manager):
        self.hp = 90
        self.att = 9
        self.deff = 8
        self.max_hp = self.hp
        super().__init__(name, type, manager)
        self.moves.append('Flurry')
        self.flurry = False

    def passive(self, arr, dmg):
        if not self.flurry:
            double = random.randint(1, 6)
            if double == 1:
                arr.hp -= dmg
                self.manager.fight.ids.char_heal.text = 'Double slash'
                self.manager.fight.buff_anim(self.manager.fight.ids.char_heal)
        elif self.flurry:
            double = random.randint(1, 3)
            if double == 1:
                arr.hp -= dmg
                self.manager.fight.ids.char_heal.text = 'Double slash'
                self.manager.fight.buff_anim(self.manager.fight.ids.char_heal)

    def spec_skill(self, enemy=None):
        deff_cost = self.deff // 4
        if not self.flurry:
            self.flurry = True
            self.deff -= deff_cost
            self.manager.fight.ids.char_heal.text = f'Double slash x2\n-{deff_cost} DEF'
            self.manager.fight.buff_anim(self.manager.fight.ids.char_heal)
            enemy.fight(self)
        elif self.flurry:
            self.manager.fight.ids.char_heal.text = f'Already active'
            self.manager.fight.buff_anim(self.manager.fight.ids.char_heal)
            self.manager.enable()


class Mage(Player):

    def __init__(self, name, type, manager):
        self.mp = 10
        self.hp = 80
        self.att = 11
        self.deff = 7
        self.max_hp = self.hp
        self.max_mp = self.mp
        super().__init__(name, type, manager)
        self.moves.append('Pyroblast')
        self.tome = ['Tome', 0, 'assets/items/item_empty.png']

    def __str__(self):
        return f'{self.name}\n\n\nLevel: {self.level} ({self.xp}/{self.next_level} XP)\nClass:{self.type}\nHP:{self.hp}/{self.max_hp}\nMP:{self.mp}/{self.max_mp}\nATT:{self.att}\nDEF:{self.deff}'

    def eq_tome(self, item):
        self.max_mp -= self.tome[1]
        self.tome = item
        self.max_mp += self.tome[1]

    def spec_skill(self, enemy=None):
        self.manager.enable()
        mp_cost = self.max_mp // 2 - self.level
        pyro = self.att + random.randint(3, self.att//2)
        if self.mp >= mp_cost:
            self.mp -= mp_cost
            self.manager.fight.ids.enemy_nums.text = f'-{pyro}'
            self.manager.fight.dmg_anim(self.manager.fight.ids.enemy_nums)
            enemy.hp -= pyro
            if enemy.hp <= 0:
                self.manager.reward()
            else:
                enemy.fight(self)
        else:
            self.manager.fight.ids.char_heal.text = 'Not enough MP'
            self.manager.fight.mana_anim(self.manager.fight.ids.char_heal)


class Paladin(Player):

    def __init__(self, name, type, manager):
        self.mp = 8
        self.hp = 110
        self.att = 8
        self.deff = 10
        self.max_hp = self.hp
        self.max_mp = self.mp
        super().__init__(name, type, manager)
        self.moves.append('Heal')
        self.tome = ['Tome', 0, 'assets/items/item_empty.png']

    def __str__(self):
        return f'{self.name}\n\n\nLevel: {self.level} ({self.xp}/{self.next_level} XP)\nClass:{self.type}\nHP:{self.hp}/{self.max_hp}\nMP:{self.max_mp}/{self.max_mp}\nATT:{self.att}\nDEF:{self.deff}'

    def eq_tome(self, item):
        self.max_mp -= self.tome[1]
        self.tome = item
        self.max_mp += self.tome[1]

    def spec_skill(self, enemy=None):
        mp_cost = self.max_mp // 3 - self.level
        if self.mp >= mp_cost:
            heal = self.max_hp // 10 + self.level + random.randint(1, 3)
            self.hp += heal
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.mp -= mp_cost
            self.manager.fight.ids.char_heal.text = f'+{heal}'
            self.manager.fight.heal_anim(self.manager.fight.ids.char_heal)
            enemy.fight(self)
        else:
            self.manager.fight.ids.char_heal.text = 'Not enough MP'
            self.manager.fight.mana_anim(self.manager.fight.ids.char_heal)
            self.manager.enable()