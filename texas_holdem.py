import random
from dataclasses import dataclass, field
from typing import List

@dataclass
class Card:
    rank: str
    suit: str

    def __str__(self):
        return f"{self.rank}{self.suit}"

@dataclass
class Deck:
    ranks: List[str] = field(default_factory=lambda: list("23456789TJQKA"))
    suits: List[str] = field(default_factory=lambda: ["♠", "♥", "♦", "♣"])
    cards: List[Card] = field(init=False)

    def __post_init__(self):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        random.shuffle(self.cards)

    def deal(self, num: int) -> List[Card]:
        return [self.cards.pop() for _ in range(num)]

@dataclass
class Player:
    id: int
    hand: List[Card] = field(default_factory=list)

    def __str__(self):
        return f"Player {self.id}: {' '.join(str(c) for c in self.hand)}"

@dataclass
class TexasHoldem:
    num_players: int = 5
    players: List[Player] = field(init=False)
    community_cards: List[Card] = field(default_factory=list)
    deck: Deck = field(default_factory=Deck)

    def __post_init__(self):
        if self.num_players < 2 or self.num_players > 10:
            raise ValueError("Texas Hold'em supports between 2 and 10 players")
        self.players = [Player(i+1) for i in range(self.num_players)]

    def deal_hole_cards(self):
        for _ in range(2):
            for player in self.players:
                player.hand.append(self.deck.deal(1)[0])

    def deal_flop(self):
        self.deck.deal(1)  # burn card
        self.community_cards.extend(self.deck.deal(3))

    def deal_turn(self):
        self.deck.deal(1)  # burn card
        self.community_cards.extend(self.deck.deal(1))

    def deal_river(self):
        self.deck.deal(1)  # burn card
        self.community_cards.extend(self.deck.deal(1))

    def play_round(self):
        self.deal_hole_cards()
        self.deal_flop()
        self.deal_turn()
        self.deal_river()

    def show_state(self):
        for player in self.players:
            print(player)
        print("Community:", " ".join(str(c) for c in self.community_cards))

if __name__ == "__main__":
    game = TexasHoldem()
    game.play_round()
    game.show_state()
