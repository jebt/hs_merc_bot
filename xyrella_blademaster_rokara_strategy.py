import config
from merc_lib import click, wait
import pyautogui
import card_in_hand_positions as hand
import logging
# xyrella, blademaster, rokara: 4/6, 5/5, 3/4 (with tirion, scabbs, tamsin)


class XyrellaBlademasterRokaraStrategy:
    def __init__(self):
        self.battle_action_imgs = [
            config.XYRELLA_TARGETED_ATTACK,
            config.BLADEMASTER_TARGETED_ATTACK,
            config.ROKARA_TARGETED_ATTACK,
            config.CLICK_TO_CONTINUE_IMG,
            config.GREEN_READY_BUTTON_IMG,
            config.CLICK_TO_CONTINUE_IMG2,
            config.CLICK_TO_CONTINUE_IMG3,
        ]

        self.hand_positions_with_original = (
            hand.CARD_4_OF_6,
            hand.CARD_5_OF_5,
            hand.CARD_3_OF_4,
        )

        self.hand_positions_with_scabbs_malfurion_cornelius = (  # same for diablo instead of malfurion
            hand.CARD_3_OF_6,
            hand.CARD_3_OF_5,
            hand.CARD_2_OF_4,
        )

        self.hand_positions_with_tirion_grom_diablo = (
            hand.CARD_4_OF_6,
            hand.CARD_4_OF_5,
            hand.CARD_3_OF_4,
        )

        self.hand_positions_with_tirion_tamsin_diablo = (
            hand.CARD_3_OF_6,
            hand.CARD_4_OF_5,
            hand.CARD_2_OF_4
        )

        self.hand_positions = self.hand_positions_with_tirion_tamsin_diablo

    def play_mercs(self):
        for position in self.hand_positions:
            click(position)
            click(config.RIGHT_SIDE_OF_BOARD)
        click(config.READY_BUTTON)
        wait(5)

    def battle_loop_core(self, no_ideal_options_counter):
        neeru = pyautogui.locateCenterOnScreen(config.NEERU_FIREBLADE_IMG, confidence=0.9)
        if neeru:
            target = neeru
        else:
            target = config.SAFE_BET_ENEMY_MINION_LOCATION
        for img in self.battle_action_imgs:
            loc = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if loc:
                no_ideal_options_counter = -1
                logging.info(f"Detected {img.filename}! Clicking...")
                click(loc)
                if "targeted_attack" in img.filename:
                    click(target)
                elif "click_to_continue" in img.filename:
                    click(config.HARMLESS_CLICK_LOCATION)
                    click(config.HARMLESS_CLICK_LOCATION)
                elif "green_ready_button" in img.filename:
                    wait(5)  # combat actions resolving
            wait(0.5)
        return no_ideal_options_counter
