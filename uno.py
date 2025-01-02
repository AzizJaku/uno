import random
random.seed(100)

class Card:
    """
    Represents a card in the UNO game.

    Attributes:
        color (str or "Wild"): The color of the card ('Red', 'Green', 'Blue', 'Yellow'), or "Wild" for wild cards.
        value (str): The value of the card ('0-9', 'Skip', 'Reverse', 'Draw Two' (+2), 'Color Change', 'Draw Four' (+4)).
        is_wild (bool): A boolean indicating whether the card is a wild card.
    """
    # List of valid colors: 'Red', 'Green', 'Blue', 'Yellow' or 'Wild' for wild
    color_list = ['Red', 'Green', 'Blue', 'Yellow', 'Wild']

    # List of valid values: '0-9', 'Skip', 'Reverse', 'Draw Two' (+2), 'Draw Four' (+4), 'Color Change'
    value_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2', '+4', 'Color Change']

    wild_cards = ['Color Change', '+4']

    def __init__(self, color, value):
        """
        Initializes a card with a color and value.

        Args:
            color (str or ""): The color of the card, or "" for wild cards.
            value (str): The value of the card.
        """
        self.color = ""
        self.value = ""
        self.is_wild = False

        # Verify that color and value are within the valid values, then update instance variables if valid.
        if color in self.color_list and value in self.value_list:
            # Boolean to check if it's a wild card. Wild cards are 'Color Change' and '+4'
            self.is_wild = value in self.wild_cards
            self.color = color
            self.value = value

            if (self.is_wild and color != "Wild") or (not self.is_wild and color == "Wild"):
                print(f"Invalid wild card setup: {color} {value}")
                self.color = ""
                self.value = ""

    def change_color(self, new_color):
        """
        Changes the color of a wild card to the specified new color.

        Args:
            new_color (str): The new color to set for the card. Must be one of 'Red', 'Green', 'Blue', or 'Yellow'.
        """
        if self.is_wild and new_color in self.color_list[:4]:
            self.color = new_color

    def __str__(self):
        """
        Returns a string representation of the card usually for printing.
        """
        if self.is_wild:
            return f"Wild - {self.value}"
        else:
            return f"{self.color} {self.value}"


    def __repr__(self):
        """
        Returns a string representation of the card for use in the shell.
        """
        return self.__str__()


    def __eq__(self, other):
        """
        Returns if 2 cards are equal. Two cards are equal if both their color and value
        are equal or both are a Wild card with the same value
        """
        if isinstance(other, Card):
            if not self.is_wild:
                return self.color == other.color and self.value == other.value
            else:
                return self.value == other.value
        else:
            return False

    def __bool__(self):
        """
        Returns the truthiness of a Card instance.

        A Card instance is considered True if it has both a color and a value.
        If either the color or the value is missing (e.g., an empty string),
        the Card instance will evaluate to False in a boolean context.

        Returns:
            bool: True if both color and value are true, otherwise False.
        """
        # Define conditions for the card to be considered "truthy"
        return bool(self.color) and bool(self.value)



class Deck:
    """
    Represents a deck of UNO cards. Handles the creation, shuffling, and drawing of cards.

    Attributes:
        __cards (list): A list of Card objects representing the deck.
    """
    colors = ['Red', 'Green', 'Blue', 'Yellow']
    values = [str(i) for i in range(10)] + ['Skip', 'Reverse', '+2']
    wild_cards = ['Color Change', '+4']

    def __init__(self, pile = None):
        """
        Initializes the deck with UNO cards and shuffles them.

        Args:
            pile (list of Cards, optional): A list of Card objects representing the discard pile.
                If provided, initializes the deck with these cards.
                If not, creates a full UNO deck.
        """

        self.__cards = []
        if pile:
            self.reset_deck(pile)  # Initialize with pile if provided
        else:
            self.initialize_full_deck()  # Initialize with a full deck if no pile is provided

    def reset_deck(self, pile):
        """
        Resets the deck from the provided discard pile and shuffles it.

        Args:
            pile (list of Card): The pile from which to create the deck.
        """
        if not isinstance(pile, list) or not all(isinstance(card, Card) for card in pile):
            print("Pile must be a list of Card instances.")
            return None

        # Initialize deck from the provided discard pile
        self.__cards = list(pile)  # Make a copy of the pile to avoid modifying the original

        # Reset all wild cards' color to "Wild"
        for card in self.__cards:
            if card.value in ['Color Change', '+4']:
                card.color = "Wild"

        # Shuffle the deck
        random.shuffle(self.__cards)

    def initialize_full_deck(self):
        """
            Creates a full UNO deck with all colors and wild cards, and shuffles it.
        """


        # Generate color cards
        self.__cards = [Card(color, value) for color in self.colors for value in self.values]

        # Generate and add the wild cards: : 4 cards of each kind
        self.__cards += [Card("Wild", wild) for wild in self.wild_cards for _ in range(4)]

        # Shuffle the deck
        random.shuffle(self.__cards)

    def deal_card(self):
        """
        Draws a card from the deck.

        Returns:
            Card or None: The card drawn from the top of the deck, or None if the deck is empty.
        """
        if self.is_empty():
            print("Deck is empty. No cards to deal.")
            return None
        return self.__cards.pop()

    def is_empty(self):
        """
        check if a deck is empty. It returns True if there are no cards in the deck.
        Otherwise, it returns False.
        """
        return not self.__cards

    def __len__(self):
        """
        returns the number of cards in the deck
        """
        return len(self.__cards)

    def __str__(self):
        """ Return string representing deck (usually for printing). """
        return ", ".join([str(card) for card in self.__cards])

    def __repr__(self):
        """ Return string representing deck (for use in shell). """
        return self.__str__()

    def display(self, cols=5):
        """ Column-oriented display of deck which is helpful for debugging and visualization."""
        for index, card in enumerate(self.__cards):
            if index % cols == 0:
                print()
            print(f"{str(card):20}", end=" ")
        print("\n")


# Player class representing a player
class Player:
    """
    Represents a player in the UNO game.

    Attributes:
        name (str): The name of the player (e.g., 'Player #1').
        hand (list): A list of Card objects representing the player's hand.
    """
    def __init__(self, player_number):
        """
        Initializes a player with a name based on their player number.

        Args:
            player_number (int): The player's number (e.g., 1 for 'Player #1').
        """
        # Initialize the player name using the player number
        self.name = f"Player #{player_number}"
        self.hand = []

    def draw_card(self, deck):
        """
        Adds the drawn card from the deck to the player's hand.

        Args:
            deck (Deck): The deck from which to draw the card.
        """

        card = deck.deal_card()
        if card:
            self.hand.append(card)
        else:
            print(f"No cards to draw for {self.name}.")

    def __contains__(self, card):
        """Allow checking if a card is in the player's hand."""
        return card in self.hand

    def play_card(self, card):
        """
        Plays a card from the player's hand

        Args:
            card (Card): The card the player wants to play.

        Returns:
            Card or None: The card if it's a valid move, otherwise None.
        """
        if card in self.hand:
            self.hand.remove(card)
            return card
        print(f"{card} not found in hand.")  # Optional: prints a message when the card isn’t found.
        return None  # Return None if the card is not in the player's hand


    def has_won(self):
        """
        Checks if the player has won (i.e., no cards left in hand).

        Returns:
            bool: True if the player has no cards left, False otherwise.
        """
        return len(self.hand) == 0

    def __str__(self):
        """
        Returns a string representation of the player and the number of cards in their hand.
        """
        return f"{self.name} - {len(self.hand)} cards"

    def __repr__(self):
        """
        Returns a string representation of the player.
        """
        return self.__str__()
