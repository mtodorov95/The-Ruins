import random


class Room:

    def __init__(self, level, room_num, room_type, gen_loot=None):
        self.level = level
        self.room_num = room_num
        self.room_type = room_type
        self.gen_loot = gen_loot
        self.loot = {}
        self.info = f'Room {self.level}-{self.room_num}'

    def room_loot(self, level):
        loot_pool = ['Coins', 'Potions']
        loot = {}
        if self.gen_loot:
            if self.room_type == ['Boss']:
                gold = random.randint(10, 40) + level * 5
                loot.setdefault(loot_pool[0], gold)
                potion = random.randint(1, 3)
                loot.setdefault(loot_pool[1], potion)
            else:
                gold = random.randint(3, 20) + level * 3
                loot.setdefault(loot_pool[0], gold)
                pot_chance = random.choice(['yes', 'no'])
                if pot_chance == 'yes':
                    potion = 1
                    loot.setdefault(loot_pool[1], potion)
        self.loot = loot


class Shop:

    def __init__(self, level, room_num, room_type, cust):
        self.level = level
        self.room_num = room_num
        self.room_type = room_type
        self.cust = cust
        self.armor = list(self.gen_armor())
        self.weapon = list(self.gen_weapon())
        self.tome = list(self.gen_tome())
        self.item_price = 150 + self.level * 75
        self.pot_price = 75 + self.level * 75
        self.bought = False

    def __str__(self):
        return 'A strange, clearly non-human creature is leaning on\none of the walls and beckons you to approach.\n' \
               '- Be at easy adventurer. I mean you no harm. But say...\n' \
               '- Can I interest you in a trade?\n'

    def gen_armor(self):
        metals = ['Fire-brass', 'Primal Steel', 'Sungold', 'Chaosmetal', 'Ancient Cobalt']
        fabrics = ['Battle Leather', 'Gleaming Linen', 'Stormsilk', 'Nightfiber', 'Darkweave']
        armor = ['Gauntlets', 'Helmet', 'Armor', 'Gloves', 'Hood', 'Robes']
        id = self.level - 1
        if id > 4:
            id = 4
        if self.cust.type != 'Mage':
            if self.cust.type != 'Rogue':
                rand_armor = f'{metals[id]} {random.choice(armor[:3])}'
                if 'Gauntlets' in rand_armor:
                    model = 'assets/items/gauntlets.png'
                elif 'Helmet' in rand_armor:
                    model = 'assets/items/helmet.png'
                elif 'Armor' in rand_armor:
                    model = 'assets/items/armor_h.png'
            else:
                rand_armor = f'{fabrics[id]} {random.choice(armor[2:5])}'
                if 'Hood' in rand_armor:
                    model = 'assets/items/hood.png'
                elif 'Gloves' in rand_armor:
                    model = 'assets/items/gloves.png'
                elif 'Armor' in rand_armor:
                    model = 'assets/items/armor_m.png'
        else:
            rand_armor = f'{fabrics[id]} {random.choice(armor[3:])}'
            if 'Hood' in rand_armor:
                model = 'assets/items/hood.png'
            elif 'Gloves' in rand_armor:
                model = 'assets/items/gloves.png'
            elif 'Robes' in rand_armor:
                model = 'assets/items/robes.png'
        return rand_armor, self.level * 2, model

    def gen_weapon(self):
        metals = ['Fire-brass', 'Primal Steel', 'Sungold', 'Chaosmetal', 'Ancient Cobalt']
        weapons = ['Sword', 'Axe', 'Mace', 'Dagger', 'Staff']
        attr = ['of Necromancy', 'of Deadly Portals', 'of Outlandish Solar Magic', 'of Pyromancy',
                'of Secret Lunar Magic', 'of Blood Magic', 'of Elemental Magic']
        id = self.level - 1
        if id > 4:
            id = 4
        if self.cust.type != 'Mage':
            rand_weapon = f'{metals[id]} {random.choice(weapons[:4])}'
            if 'Sword' in rand_weapon:
                model = 'assets/items/sword.png'
            elif 'Dagger' in rand_weapon:
                model = 'assets/items/dagger.png'
            elif 'Mace' in rand_weapon:
                model = 'assets/items/mace.png'
            elif 'Axe' in rand_weapon:
                model = 'assets/items/axe.png'
        else:
            rand_weapon = f'{metals[id]} {weapons[4]} {random.choice(attr)}'
            model = 'assets/items/staff.png'
        return rand_weapon, self.level * 2, model

    def gen_tome(self):
        attr = ['of Necromancy', 'of Deadly Portals', 'of Outlandish Solar Magic', 'of Pyromancy',
                'of Secret Lunar Magic', 'of Blood Magic', 'of Elemental Magic']
        rand_tome = f'Compendium {random.choice(attr)}'
        model = 'assets/items/tome.png'
        return rand_tome, self.level * 4, model

    def buy(self, item):
        if item == 'armor':
            remainder = self.cust.inv.get('Coins') - self.item_price
            self.cust.inv['Coins'] = remainder
            self.cust.eq_armor(self.armor)
            self.bought = True
        elif item == 'weapon':
            remainder = self.cust.inv.get('Coins') - self.item_price
            self.cust.inv['Coins'] = remainder
            self.cust.eq_weapon(self.weapon)
            self.bought = True
        elif item == 'tome':
            remainder = self.cust.inv.get('Coins') - self.item_price
            self.cust.inv['Coins'] = remainder
            self.cust.eq_tome(self.tome)
            self.bought = True
        elif item == 'potion':
            potion = {'Potions': 1}
            self.cust.add_to_inv(potion)
            remainder = self.cust.inv.get('Coins') - self.pot_price
            self.cust.inv['Coins'] = remainder