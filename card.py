# ============================================================
# FILE: card.py
# ============================================================
"""
Card class representing a single memory card.
"""
import pygame
from config import CARD_WIDTH, CARD_HEIGHT, WHITE, BLACK, GRAY, BLUE


class Card:
    """
    A single card in the memory game.
    """
    def __init__(self, symbol, index):
        """
        Initialize a card.
        
        Args:
            symbol (str): The symbol/text displayed on the card
            index (int): Unique identifier for this card instance
        """
        self.symbol = symbol
        self.index = index
        self.is_flipped = False
        self.is_matched = False
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        
    def flip(self):
        """Flip the card (only if not already matched)."""
        if not self.is_matched:
            self.is_flipped = not self.is_flipped
            
    def match(self):
        """Mark the card as matched."""
        self.is_matched = True
        self.is_flipped = False  # Hide matched cards
        
    def draw(self, surface, font, show_all=False):
        """
        Draw the card on the surface.
        
        Args:
            surface: Pygame surface to draw on
            font: Pygame font for text rendering
            show_all (bool): If True, show all cards (for debugging/endgame)
        """
        # Determine card color based on state
        if self.is_matched:
            # Matched cards are hidden (invisible) or shown as green
            color = (50, 200, 50)  # Green for matched
            border_color = (0, 150, 0)
            # Draw a subtle green box for matched cards
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=8)
            return
            
        # Card back (unflipped)
        if not self.is_flipped and not show_all:
            # Draw card back with pattern
            pygame.draw.rect(surface, BLUE, self.rect, border_radius=8)
            pygame.draw.rect(surface, (30, 80, 180), self.rect, 3, border_radius=8)
            
            # Add decorative pattern on back
            center_x = self.rect.centerx
            center_y = self.rect.centery
            # Draw a diamond pattern
            points = [
                (center_x, self.rect.top + 10),
                (self.rect.right - 10, center_y),
                (center_x, self.rect.bottom - 10),
                (self.rect.left + 10, center_y)
            ]
            pygame.draw.polygon(surface, (100, 150, 255), points, 2)
            # Inner diamond
            inner_points = [
                (center_x, self.rect.top + 20),
                (self.rect.right - 20, center_y),
                (center_x, self.rect.bottom - 20),
                (self.rect.left + 20, center_y)
            ]
            pygame.draw.polygon(surface, (150, 200, 255), inner_points, 1)
            
        # Card front (flipped or show_all)
        else:
            # Card face background
            pygame.draw.rect(surface, WHITE, self.rect, border_radius=8)
            pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
            
            # Render the symbol in the center
            text_surface = font.render(self.symbol, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
            
            # Add a subtle glow effect for flipped cards
            if self.is_flipped:
                glow = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                glow.fill((255, 255, 200, 30))
                surface.blit(glow, self.rect.topleft)
                
    def contains_point(self, pos):
        """
        Check if a point is inside the card.
        
        Args:
            pos (tuple): (x, y) position
            
        Returns:
            bool: True if point is inside the card
        """
        return self.rect.collidepoint(pos)
        
    def set_position(self, x, y):
        """Set the card's position on screen."""
        self.rect.x = x
        self.rect.y = y
