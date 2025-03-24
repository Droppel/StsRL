import numpy as np
import math
import typing

from stssim.player import Player
from stssim.enemies.enemy import Enemy
from stssim.cards.card import Card
from stssim.cards.strike import Strike
from stssim.cards.defend import Defend
from stssim.cards.ironclad.bash import Bash

class Combat():
    def __init__(self, enemy: Enemy):
        self.current_turn = 0
        
        self.drawpile = [i for i in range(11)]
        self.hand = []
        self.discardpile = []

        np.random.shuffle(self.drawpile)

        self.player = Player()

        self.enemy = enemy

        self.winner = 0 # 0: None, 1: Player, 2: Enemy

        self.next_turn()
    
    def get_card_from_id(self, card_id: int) -> Card:
        if card_id < 5:
            return Strike()
        if card_id < 10:
            return Defend()
        if card_id == 10:
            return Bash()
        return None

    def step(self, action):
        if action == 11:
            self.end_turn()
            return self.is_done(), True
        
        deckstate = self.get_deck_state()
        if deckstate[action] != 1: # Trying to play a card that is not in the hand
            return self.is_done(), False
        
        card: Card = self.get_card_from_id(action)

        if self.player.energy < card.cost: # Not enough energy to play the card
            return self.is_done(), False

        self.discardpile.append(action)
        self.hand.remove(action)
        card.play(self.player, self.enemy)
        self.player.energy -= card.cost

        return self.is_done(), True
    
    def get_deck_state(self):
        deckstate = np.zeros(11, dtype=np.int32)
        for card in self.hand:
            deckstate[card] = 1
        for card in self.discardpile:
            deckstate[card] = 2
        return deckstate
        
    def is_done(self):
        if self.player.health <= 0:
            self.winner = 2
            return True
        if self.enemy.health <= 0:
            self.winner = 1
            return True
        return False
    
    def end_turn(self):
        for card in self.hand:
            self.discardpile.append(card)
        self.hand = []
        self.enemy.block = 0
        self.enemy.do_turn(self.player)
        self.current_turn += 1
        self.next_turn()

    def next_turn(self):
        # Get new enemy intent
        self.enemy.update_intent(self.current_turn)
        
        # Tick buffs/debuffs
        if self.enemy.vulnerable > 0:
            self.enemy.vulnerable -= 1

        self.enemy.strength += self.enemy.ritual

        self.player.energy = 3
        self.player.block = 0
        self.draw_cards(5)
    
    def draw_cards(self, n):
        for i in range(n):
            self.draw_card()
    
    def draw_card(self):
        if len(self.drawpile) == 0:
            self.drawpile = self.discardpile
            self.discardpile = []
            np.random.shuffle(self.drawpile)
        self.hand.append(self.drawpile.pop())
    
    def print(self):
        print(f"Player: {self.player.health} HP, {self.player.energy} Energy, {self.player.block} Block")
        print(f"Enemy: {self.enemy.health} HP, {self.enemy.block} Block, {self.enemy.strength} Strength, {self.enemy.vulnerable} Vulnerable")
        print(f"Enemy Intent: {self.enemy.intent}")
        print(f"Hand: {self.hand}")