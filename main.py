#######################################################################################################################
#
# project main
#
# This program will simulate a game of UNO. The program will ask the user if they want to play a game of UNO. If the
# user says yes, the program will ask the user how many players they want to play with. The program will then create a
# deck of cards, deal 5 cards to each player, and deal a card to the discard pile. The program will loop through the
# players and ask each player to play a card. If the player has a playable card, then the program will ask the player
# to choose a card. If the player does not have a card that can be played, the program will draw a card for the player.
# The program will then check if the player has won the game. If the player has won the game, the program will print the
# player's name and end the game. If the player has not won the game, the program will move on to the next player.
#######################################################################################################################


from uno import Card, Deck, Player

# Use these in your input statement
#"\n:~Enter number of players (2-5) ~:"
"\t:~Choose a card color (Red, Green, Blue, Yellow, or Wild) ~:"
"\t:~Choose a card value (0-9, Skip, Reverse, +2, Color Change, +4) ~:"
"\t:~Choose a new color (Red, Green, Blue, Yellow) ~:"
"\t:~Choose a valid color (Red, Green, Blue, Yellow) ~:"
"\n:~Do you want to play a game of UNO? (yes/no) ~:"
"\n:~Do you want to play another round? (yes/no) ~:"

# Use these in your print statement
"Please enter a number between 2 and 5."
"\n{}'s turn. Current card: {}"
"\tYour hand: {}"
"\tPlayable cards: {}"
"\tInvalid card choice. Please choose a valid card from your hand."
"\tNo playable cards. Drawing a card."
"\nGame state:"
"\t{} is skipped!"
"\tDirection reversed!"
"\t{} draws two cards!"
"\tColor Changed to {}!"
"\t{} draws four cards!"
"\n-----{player.name} has won the round-----"
"Thanks for playing!\nGo Green!! Go White!!"

# Write your functions definitions here


def play_game():
    """ask user if they want to play a game of UNO"""
    while True:
        yes_or_no = input("\n:~Do you want to play a game of UNO? (yes/no) ~:")     # ask user if they want to play
        yes_or_no = yes_or_no.lower()   # convert the input to lowercase
        if yes_or_no == 'yes':     # check if user wants to play
            return True
        else:
            return False

def closing_function():
    """in this function the closing message will be printed to show that the gabe has completed
     and the program is done."""
    print("Thanks for playing!\nGo Green!! Go White!!")   # print the closing message


def player_num():
    """in this function the user will enter the number of players"""
    while True:
        number_of_players = input("\n:~Enter number of players (2-5) ~:")     # get the number of players
        if number_of_players.isdigit() and int(number_of_players) >= 2 and int(number_of_players) <= 5:
            number_of_players = int(number_of_players)  # convert the number of players to an integer
            return number_of_players    # return the number of players
        else:
            print("Please enter a number between 2 and 5.")   # print the message
            continue


def player_dictionary(p_num):
    """In this function, a dictionary of players will be created."""
    dict_of_players = {}   # create an empty dictionary
    for i in range(1, p_num+1):     # loop through the number of players
        dict_of_players[i] = Player(i)  # creates a dictionary of players
    return dict_of_players    # return the dictionary of players


def first_card_deal(deck, dict_of_players):
    """this function will deal the first 5 cards to each player"""
    for player in dict_of_players.values():     # loop through the players
        for j in range(5):  # deal 5 cards to each player
            player.draw_card(deck)  # deals card to the players


def players_turn(player, discard_pile, deck):
    """in this function the players turn is going to be determined based on the code below"""
    current_card = discard_pile[-1] # get the current card
    print(f"\n{player.name}'s turn. Current card: {current_card}") # print the current card
    print(f"\tYour hand: {player.hand}")   # print the player's hand
    playable_cards = []    # create an empty list
    for i in player.hand: # loop through the player's hand
        if i.color == current_card.color or i.value == current_card.value or i.is_wild: # check if the card is playable
            playable_cards.append(i)  # add the card to the playable cards
    if playable_cards == []:   # check if the player has no playable cards
        if deck.is_empty(): # check if the deck is empty
            deck.reset_deck(discard_pile) # reset the deck
            discard_pile = []  # create an empty discard pile
            discard_pile.append(deck.deal_card()) # deal a card to the discard pile
        player.draw_card(deck) # draw a card for the player
        print("\tNo playable cards. Drawing a card.") # print the message
        return None, discard_pile  # return None and the discard pile
    else:
        print(f"\tPlayable cards: {playable_cards}")   # print the playable cards
        return playable_cards, discard_pile     # return the playable cards and the discard pile


def choose_card(playable_cards, player, discard_pile):
    """in this function the player will be given the opportunity to choose a card to play"""
    while True:
        card_color = input("\t:~Choose a card color (Red, Green, Blue, Yellow, or Wild) ~:")
        card_value = input("\t:~Choose a card value (0-9, Skip, Reverse, +2, Color Change, +4) ~:")
        card = Card(card_color, card_value) # create a card object
        if card in playable_cards and card: # check if the card is in the playable cards
            player.play_card(card)  # play the card
            discard_pile.append(card)   # add the card to the discard pile
            return discard_pile, card   # return the discard pile and the card
        else:
            print("\tInvalid card choice. Please choose a valid card from your hand.")  # print the message
            print(f"\tPlayable cards: {playable_cards}")    # print the playable cards


def special_case(card, current_player, p_dict, clockwise, deck):
    """this is the special case function that will handle the special cases of the game"""
    if card.value == 'Skip': # check if the card is a skip card
        current_player = next_player(clockwise, current_player, p_dict)     # skip the player
        print(f"\t{p_dict[current_player].name} is skipped!")
    elif card.value == 'Reverse':   # check if the card is a reverse card
        clockwise = clockwise * -1   # reverse the direction of the game
        print("\tDirection reversed!")
    elif card.value == '+2':    # check if the card is a +2 card
        current_player = next_player(clockwise, current_player, p_dict)    # skip the player
        for i in range(2):  # draw two cards
            p_dict[current_player].draw_card(deck)  # draw two cards
        print(f"\t{p_dict[current_player].name} draws two cards!")  # print the message
    elif card.is_wild:  # check if the card is a wild card
        new_color = input("\t:~Choose a new color (Red, Green, Blue, Yellow) ~:")   # ask the player to choose a color
        while new_color not in ['Red', 'Green', 'Yellow', 'Blue']:  # check if the color is valid
            new_color = input("\t:~Choose a valid color (Red, Green, Blue, Yellow) ~:") # ask player to choose a color
        card.change_color(new_color)    # change the color of the card
        print(f"\tColor Changed to {new_color}!")   # print the message
        if card.value == '+4':  # check if the card is a +4 card
            current_player = next_player(clockwise, current_player, p_dict)   # skip the player
            for i in range(4):  # draw four cards
                p_dict[current_player].draw_card(deck)  # draw four cards
            print(f"\t{p_dict[current_player].name} draws four cards!") # print the message
    return clockwise, current_player    # return the direction and the current

def next_player(clockwise, current_player, p_dict):
    """ in this function determines the next player in the game"""
    next_num_player = ((current_player - 1 + clockwise) % len(p_dict)) + 1  # determines the next player
    return next_num_player  # returns the next player


def player_stats(p_dict):
    """this is the player stats function that will print the game state of the game"""
    print("\nGame state:")   # print the game state
    for i in p_dict.values():    # loop through the players
        print(i)   # print the player


def player_won(current_player, p_dict):
    """
    Args:this function checks if the player has won the game
        current_player:
        p_dict:

    Returns:

    """
    if p_dict[current_player].has_won():
        print(f"\n-----{p_dict[current_player].name} has won the round-----")
        return True
    else:
        return False


def main():
    """main function"""
    banner = """🌟🌟🌟 Welcome to the *Ultimate UNO Showdown*! 🌟🌟🌟

    💥 Prepare yourself for a thrilling, card-flipping adventure
    where alliances waver, strategies unfold, and only the
    sharpest tactician will claim the ultimate victory! 💥

    💥 Will you reverse the tide, skip ahead of your rivals,
    or drop that Wild Draw Four at the perfect moment to leave
    them in disarray? Let the games begin! 💥
    """
    print(banner)

    game_start = play_game()
    while game_start:
        p_num = player_num() # get the number of players
        p_dict = player_dictionary(p_num) # create a dictionary of players
        deck = Deck() # create a deck
        first_card_deal(deck, p_dict) # deals initial 5 cards to each player
        discard_pile = [] # create a discard pile
        discard_pile.append(deck.deal_card()) # deal a card to the discard pile
        clockwise = 1 # set the direction of the game
        current_player = 1
        while True:
            player = p_dict[current_player]
            playable_cards, discard_pile = players_turn(player, discard_pile, deck)
            if playable_cards:
                discard_pile, card = choose_card(playable_cards, player, discard_pile)
                clockwise, current_player = special_case(card, current_player, p_dict, clockwise, deck)
            winner = player_won(current_player, p_dict)
            if winner == True:
                break
            current_player = next_player(clockwise, current_player, p_dict)
            player_stats(p_dict)
        more = input("\n:~Do you want to play another round? (yes/no) ~:")
        if more.lower() == 'no':
            break
        else:
            continue

    closing_function()



# DO NOT MODIFY THE FOLLOWING 2 LINES.
# DO NOT WRITE ANYTHING AFTER THE FOLLOWING 2 LINES OF CODES
# All your code should be either in the main function
# or in another function.
if __name__ == "__main__":
    main()
