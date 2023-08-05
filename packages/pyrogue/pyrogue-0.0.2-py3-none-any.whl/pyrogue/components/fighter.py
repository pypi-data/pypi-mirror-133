from game_messages import Message
import curses

class Fighter:
    def __init__(self, hp, defense, power, mana=0, stamina=0):
        self.max_hp = hp
        self.hp = hp
        self.max_mana = mana
        self.mana = mana
        self.max_stamina = stamina
        self.stamina = stamina

        # Base defense and power
        self.defense = defense
        self.power = power
        self.conditions = []

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                            self.owner.name.capitalize(), target.name, str(damage)), curses.color_pair(1))})
            results.extend(target.fighter.take_damage(damage))

        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                            self.owner.name.capitalize(), target.name), curses.color_pair(1))})

        return results

    def _attack(self, target):
        results = []


        # Apply any active conditions
        for condition in self.conditions:
            pass
        for condition in target.conditions:
            pass

        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                            self.owner.name.capitalize(), target.name, str(damage)), curses.color_pair(1))})
            results.extend(target.fighter.take_damage(damage))

        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                            self.owner.name.capitalize(), target.name), curses.color_pair(1))})

        return results

