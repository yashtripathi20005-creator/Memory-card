# ============================================================
# FILE: board.py
# ============================================================
"""
Board class managing the grid of cards.
"""
import random
import pygame
from card import Card
from config import (
    CARD_ROWS, CARD_COLS, CARD_WIDTH, CARD_HEIGHT, 
    CARD_MARGIN, SYMBOLS, SCREEN_WIDTH, SCREEN_HEIGHT
)


class Board:
    """
    The game board containing all cards in a grid.
    """
    def __init__(self):
        """Initialize the board with shuffled cards."""
        self.cards = []
        self.selected_cards = []  # Currently flipped cards (max 2)
        self.first_card_index = None
        self.second_card_index = None
        self.is_processing = False  # True during flip delay
        self.matched_pairs = 0
        self.total_pairs = len(SYMBOLS)
        
        self._create_cards()
        self._shuffle_cards()
        self._arrange_cards()
        
    def _create_cards(self):
        """Create card pairs with symbols."""
        # Each symbol appears twice
        self.cards = []
        for i, symbol in enumerate(SYMBOLS):
            # Create two cards with same symbol (pair)
            card1 = Card(symbol, i * 2)
            card2 = Card(symbol, i * 2 + 1)
            self.cards.append(card1)
            self.cards.append(card2)
            
    def _shuffle_cards(self):
        """Shuffle the card deck."""
        random.shuffle(self.cards)
        
    def _arrange_cards(self):
        """Arrange cards in a grid layout."""
        # Calculate total grid dimensions
        total_width = CARD_COLS * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN
        total_height = CARD_ROWS * (CARD_HEIGHT + CARD_MARGIN) - CARD_MARGIN
        
        # Center the grid on screen
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        # Place each card in the grid
        for index, card in enumerate(self.cards):
            row = index // CARD_COLS
            col = index % CARD_COLS
            x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
            y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
            card.set_position(x, y)
            
    def handle_click(self, pos):
        """
        Handle a mouse click on the board.
        
        Args:
            pos (tuple): (x, y) mouse position
            
        Returns:
            bool: True if a card was flipped
        """
        if self.is_processing:
            return False
            
        # Don't allow more than 2 cards selected
        if len(self.selected_cards) >= 2:
            return False
            
        # Find the clicked card
        for card in self.cards:
            if card.contains_point(pos) and not card.is_matched and not card.is_flipped:
                # Flip the card
                card.flip()
                self.selected_cards.append(card)
                
                # Check if we have two cards selected
                if len(self.selected_cards) == 2:
                    # Check for match
                    self.is_processing = True
                    return True
                return True
                
        return False
        
    def check_match(self):
        """
        Check if the two selected cards match.
        
        Returns:
            bool: True if they match
        """
        if len(self.selected_cards) != 2:
            return False
            
        card1, card2 = self.selected_cards
        
        if card1.symbol == card2.symbol and card1.index != card2.index:
            # Match found
            card1.match()
            card2.match()
            self.matched_pairs += 1
            self.selected_cards = []
            self.is_processing = False
            return True
        else:
            # No match - flip them back after delay
            return False
            
    def flip_back(self):
        """Flip the selected cards back (called after delay on no match)."""
        for card in self.selected_cards:
            card.flip()  # Flip back
        self.selected_cards = []
        self.is_processing = False
        
    def is_game_complete(self):
        """Check if all pairs have been matched."""
        return self.matched_pairs == self.total_pairs
        
    def draw(self, surface, font):
        """
        Draw all cards on the surface.
        
        Args:
            surface: Pygame surface
            font: Pygame font for text
        """
        for card in self.cards:
            card.draw(surface, font)
            
    def reset(self):
        """Reset the board for a new game."""
        self.selected_cards = []
        self.is_processing = False
        self.matched_pairs = 0
        self.first_card_index = None
        self.second_card_index = None
        
        # Reset all cards
        for card in self.cards:
            card.is_flipped = False
            card.is_matched = False
            
        # Reshuffle and rearrange
        self._shuffle_cards()
        self._arrange_cards()
