import random


class Npc:

    def __init__(self, hp, att, deff, type, level, manager):
        self.max_hp = hp
        self.hp = hp
        self.att = att
        self.deff = deff
        self.type = type
        self.name = self.type
        self.level = level
        self.xp_reward = self.level * 8 + random.randint(1, 6)
        self.loot = {}
        self.moves = ['Attack', 'Skill']
        self.manager = manager
        self.model = ''
        if self.type == 'Soldier':
            self.model = 'assets/char/soldier.png'
        if self.type == 'Champion':
            self.model = 'assets/char/champion.png'
        if self.type == 'Bandit':
            self.model = 'assets/char/bandit.png'
        if self.type == 'Sorcerer':
            self.model = 'assets/char/sorcerer.png'

    def __str__(self):
        return f'{self.type}\n\nLevel: {self.level}\nHP:{self.hp}\nATT:{self.att}\nDEF:{self.deff}'

    def spec_skill(self, arr=None):
        self.manager.enable()
        if self.type == 'Champion':
            heal = self.max_hp // 10 + self.level
            self.hp += heal
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.manager.fight.ids.enemy_heal.text = f'+{heal}'
            self.manager.fight.heal_anim(self.manager.fight.ids.enemy_heal)

    def fight(self, enemy):
        self.manager.fight.ids.char_nums.font_size = 32
        if self.type == 'Champion':
            if self.hp < self.max_hp / 2:
                move = random.choice(self.moves)
            else:
                move = 'Attack'
        else:
            move = 'Attack'
        if move == 'Attack':
            self.manager.fight.npc_att_anim(self.manager.fight.ids.npc_portrait)
            crit = False
            crit_chance = random.randint(1, 12)
            if crit_chance == 1 or crit_chance == 2:
                crit = True
                self.manager.fight.ids.char_nums.font_size = 52
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
                self.manager.fight.ids.char_nums.font_size = 32
            if miss:
                self.manager.fight.ids.char_nums.text = 'Miss'
                self.manager.fight.dmg_anim(self.manager.fight.ids.char_nums)
            else:
                enemy.hp -= attack
                if self.type == 'Bandit':
                    double = random.randint(1, 6)
                    if double == 1:
                        enemy.hp -= attack
                        self.manager.fight.ids.enemy_heal.text = 'Double slash'
                        self.manager.fight.buff_anim(self.manager.fight.ids.enemy_heal)
                self.manager.fight.ids.char_nums.text = f'-{attack}'
                self.manager.fight.dmg_anim(self.manager.fight.ids.char_nums)
        elif move == 'Skill':
            self.spec_skill(enemy)

    def npc_loot(self, level):
        loot_pool = ['Coins', 'Potions']
        loot = {}
        gold = random.randint(3, 20) + level * 2
        loot.setdefault(loot_pool[0], gold)
        pot_chance = random.randint(1, 10)
        if pot_chance == 1:
            potion = 1
            loot.setdefault(loot_pool[1], potion)
        self.loot = loot


class Boss(Npc):

    def __init__(self, hp, att, deff, type, level, manager, name):
        super().__init__(hp, att, deff, type, level, manager)
        self.name = name
        self.model = 'assets/char/boss.png'
        self.xp_reward = self.level * 10 + random.randint(4, 12)

    def __str__(self):
        return f'{self.name}\n\nHP:{self.hp}\nATT:{self.att}\nDEF:{self.deff}'

    def fight(self, enemy):
        self.manager.fight.ids.char_nums.font_size = 32
        if self.type == 'Champion':
            if self.hp < self.max_hp / 2:
                move = random.choice(self.moves)
            else:
                move = 'Attack'
        else:
            move = 'Attack'
        if move == 'Attack':
            self.manager.fight.npc_att_anim(self.manager.fight.ids.npc_portrait)
            crit = False
            crit_chance = random.randint(1, 12)
            if crit_chance == 1 or crit_chance == 2:
                crit = True
                self.manager.fight.ids.char_nums.font_size = 52
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
                self.manager.fight.ids.char_nums.font_size = 32
            if miss:
                self.manager.fight.ids.char_nums.text = 'Miss'
                self.manager.fight.dmg_anim(self.manager.fight.ids.char_nums)
            elif not miss:
                enemy.hp -= attack
                if self.type == 'Bandit':
                    double = random.randint(1, 6)
                    if double == 1:
                        enemy.hp -= attack
                        self.manager.fight.ids.enemy_heal.text = 'Double slash'
                        self.manager.fight.buff_anim(self.manager.fight.ids.enemy_heal)
                self.manager.fight.ids.char_nums.text = f'-{attack}'
                self.manager.fight.dmg_anim(self.manager.fight.ids.char_nums)
        elif move == 'Skill':
            self.spec_skill(enemy)

    def boss_loot(self, level):
        loot_pool = ['Coins', 'Potions']
        loot = {}
        gold = random.randint(15, 50) + level * 3
        loot.setdefault(loot_pool[0], gold)
        pot_chance = random.randint(1, 10)
        if pot_chance == 1:
            potion = 1
            loot.setdefault(loot_pool[1], potion)
        self.loot = loot