import random

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from character import Player, Berserker, Mage, Paladin, Rogue
from npc import Npc, Boss
from room import Room, Shop

LabelBase.register(name='War', fn_regular='text/VecnaBold-4YY4.ttf')


class WelcomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.version = '0.4b'

    def on_leave(self, *args):
        lore = Popup(title=f'Danger', title_align='center', title_size=36, title_font='War',
                     title_color=[1, 0, 0, 1],
                     size_hint=(0.7, 0.6),
                     separator_color=[1, 0.6, 0.1, 1],
                     content=Label(
                         text=f"***\nTurn around and flee\nNone who enter here ever come back out\n***\n\n\n\n- Or so the sign in front"
                              f" of the entrance to the ruins reads.\nBut you certainly haven't come all this way just to turn back.",
                         font_size=20, font_name='War', halign='center'),
                     background='assets/misc/popup_blue.png')
        lore.open()


class CharScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def select(self, arg):
        if arg.state == 'down':
            arg.background_color = 1, 1, 1, 1
        else:
            arg.background_color = 1, 1, 1, 0.5

    def classes(self, instance, value):
        if value:
            self.manager.classes = instance.name

    def get_name(self):
        name = self.ids.char_name.text
        self.manager.name = name
        if name != '' and self.manager.classes != '':
            self.ids.confirm.disabled = False

    def on_leave(self, *args):
        self.ids.char_name.text = ''
        self.ids.confirm.disabled = True


class MainScreen(Screen):
    specs = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.ids.portrait.source = f'assets/char/{self.manager.classes}.png'
        self.ids.head_model.source = self.manager.player.head[2]
        self.ids.head.text = f'+{self.manager.player.head[1]} DEF' if self.manager.player.head[1] != 0 else ''
        self.ids.chest_model.source = self.manager.player.chest[2]
        self.ids.chest.text = f'+{self.manager.player.chest[1]} DEF' if self.manager.player.chest[1] != 0 else ''
        self.ids.hands_model.source = self.manager.player.hands[2]
        self.ids.hands.text = f'+{self.manager.player.hands[1]} DEF' if self.manager.player.hands[1] != 0 else ''
        self.ids.weapon1_model.source = self.manager.player.weapon[2]
        self.ids.weapon1.text = f'+{self.manager.player.weapon[1]} ATT' if self.manager.player.weapon[1] != 0 else ''
        if self.manager.player.type == 'Mage' or self.manager.player.type == 'Paladin':
            self.ids.weapon2_model.source = self.manager.player.tome[2]
            self.ids.weapon2.text = f'+{self.manager.player.tome[1]} MP' if self.manager.player.tome[1] != 0 else ''
        else:
            self.ids.weapon2.text = 'Locked'
            self.ids.weapon2_model.source = 'assets/items/item_locked.png'
        if self.manager.player.hp != self.manager.player.max_hp:
            restore = (self.manager.player.max_hp - self.manager.player.hp) // 2
            self.manager.player.hp += restore
            if self.manager.player.hp > self.manager.player.max_hp:
                self.manager.player.hp = self.manager.player.max_hp
        if hasattr(self.manager.player, 'max_mp'):
            self.manager.player.mp = self.manager.player.max_mp
        Clock.schedule_interval(self.update, 1.0/30)

    def inventory(self):
        preview = ''
        for item, amount in self.manager.player.inv.items():
            if amount != 0:
                preview += (f'{amount} {item}\n')
        return preview

    def spec_select(self):
        hp_btn = Button(text=f'Health + {self.manager.player.level * 2}',
                        font_name='War', font_size=18,
                        size_hint=(0.6, 0.2),
                        pos_hint={'center_x':0.5},
                        on_press=lambda x: self.manager.player.stat_increase('hp'),
                        background_down='assets/misc/std_btn_dis.png',
                        background_disabled_normal='assets/misc/std_btn_dis.png',
                        background_normal='assets/misc/std_btn.png')
        mp_btn = Button(text=f'Mana + {self.manager.player.level * 2}',
                        font_name='War',font_size=18,
                        size_hint=(0.6, 0.2),
                        pos_hint={'center_x': 0.5},
                        on_press=lambda x: self.manager.player.stat_increase('mp'),
                        background_down='assets/misc/std_btn_dis.png',
                        background_disabled_normal='assets/misc/std_btn_dis.png',
                        background_normal='assets/misc/std_btn.png')
        att_btn = Button(text=f'Attack + {1}', on_press=lambda x: self.manager.player.stat_increase('att'),
                         font_name='War',font_size=18,
                         size_hint=(0.6, 0.2),
                         pos_hint={'center_x': 0.5},
                         background_down='assets/misc/std_btn_dis.png',
                         background_disabled_normal='assets/misc/std_btn_dis.png',
                         background_normal='assets/misc/std_btn.png')
        def_btn = Button(text=f'Defence + {1}', on_press=lambda x: self.manager.player.stat_increase('def'),
                         font_name='War',font_size=18,
                         size_hint=(0.6, 0.2),
                         pos_hint={'center_x': 0.5},
                         background_down='assets/misc/std_btn_dis.png',
                         background_disabled_normal='assets/misc/std_btn_dis.png',
                         background_normal='assets/misc/std_btn.png')
        box = BoxLayout(orientation='vertical', spacing=10)
        box.add_widget(hp_btn)
        if hasattr(self.manager.player, 'max_mp'):
            box.add_widget(mp_btn)
        box.add_widget(att_btn)
        box.add_widget(def_btn)
        self.specs = Popup(title='Choose your specialization', title_align='center', title_size=24, title_font='War',
                           title_color=[1, 0.6, 0.1, 1],
                           size_hint=(0.5, 0.5),
                           separator_color=[1, 0.6, 0.1, 1],
                           content=box, background='assets/misc/popup_blue.png')
        self.specs.open()

    def update(self, dt):
        if self.manager.num != 0:
            self.ids.room.text = f'[color=rgba(198,27,41,255)]Current Room: {self.manager.level}-{self.manager.num}[/color]'
            self.ids.next_room.text = 'Next room'
        else:
            self.ids.room.text = '[color=rgba(198,27,41,255)]Outside[/color]'
            self.ids.next_room.text = 'Enter'
        self.ids.character.text = f'{self.manager.player.__str__()}'
        self.ids.inventory.text = f'{self.inventory() if self.manager.player.inv != {} else "Empty"}'
        self.ids.spec.text = f'Skill points({self.manager.player.skill_points})'
        if self.manager.player.skill_points > 0:
            self.ids.spec.disabled = False
        else:
            self.ids.spec.disabled = True
        if self.manager.player.inv.get('Potions', 0) > 0:
            self.ids.potion.disabled = False
        else:
            self.ids.potion.disabled = True


class FightScreen(Screen):
    init_att = NumericProperty()
    init_def = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def att_anim(self, arg):
        move = Animation(pos_hint={'center_x': 0.8}, duration=0.2) + Animation(pos_hint={'center_x': 0.6}, duration=0.2)
        move.bind(on_complete=lambda x,a:self.manager.npc.fight(self.manager.player) if self.manager.npc.hp > 0 else None)
        move.start(arg)

    def npc_att_anim(self, arg):
        move = Animation(pos_hint={'center_x': 0.2}, duration=0.2) + Animation(pos_hint={'center_x': 0.4}, duration=0.2)
        move.bind(on_complete=lambda x, a: self.manager.enable())
        move.start(arg)

    def dmg_anim(self, arg):
        fade = Animation(color=[1, 0, 0, 1], duration=0.3) + Animation(color=[1, 0, 0, 0], duration=0.3)
        fade.start(arg)

    def heal_anim(self, arg):
        fade = Animation(color=[0, 1, 0, 1], duration=0.3) + Animation(color=[0, 1, 0, 0], duration=0.3)
        fade.start(arg)

    def buff_anim(self, arg):
        fade = Animation(color=[1, 1, 0.2, 1], duration=0.3) + Animation(color=[1, 1, 0.2, 0], duration=0.3)
        fade.start(arg)

    def mana_anim(self, arg):
        fade = Animation(color=[0, 0.4, 0.6, 1], duration=0.3) + Animation(color=[0, 0.4, 0.6, 0], duration=0.3)
        fade.start(arg)

    def on_pre_enter(self, *args):
        self.ids.portrait.source = f'assets/char/{self.manager.classes}.png'
        self.ids.npc_portrait.source = self.manager.npc.model
        self.ids.btn1.text = self.manager.player.moves[0]
        self.ids.btn2.text = self.manager.player.moves[1]
        self.ids.leave.disabled = True
        self.ids.btn1.disabled = False
        self.ids.btn2.disabled = False
        self.init_att = self.manager.player.att
        self.init_def = self.manager.player.deff
        Clock.schedule_interval(self.update, 1.0/30)

    def on_leave(self, *args):
        self.manager.player.att = self.init_att
        self.manager.player.deff = self.init_def
        if hasattr(self.manager.player, 'rage'):
            self.manager.player.rage = False
        if hasattr(self.manager.player, 'flurry'):
            self.manager.player.flurry = False
        self.manager.level_check()

    def update(self, dt):
        self.ids.char_info.text = f'{self.manager.player.name}\n{self.manager.player.hp}/{self.manager.player.max_hp} HP\n'
        if hasattr(self.manager.player, 'max_mp'):
            self.ids.char_info.text += f'{self.manager.player.mp}/{self.manager.player.max_mp} MP'
        if hasattr(self.manager.npc, 'name'):
            self.ids.npc_info.text = f'{self.manager.npc.name}\n{self.manager.npc.hp}/{self.manager.npc.max_hp} HP'
        else:
            self.ids.npc_info.text = f'{self.manager.npc.type}\n{self.manager.npc.hp}/{self.manager.npc.max_hp} HP'
        self.ids.potions.text = f"Use\npotion x{self.manager.player.inv.get('Potions', 0)}"
        if self.manager.player.inv.get('Potions', 0) > 0:
            self.ids.potions.disabled = False
        else:
            self.ids.potions.disabled = True
        if self.manager.npc.hp <= 0:
            self.ids.btn1.disabled = True
            self.ids.btn2.disabled = True
            self.ids.leave.disabled = False
        if self.manager.player.hp <= 0:
            self.manager.death()
            self.manager.level = 1
            self.manager.num = 0
            self.manager.room = Room(self.manager.level, self.manager.num, 'Regular', False)
            self.manager.player = Berserker('name', 'default', self.manager)
            self.manager.current = 'char'


class ShopScreen(Screen):
    selection = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def choice(self, instance, value):
        if value:
            self.selection = instance.name

    def select(self, arg):
        if arg.state == 'down':
            arg.background_color = 1, 1, 1, 1
        else:
            arg.background_color = 1, 1, 1, 0.5

    def on_pre_enter(self, *args):
        self.ids.buy.disabled = True
        self.ids.item1.disabled = False
        self.ids.item2.disabled = False
        if hasattr(self.manager.player, 'max_mp'):
            self.ids.item3.disabled = False
        else:
            self.ids.item3.disabled = True
        self.ids.portrait.source = f'assets/char/{self.manager.classes}.png'
        self.ids.weapon.text = f'{self.manager.room.weapon[0]} +{self.manager.room.weapon[1]} ATT : {self.manager.room.item_price} Coins'
        self.ids.item1.background_normal = self.manager.room.weapon[2]
        self.ids.item1.background_down = self.manager.room.weapon[2]
        self.ids.armor.text = f'{self.manager.room.armor[0]} +{self.manager.room.armor[1]} DEF : {self.manager.room.item_price} Coins'
        self.ids.item2.background_normal = self.manager.room.armor[2]
        self.ids.item2.background_down = self.manager.room.armor[2]
        self.ids.tome.text = f'{self.manager.room.tome[0]} +{self.manager.room.tome[1]} MP : {self.manager.room.item_price} Coins\n'
        self.ids.item3.background_normal = self.manager.room.tome[2]
        self.ids.item3.background_down = self.manager.room.tome[2]
        self.ids.item3.background_disabled_normal = self.manager.room.tome[2]
        self.ids.potion.text = f'Potion : {self.manager.room.pot_price} Coins'
        Clock.schedule_interval(self.update, 1.0/30)

    def buy(self):
        if self.selection != 'potion':
            if self.manager.player.inv.get('Coins') >= self.manager.room.item_price:
                self.manager.room.buy(self.selection)
                title = 'Success'
                if self.selection == 'weapon':
                    l = Label(text=f"Bought {self.manager.room.weapon[0]}",font_size=18, font_name='War')
                elif self.selection == 'armor':
                    l = Label(text=f"Bought {self.manager.room.armor[0]}",font_size=18, font_name='War')
                elif self.selection == 'tome':
                    l = Label(text=f"Bought {self.manager.room.tome[0]}",font_size=18, font_name='War')
            else:
                title = 'Denied'
                l = Label(text="You don't have enough coins to afford that.",font_size=18, font_name='War')
        elif self.selection == 'potion':
            if self.manager.player.inv.get('Coins') >= self.manager.room.pot_price:
                self.manager.room.buy(self.selection)
                title = 'Success'
                l = Label(text='Bought a Potion',font_size=18, font_name='War')
            else:
                title = 'Denied'
                l = Label(text="You don't have enough coins to afford that.",font_size=18, font_name='War')
        transaction = Popup(title=title, title_align='center', title_size=24, title_font='War',
                            title_color=[1, 0, 0, 1],
                            size_hint=(0.4, 0.2),
                            separator_color=[1, 0.6, 0.1, 1],
                            content=l,
                            background='assets/misc/popup_blue.png')
        transaction.open()

    def update(self, dt):
        if isinstance(self.manager.room, Shop):
            self.ids.coins.text = f"{self.manager.player.inv.get('Coins', 0)}"
            if self.selection != '':
                self.ids.buy.disabled = False
            if not self.manager.room.bought:
                self.ids.msg.text = 'Choose one item that appeals to you. I also have as many Potions as you can afford.'
            else:
                self.ids.msg.text = 'Care for some Potions?'
                self.ids.item1.background_disabled_normal = self.manager.room.weapon[2]
                self.ids.item1.background_disabled_down = self.manager.room.weapon[2]
                self.ids.item1.disabled = True
                self.ids.item1.state = 'normal'
                self.ids.item2.background_disabled_normal = self.manager.room.armor[2]
                self.ids.item2.background_disabled_down = self.manager.room.armor[2]
                self.ids.item2.disabled = True
                self.ids.item2.state = 'normal'
                self.ids.item3.background_disabled_normal = self.manager.room.tome[2]
                self.ids.item3.background_disabled_down = self.manager.room.tome[2]
                self.ids.item3.disabled = True
                self.ids.item3.state = 'normal'


class Manager(ScreenManager):
    classes = StringProperty()
    name = StringProperty()
    player = ObjectProperty()

    room = ObjectProperty()

    npc = ObjectProperty()

    level = NumericProperty(1)
    num = NumericProperty(0)

    home = ObjectProperty()
    char = ObjectProperty()
    main = ObjectProperty()
    fight = ObjectProperty()
    shop = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room = Room(self.level, self.num, 'Regular', False)

    def create_char(self):
        if self.classes == 'berserker':
            player = Berserker(self.name, self.classes.capitalize(), self)
        elif self.classes == 'rogue':
            player = Rogue(self.name, self.classes.capitalize(), self)
        elif self.classes == 'mage':
            player = Mage(self.name, self.classes.capitalize(), self)
        elif self.classes == 'paladin':
            player = Paladin(self.name, self.classes.capitalize(), self)
        self.player = player

    def generate_room(self, prev_room, player):
        types = ['Regular', 'Loot', 'Shop', 'Boss']
        num = prev_room.room_num + 1
        if num == 10:
            num = 1
            level = prev_room.level + 1
        else:
            num = prev_room.room_num + 1
            level = prev_room.level
        if prev_room.room_type == types[3:]:
            num = 1
            level = prev_room.level + 1
        if num > 6:
            if num == 9:
                room_type = types[3:]
            else:
                if level == 1:
                    room_type = random.choices(types, [40, 10, 0, 50], k=1)
                else:
                    room_type = random.choices(types, [35, 5, 10, 50], k=1)
        else:
            if level == 1:
                room_type = random.choices(types[:3], [90, 10, 0], k=1)
            else:
                room_type = random.choices(types[:3], [85, 5, 10], k=1)
        if room_type == types[0]:
            loot_chance = random.randrange(2)
            if loot_chance == 1:
                gen_loot = True
            else:
                gen_loot = False
        else:
            gen_loot = True
        if room_type == ['Shop']:
            self.room = Shop(level, num, room_type, player)
        else:
            self.room = Room(level, num, room_type, gen_loot)
        self.level = level
        self.num = num
        self.enter_room()

    def random_npc(self, lvl):
        classes = ['Soldier', 'Bandit', 'Sorcerer', 'Champion']
        npc_class = random.choice(classes)
        if npc_class == 'Soldier':
            health = random.randint(45, 85) + lvl * 12
            attack = random.randint(4, 6) + lvl * 2
            defence = random.randint(6, 8) + lvl * 2
            npc = Npc(health, attack, defence, npc_class, lvl, self)
            self.npc = npc
        elif npc_class == 'Bandit':
            health = random.randint(35, 55) + lvl * 12
            attack = random.randint(5, 7) + lvl * 2
            defence = random.randint(4, 5) + lvl * 2
            npc = Npc(health, attack, defence, npc_class, lvl, self)
            self.npc = npc
        elif npc_class == 'Sorcerer':
            health = random.randint(30, 50) + lvl * 12
            attack = random.randint(7, 9) + lvl * 2
            defence = random.randint(2, 4) + lvl * 2
            npc = Npc(health, attack, defence, npc_class, lvl, self)
            self.npc = npc
        elif npc_class == 'Champion':
            health = random.randint(55, 75) + lvl * 12
            attack = random.randint(4, 6) + lvl * 2
            defence = random.randint(4, 6) + lvl * 2
            npc = Npc(health, attack, defence, npc_class, lvl, self)
            self.npc = npc

    def random_boss(self, lvl):
        classes = ['Soldier', 'Bandit', 'Sorcerer', 'Champion']
        names = ['Anael', 'Qaletaqa', 'Lexus', 'Manauia', 'Raimunde', 'Alexandrie', 'Alick', 'Alexandros', 'Reima',
                 'Ásmundr', 'Malandra', 'Sondra', 'Ezahl']
        titles = ['Destruction Sentinel', 'The Preserver', 'Harmony Guard', 'Grand Tranquility Guardian',
                  'The Void Guard',
                  'Amity Warden', 'Solitude Defender', 'The Timeless Guard', 'Soul Flayer', 'The Sanctum Keeper',
                  'Havoc Overseer']
        full_name = random.choice(names) + ', ' + random.choice(titles)
        boss_class = random.choice(classes)
        if boss_class == 'Soldier':
            health = random.randint(60, 100) + lvl * 22
            attack = random.randint(5, 7) + lvl * 3
            deffence = random.randint(7, 9) + lvl * 3
            boss = Boss(health, attack, deffence, boss_class, lvl, self, full_name)
            self.npc = boss
        elif boss_class == 'Bandit':
            health = random.randint(50, 70) + lvl * 22
            attack = random.randint(6, 8) + lvl * 3
            deffence = random.randint(5, 6) + lvl * 3
            boss = Boss(health, attack, deffence, boss_class, lvl, self, full_name)
            self.npc = boss
        elif boss_class == 'Sorcerer':
            health = random.randint(45, 65) + lvl * 22
            attack = random.randint(7, 9) + lvl * 3
            deffence = random.randint(3, 5) + lvl * 3
            boss = Boss(health, attack, deffence, boss_class, lvl, self, full_name)
            self.npc = boss
        elif boss_class == 'Champion':
            health = random.randint(75, 95) + lvl * 22
            attack = random.randint(5, 7) + lvl * 3
            deffence = random.randint(5, 7) + lvl * 3
            boss = Boss(health, attack, deffence, boss_class, lvl, self, full_name)
            self.npc = boss

    def fight_popup(self):
        enemy = Popup(title=f'Room: {self.level}-{self.num}', title_align='center', title_size=24, title_font='War',
                      title_color=[1, 0, 0, 1],
                      size_hint=(0.5, 0.5),
                      separator_color=[1, 0.6, 0.1, 1],
                      content=Label(
                          text=f'You have been spotted.\nViolence is the only solution.\n\n{self.npc.__str__()}',
                          font_size=20, halign='center', font_name='War'),
                      background='assets/misc/popup_blue.png')
        enemy.open()
        self.current = 'fight'

    def loot_room(self):
        self.room.room_loot(self.room.level)
        self.player.add_to_inv(self.room.loot)
        if self.room.gen_loot:
            loot = f'{self.room.loot.setdefault("Potions", 0)} Potion(s)\n{self.room.loot.get("Coins")} Coins'
        else:
            loot = 'No loot to be found here.'
        loot_room = Popup(title=f'Room: {self.level}-{self.num}', title_align='center', title_size=24, title_font='War',
                          title_color=[1, 0, 0, 1],
                          size_hint=(0.5, 0.5),
                          separator_color=[1, 0.6, 0.1, 1],
                          content=Label(
                              text=f"You don't see any enemies in here.\nSearching the room seems like a good plan.\n\n{loot}",
                              font_size=20, halign='center', font_name='War'),
                          background='assets/misc/popup_blue.png')
        loot_room.open()

    def shop_popup(self):
        shop = Popup(title=f'Room: {self.level}-{self.num}', title_align='center', title_size=24, title_font='War',
                     title_color=[1, 0, 0, 1],
                     size_hint=(0.6, 0.5),
                     separator_color=[1, 0.6, 0.1, 1],
                     content=Label(
                         text=self.room.__str__(),
                         font_size=20, halign='center', font_name='War'),
                     background='assets/misc/popup_blue.png')
        shop.open()
        self.current = 'shop'

    def enable(self):
        self.fight.ids.btn1.disabled = False
        self.fight.ids.btn2.disabled = False

    def fighting(self, btn):
        self.fight.ids.btn1.disabled = True
        self.fight.ids.btn2.disabled = True
        if btn.text == 'Attack':
            self.player.basic_attack(self.npc)
            self.fight.att_anim(self.fight.ids.portrait)
        else:
            self.player.spec_skill(self.npc)

    def enter_room(self):
        if self.room.room_type == ['Regular']:
            self.random_npc(self.room.level)
            self.fight.ids.npc_portrait.size_hint = 0.7, 0.6
            self.fight_popup()
        elif self.room.room_type == ['Boss']:
            self.random_boss(self.room.level)
            self.fight.ids.npc_portrait.size_hint = 0.8, 0.7
            self.fight_popup()
        elif self.room.room_type == ['Loot']:
            self.loot_room()
        elif self.room.room_type == ['Shop']:
            self.shop_popup()

    def reward(self):
        self.player.xp += self.npc.xp_reward
        self.npc.npc_loot(self.npc.level)
        self.player.add_to_inv(self.npc.loot)
        self.room.room_loot(self.room.level)
        self.player.add_to_inv(self.room.loot)
        if self.room.gen_loot:
            loot = f'{self.room.loot.setdefault("Potions", 0)} Potion(s).\n{self.room.loot.get("Coins")} Coins.'
        else:
            loot = 'No loot to be found here.'
        room_loot = Popup(title=f'Room Loot', title_align='center', title_size=24, title_color=[1, 0, 0, 1], title_font='War',
                          size_hint=(0.4, 0.3),
                          separator_color=[1, 0.6, 0.1, 1],
                          content=Label(text=loot, font_size=20, font_name='War', halign='center'),
                          background='assets/misc/popup_blue.png')
        room_loot.open()
        if hasattr(self.npc, 'name'):
            x = self.npc.name
        else:
            x = self.npc.type
        xp = Popup(title=f'Victory', title_align='center', title_size=24, title_color=[1, 0, 0, 1], title_font='War',
                   size_hint=(0.5, 0.5),
                   separator_color=[1, 0.6, 0.1, 1],
                   content=Label(
                       text=f'{x} has been killed.\nYou earned {self.npc.xp_reward} XP.\nYou found '
                            f'{self.npc.loot.setdefault("Potions", 0)} Potion(s) and\n{self.npc.loot.get("Coins")} '
                            f'Coins on the enemy.',
                       font_size=20, halign='center', font_name='War'), background='assets/misc/popup_blue.png')
        xp.open()

    def level_check(self):
        if self.player.xp >= self.player.next_level:
            self.player.level_up()
            label = Label(font_name='War',font_size=20)
            if hasattr(self.player, 'max_mp'):
                label.text = f'{self.player.name} has reached level {self.player.level}\n\nAll your stats have increased:' \
                             f'\nHealth: +{self.player.level * 2}\nMana: +{self.player.level * 2}\n' \
                             f'Attack: +{1}\nDefence: +{1}\nYour health has fully recovered.'
            else:
                label.text = f'{self.player.name} has reached level {self.player.level}\nAll your stats have increased:\n' \
                             f'Health: +{self.player.level * 2}\nAttack: +{1}\nDefence: +{1}\n' \
                             f'Your health has fully recovered.'
            level_up = BoxLayout()
            level_up.add_widget(label)
            level = Popup(title=f'Level Up', title_align='center', title_size=24, title_font= 'War',
                          title_color=[1, 0.6, 0.1, 1], size_hint=(0.5, 0.5), separator_color=[1, 0.6, 0.1, 1],
                          content=level_up, background='assets/misc/popup_blue.png')
            level.open()

    def death(self):
        dead = Popup(title=f'Defeat', title_align='center', title_size=28, title_font='War',
                     title_color=[1, 0, 0, 1],
                     size_hint=(0.7, 0.6),
                     separator_color=[1, 0.6, 0.1, 1],
                     content=Label(
                         text=f"You have been slain.\nAnd so the ruins await their next victim.",
                         font_size=24, font_name='War', halign='center'),
                     background='assets/misc/popup_red.png')
        dead.open()


class TheRuins(App):
    texture = ObjectProperty()

    def build(self):
        self.texture = Image(source='assets/tiles/bg_tile.png').texture
        self.texture.wrap = 'repeat'
        self.texture.uvsize = (8, 8)
        sm = Manager()
        return sm


game = TheRuins()
game.run()
