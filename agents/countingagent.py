from agents.unoagent import UnoAgent
from unotypes import *
import random
from collections import Counter
import numpy as np


def calculate_score(cards_left, hand, card):
    cards_left_stack = sum([1 for c in cards_left if c.stacks_on(card)])
    same_color_hand = sum([1 for c in hand if c.color == card.color])
    
    score = same_color_hand +  1/(cards_left_stack + 1) 
    
    match card.sign:
        case Sign.DRAW_FOUR:
            return score + 4
        case Sign.CHANGE_COLOR:
            return score + 3
        case Sign.DRAW_TWO:
            return score + 2
        case Sign.SKIP:
            return score + 1
    return score

class CountingAgent(UnoAgent):

    def get_action(self, observations, **kwargs) -> Action:
        last_observation = observations[-1]
        top_card = last_observation.top_card
        hand = last_observation.hand

        # Always accept draw four
        if last_observation.can_challenge_draw_four:
            return AcceptDrawFour()
        
        # Skip turn if drawn card and it doesn't stack
        if last_observation.previously_drawn_card:
            if not last_observation.previously_drawn_card.stacks_on(top_card):
                return SkipTurn()
        
        # The card count begins
        played_cards = Counter()
        for o in reversed(observations):
            if o.top_card.is_wild:
                played_cards[Card(sign=o.top_card.sign, color=None)] += 1
            else:
                played_cards[o.top_card] += 1
            if o.is_initial_state:
                break

        # All cards
        all_cards = Counter()
        non_wild_signs = [Sign(sign) for sign in Sign if not Sign(sign).is_wild]

        for c, s in itertools.product(Color, non_wild_signs):
            if s == Sign.ZERO:
                all_cards[Card(sign=s, color=c)] = 1
            else:
                all_cards[Card(sign=s, color=c)] = 2

        all_cards[Card(sign=Sign.CHANGE_COLOR, color=None)] = 4
        all_cards[Card(sign=Sign.DRAW_FOUR, color=None)] = 4

        not_played_yet = all_cards - played_cards

        played_green = sum([count for card, count in played_cards.items() if card.color == Color.GREEN])        
        played_yellow = sum([count for card, count in played_cards.items() if card.color == Color.YELLOW])        
        played_red = sum([count for card, count in played_cards.items() if card.color == Color.RED])
        played_blue = sum([count for card, count in played_cards.items() if card.color == Color.BLUE])

        my_green_cards = sum([1 for card in hand if card.color == Color.GREEN])
        my_yellow_cards = sum([1 for card in hand if card.color == Color.YELLOW])
        my_red_cards = sum([1 for card in hand if card.color == Color.RED])
        my_blue_cards = sum([1 for card in hand if card.color == Color.BLUE])

        my_no_color_cards = [card.sign for card in hand if not card.color]

        # Play draw 4 if in hand
        if Sign.DRAW_FOUR in my_no_color_cards:
            if Sign.CHANGE_COLOR in my_no_color_cards:
                # choose the color that has fewest cards left
                i = np.argmax([played_green, played_yellow, played_red, played_blue])
                match i:
                    case 0:
                        return PlayCard(Card(Sign.DRAW_FOUR, Color.GREEN))
                    case 1:
                        return PlayCard(Card(Sign.DRAW_FOUR, Color.YELLOW))
                    case 2:
                        return PlayCard(Card(Sign.DRAW_FOUR, Color.RED))
                    case 3:
                        return PlayCard(Card(Sign.DRAW_FOUR, Color.BLUE))
            else:
                # choose the color we have most of 
                i = np.argmax([my_green_cards, my_yellow_cards, my_red_cards, my_blue_cards])
                match i:
                    case 0:
                        return PlayCard(Card(Sign.DRAW_FOUR, Color.GREEN))
                    case 1:
                        return PlayCard(Card(Sign.DRAW_FOUR, Color.YELLOW))
                    case 2:
                        return PlayCard(Card(Sign.DRAW_FOUR, Color.RED))
                    case 3:
                        return PlayCard(Card(Sign.DRAW_FOUR, Color.BLUE))

        playable_cards = []
        for card in hand:
            if card.stacks_on(top_card):
                if card.is_wild:
                    playable_cards += [Card(sign=card.sign, color=Color.GREEN), Card(sign=card.sign, color=Color.YELLOW), 
                                        Card(sign=card.sign, color=Color.RED), Card(sign=card.sign, color=Color.BLUE)]
                else:
                    playable_cards.append(card)

        if playable_cards:
            i = np.argmax([calculate_score(not_played_yet.elements(), hand, card) for card in playable_cards])
            return PlayCard(playable_cards[i])
        else:
            return DrawCard()

