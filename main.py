# ============================================================
# FILE: main.py
# ============================================================
"""
Entry point for the Memory Card Matching Game.
"""
from game import MemoryGame


def main():
    """Start the game."""
    game = MemoryGame()
    game.run()


if __name__ == "__main__":
    main()
