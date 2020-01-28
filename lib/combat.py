from lib.models.entity import Weapon
from lib.models.creature import Creature
from lib.models.player import Player


class CombatHandler():

    combat_instances = []

    def add_instance(self, instance: CombatInstance):
        self.combat_instances.append(instance)

    def advance_rounds(self):
        for instance in combat_instances:
            instance.advance_round()


class CombatInstance():
    
    participants = []
    waiting_participants = []
    waiting_removal = []

    def add_participant(self, participant: Creature):
        self.waiting_participants.append(participant)


    def remove_participant(self, participant: Creature):
        self.waiting_removal.append(participant)

    def advance_round(self):
        
        # Clear out your dead.
        for participant in self.waiting_removal:
            self.participants.remove(participant)

        # Are we waiting to add any new participants?
        for participant in self.waiting_participants:
            # Handle any pre-combat stuff now.
            participant.roll_initiative()
            # Add them to the battle.
            self.participants.append(participant)

        # Sort participants into initiative order.
        self.participants.sort(key=lambda x: x.initative, reverse=False)

        #TODO: Maybe change 'participant' to 'creature'?
        for participant in participants:
            roll = participant.roll_attack(participant.target)
            if roll != 1:
                particpant.target.message(f'{participant.name} attacks you!')
                participant.message(f'You attack {participant.target.name}!')
            if roll >= participant.target.armor_class:
                damage = participant.roll_damage()
                participant.target.take_damage(damage)
                participant.target.message(f'You take {damage} damage from {participant.name}'.)
                participant.message(f'You deal {damage} damage to {participant.target.name}'.)
                # Are they dead?
                if participant.target.dead:
                    # This will be decided in the Creature object.
                    participant.target.message(f'{participant.name} kills you!')
                    participant.message(f'You kill {participant.target.name}!')
                    # Remove them from the combat.
                    self.remove_participant(participant.target)
            else:
                participant.message(f'You miss {participant.target.name}!')
                participant.target.name(f'{participant.name} misses you!')

                # If we're not tracking the target in this instance then we should be.
                if participant.target not in self.participants and participant.target not in self.waiting_participants:
                    self.add_participant(participant.target)
