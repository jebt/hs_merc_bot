"""
hs_merc_bot.py
author: roelantvanderhilst@gmail.com
todo: visitor task priority list
todo: treasure priority list
todo: avoid elites
todo: deal with stealth target
todo: use the hearthstone log for playing mercs from hand and abilities/targets
todo: encounter selection should remember coordinates of encounters so it doesn't have to do horizontal again
todo: possible res node should only be added if aside from the res cue, also the visit button needs to be highlighted
"""
import pyautogui
import config
import enum
from merc_lib import click, wait, detect
from xyrella_blademaster_rokara_strategy import XyrellaBlademasterRokaraStrategy
import logging
from logging import info
import sys


class ExpectedOnScreenError(Exception):
    pass


class TakesTooLongError(Exception):
    pass


class CheckpointError(Exception):
    pass


class Checkpoint(enum.Enum):
    UNKNOWN = 1
    BOUNTY_SELECT = 2
    ENCOUNTER_SELECT = 3
    REWARDS_COLLECTION = 4
    TREASURE_SELECT = 5
    TO_BATTLE = 6


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25
strat = XyrellaBlademasterRokaraStrategy()
checkpoint = Checkpoint.UNKNOWN


# horizontal_direction_switch = "left_to_right" todo: remove


def wait_for_yellow_played_button():
    times_to_try = 60
    for i in range(times_to_try):
        if i % 5 == 0:
            info(f"Trying to detect Played button ({i + 1}/{times_to_try})...")
        played_button_region_screenshot = pyautogui.screenshot(region=config.PLAYED_BUTTON_REGION)
        if pyautogui.locate(played_button_region_screenshot, config.PLAYED_BUTTON_IMG, confidence=0.9):
            return True
        elif i < times_to_try - 1:
            wait(1)
    raise ExpectedOnScreenError(f"Could not detect Played button after {times_to_try} tries!")


def go_battle():
    global checkpoint
    checkpoint = Checkpoint.TO_BATTLE
    info("go_battle()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(10)
    wait_for_yellow_played_button()


def go_task():
    info("go_task()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(0.5)
    click(config.THIRD_VISITOR_LOCATION)
    click(config.CHOOSE_VISITOR_BUTTON)
    wait(0.5)
    click(config.CHOOSE_VISITOR_BUTTON)
    wait(3)


def go_res():
    info("go_res()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(5)


def go_warp():
    info("go_warp()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(5)


def go_boon():
    info("go_boon()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(0.5)
    click(config.TREASURE_SELECTION_CLICKING_POINT)
    wait(3)


def go_pick_up():
    info("go_pick_up()")
    logging.warning("THIS CAN BE RISKY! WE MIGHT DIE WITH THIS!")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(0.5)
    click(config.TREASURE_SELECTION_CLICKING_POINT)
    wait(5)


def go_sabotage():
    info("go_sabotage()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(10)  # because it might take long when the map is really big


def go(encounter):  # todo: replace with polymorphism
    if encounter == config.ENCOUNTER_SELECTION_WARP_BUTTON_IMG:
        go_warp()
    elif encounter == config.RES_CUE_IMG:
        go_res()
    elif encounter == config.SABOTAGE_CUE_IMG:
        go_sabotage()
    elif encounter == config.ENCOUNTER_SELECTION_PLAY_BUTTON_IMG:
        go_battle()
    elif encounter == config.ENCOUNTER_SELECTION_REVEAL_BUTTON_IMG:
        go_boon()
    elif encounter == config.ENCOUNTER_SELECTION_PICK_UP_BUTTON_IMG:
        go_pick_up()
    else:
        raise ValueError("Unknown encounter!")


def click_horizontal_for(preferable_encounter):
    for x_coord in config.TRY_ENCOUNTER_X_COORDS:
        click((x_coord, 500))
        if detect(preferable_encounter[0]):
            return


def get_preferable_encounter(available_encounters):
    for encounter in available_encounters:
        if available_encounters[encounter][1]:
            return encounter
    raise ValueError("No known encounters available!")


def alternative_encounter_selection():
    available_encounters = {  # todo: replace dictionary with class
        "warp": (config.ENCOUNTER_SELECTION_WARP_BUTTON_IMG, False),
        "res": (config.RES_CUE_IMG, False),
        "sabotage": (config.SABOTAGE_CUE_IMG, False),
        "battle": (config.ENCOUNTER_SELECTION_PLAY_BUTTON_IMG, False),
        "boon": (config.ENCOUNTER_SELECTION_REVEAL_BUTTON_IMG, False),
        "pick_up": (config.ENCOUNTER_SELECTION_PICK_UP_BUTTON_IMG, False),
    }
    for x_coord in config.TRY_ENCOUNTER_X_COORDS:
        click((x_coord, 500))
        if detect(config.ENCOUNTER_SELECTION_VISIT_BUTTON_IMG):
            if detect(config.TASK_CUE_IMG):
                go_task()
                return
        else:
            for encounter in available_encounters:
                if not available_encounters[encounter][1]:
                    available_encounters[encounter] = (
                        available_encounters[encounter][0],
                        not detect(available_encounters[encounter][0]) is None
                    )
    preferable_encounter = get_preferable_encounter(available_encounters)
    click_horizontal_for(available_encounters[preferable_encounter])
    go(available_encounters[preferable_encounter][0])


# def try_horizontal_for(image): todo: remove
#     global horizontal_direction_switch
#     x_coords = None
#     if horizontal_direction_switch == "left_to_right":
#         x_coords = config.TRY_ENCOUNTER_X_COORDS
#         horizontal_direction_switch = "right_to_left"
#     elif horizontal_direction_switch == "right_to_left":
#         x_coords = config.TRY_ENCOUNTER_X_COORDS[::-1]
#         horizontal_direction_switch = "left_to_right"
#     for x_coord in x_coords:
#         location = (x_coord, 500)
#         click(location)
#         if detect(image):
#             return True
#     return False


def button_is_already_active_because_only_one_option():
    if detect(config.ENCOUNTER_SELECTION_VISIT_BUTTON_IMG):
        if detect(config.TASK_CUE_IMG):
            go_task()
        elif detect(config.RES_CUE_IMG):
            go_res()
        elif detect(config.SABOTAGE_CUE_IMG):
            go_sabotage()
        else:
            raise ExpectedOnScreenError("Visit button highlighted but no TASK, RES or SABOTAGE cue!")
    elif detect(config.ENCOUNTER_SELECTION_PLAY_BUTTON_IMG):
        go_battle()
    elif detect(config.ENCOUNTER_SELECTION_REVEAL_BUTTON_IMG):
        go_boon()
    elif detect(config.ENCOUNTER_SELECTION_WARP_BUTTON_IMG):
        go_warp()
    elif detect(config.ENCOUNTER_SELECTION_PICK_UP_BUTTON_IMG):
        go_pick_up()
    else:
        return False
    return True


# def try_horizontal_for_various_visits():
#     if try_horizontal_for(config.ENCOUNTER_SELECTION_VISIT_BUTTON_IMG):
#         if detect(config.TASK_CUE_IMG):
#             go_task()
#         elif detect(config.RES_CUE_IMG):
#             go_res()
#         elif detect(config.SABOTAGE_CUE_IMG):
#             go_sabotage()
#         else:
#             raise ExpectedOnScreenError("Visit button highlighted but no TASK, RES or SABOTAGE cue!")
#     else:
#         return False
#     return True
#
#
# def try_horizontals():
#     if try_horizontal_for_various_visits():
#         # action is called in function
#         pass
#     elif try_horizontal_for(config.ENCOUNTER_SELECTION_PLAY_BUTTON_IMG):
#         go_battle()
#     elif try_horizontal_for(config.ENCOUNTER_SELECTION_WARP_BUTTON_IMG):
#         go_warp()
#     elif try_horizontal_for(config.ENCOUNTER_SELECTION_REVEAL_BUTTON_IMG):
#         go_boon()
#     elif try_horizontal_for(config.ENCOUNTER_SELECTION_PICK_UP_BUTTON_IMG):
#         go_pick_up()
#     else:
#         return False
#     return True


def encounter_selection():
    info("encounter_selection()")
    loop_count = 0
    while checkpoint == Checkpoint.ENCOUNTER_SELECT:
        if button_is_already_active_because_only_one_option():
            # action is called in deeper function
            continue
        # elif try_horizontals():
        #     # action is called in deeper function
        #     continue
        elif alternative_encounter_selection():
            # action is called in deeper function
            continue
        elif loop_count > 3:
            raise TakesTooLongError("Keeps going through encounter selection loop!")
        loop_count += 1


def proceed_at_bounty_complete():
    if pyautogui.locateCenterOnScreen(config.BOUNTY_COMPLETE_IMG, confidence=0.9):
        click(config.BOUNTY_COMPLETE_OK_BUTTON)
    else:
        raise ExpectedOnScreenError(f"Could not detect BOUNTY_COMPLETE_IMG")


def collect_rewards():
    """
    With keyboard input (12345).
    """
    pyautogui.press('1')
    pyautogui.press('2')
    pyautogui.press('3')
    pyautogui.press('4')
    pyautogui.press('5')


# def encounter_loop():
#     bounties_done = 0
#     while True:
#         recognize_checkpoint()
#         if not checkpoint == Checkpoint.ENCOUNTER_SELECT:
#             raise CheckpointError("Expected encounter select screen here!")
#         info(f"Bounties done: {bounties_done}. Starting bounty...")
#         encounter_selection()
#         if wait_for_yellow_played_button():
#             click(config.PLAYED_BUTTON)
#         battle_loop()
#         recognize_checkpoint()
#         if checkpoint == Checkpoint.TREASURE_SELECT:
#             treasure_select_to_encounter_select()
#         elif checkpoint == Checkpoint.REWARDS_COLLECTION:
#             collect_rewards()  # this can be done with 12345
#             click(config.REWARDS_DONE_BUTTON)
#             wait(5)
#             proceed_at_bounty_complete()
#             wait(3)
#             bounties_done += 1
#             info("DONE! WE SHOULD BE AT THE BOUNTIES SCREEN WITH FIRST SELECTED AND CHOOSE BUTTON READY TO GO.")
#             bounty_select_to_encounter_select()


def begin_countdown():
    for i in range(config.BEGIN_DELAY):
        info(f"Starting bot in {config.BEGIN_DELAY - i} seconds...")
        wait(1)


def detect_treasure():
    if pyautogui.locateCenterOnScreen(config.PICK_ONE_TREASURE_IMG, confidence=0.89):
        info(f"detected {config.PICK_ONE_TREASURE_IMG.filename} on screen")
        return True
    # elif pyautogui.locateCenterOnScreen(config.PICK_ONE_TREASURE_IMG2, confidence=0.89):
    #     info(f"detected {config.PICK_ONE_TREASURE_IMG2.filename} on screen")
    #     return True
    # elif pyautogui.locateCenterOnScreen(config.PICK_ONE_TREASURE_IMG3, confidence=0.89):
    #     info(f"detected {config.PICK_ONE_TREASURE_IMG3.filename} on screen")
    #     return True
    # elif pyautogui.locateCenterOnScreen(config.PICK_ONE_TREASURE_IMG4, confidence=0.89):
    #     info(f"detected {config.PICK_ONE_TREASURE_IMG4.filename} on screen")
    elif pyautogui.locateCenterOnScreen(config.KEEP_OR_REPLACE_TREASURE_IMG, confidence=0.89):
        info(f"detected {config.KEEP_OR_REPLACE_TREASURE_IMG.filename} on screen")
        return True


def detect_reward():
    for i in range(2):
        if pyautogui.locateCenterOnScreen(config.REWARD_IMG, confidence=0.87):
            info(f"detected {config.REWARD_IMG.filename}")
            return True
        elif pyautogui.locateCenterOnScreen(config.REWARD_IMG2, confidence=0.87):
            info(f"detected {config.REWARD_IMG2.filename}")
            return True
    # for i in range(10000):
    #     if i % 100 == 0:
    #         print(i)
    #     if not pyautogui.locateCenterOnScreen(config.REWARD_IMG, confidence=0.87):
    #         print(f"{i} NO MATCH!!!")


def recognize_checkpoint():
    global checkpoint
    if detect_reward():
        checkpoint = Checkpoint.REWARDS_COLLECTION
    elif detect(config.PICK_ONE_TREASURE_IMG):
        checkpoint = Checkpoint.TREASURE_SELECT
    elif detect(config.BOSS_INFO_IMG):
        checkpoint = Checkpoint.BOUNTY_SELECT
    elif detect(config.ENCOUNTER_TEXT_IMG):
        checkpoint = Checkpoint.ENCOUNTER_SELECT
    elif detect(config.ENCOUNTER_HEROIC_TEXT_IMG):
        checkpoint = Checkpoint.ENCOUNTER_SELECT
    else:
        checkpoint = Checkpoint.UNKNOWN
        raise CheckpointError("Was not able to recognize any of the checkpoint screens!")
    info(checkpoint)


def bounty_select_to_encounter_select():
    click(strat.bounty_selection_location)
    click(config.BOUNTY_SELECTION_CHOOSE_BUTTON)
    wait(1)
    click(config.PARTY_SELECTION_CHOOSE_BUTTON)
    wait(1)
    click(config.PARTY_LOCK_IN_BUTTON)
    wait(5)  # This is where it scrolls down the bounty map
    recognize_checkpoint()


def encounter_select_to_merc_played():
    encounter_selection()


def merc_played_to_battle():
    info("merc_played_to_battle()")
    strat.play_mercs()


def first_ability_target_enemy_minion():
    click(config.SAFE_BET_FIRST_ABILITY_LOCATION)
    click(config.SAFE_BET_ENEMY_MINION_LOCATION)


def basic_battle_loop_core():
    neeru = pyautogui.locateCenterOnScreen(config.NEERU_FIREBLADE_IMG, confidence=0.9)
    ancient = pyautogui.locateCenterOnScreen(config.CORRUPTED_ANCIENT, confidence=0.9)
    if neeru:
        target = neeru
    elif ancient:
        target = ancient
    else:
        target = config.SAFE_BET_ENEMY_MINION_LOCATION
    click(config.SAFE_BET_ALLY_MERC_LOCATION)
    for i in range(5):
        # todo: break out when green ready button shows up, after trying for a while, raise a TakesTooLongError.
        click(config.SAFE_BET_FIRST_ABILITY_LOCATION)
        click(target)
    click(config.READY_BUTTON)
    wait(15)  # combat resolving
    # todo: instead of waiting we could look for the yellow ready button showing up (or the various click to
    #  continues!!) if neither show up after a certain while, a TakesTooLongError should be raised


def battle_loop():
    global checkpoint
    battle_loop_times = 20
    # weird_situation_alternator = "yellow_button_strat"
    # no_ideal_options_counter = -1
    for i in range(battle_loop_times):
        # no_ideal_options_counter += 1
        # if no_ideal_options_counter > 3:  # failsafe for unusual combat situation
        #     if weird_situation_alternator == "yellow_button_strat":
        #         info("Something is weird! Going to click YELLOW ready button this time...")
        #         click(config.READY_BUTTON)
        #         weird_situation_alternator = "target_first_ability_strat"
        #         no_ideal_options_counter = -1
        #     elif weird_situation_alternator == "target_first_ability_strat":
        #         info("Something is weird! Trying to target an ability this time...")
        #         first_ability_target_enemy_minion()
        #         weird_situation_alternator = "yellow_button_strat"
        #         no_ideal_options_counter = -1
        #     else:
        #         raise ValueError(
        #             "weird_situation_alternator should always be one of the two possible values, "
        #             "namely: 'yellow_button_strat' or 'target_first_ability_strat'!")
        #     wait(5)  # combat actions resolving
        # if detect(config.PICK_ONE_TREASURE_IMG):
        if detect_treasure():
            info("No battle taking place (treasure). Returning from battle_loop...")
            checkpoint = Checkpoint.TREASURE_SELECT
            return
        elif detect_reward():
            info("No battle taking place (rewards). Returning from battle_loop...")
            checkpoint = Checkpoint.REWARDS_COLLECTION
            return
        info(f"battle_loop() {i + 1}/{battle_loop_times}...")
        # no_ideal_options_counter = specific_pluggable_battle_loop_core(no_ideal_options_counter)
        # no_ideal_options_counter = strat.battle_loop_core(no_ideal_options_counter)
        basic_battle_loop_core()
    raise TakesTooLongError("Should have moved on from battle phase by now!")


def specific_pluggable_battle_loop_core(no_ideal_options_counter):
    # for img in config.battle_action_imgs:
    for img in config.targeted_battle_action_imgs:
        loc = pyautogui.locateCenterOnScreen(img, confidence=0.9)
        if loc:
            no_ideal_options_counter = -1
            info(f"Detected {img.filename}! Clicking...")
            click(loc)
            if "targeted_attack" in img.filename:
                click(config.SAFE_BET_ENEMY_MINION_LOCATION)
            elif "click_to_continue" in img.filename:
                click(config.HARMLESS_CLICK_LOCATION)
                click(config.HARMLESS_CLICK_LOCATION)
            elif "green_ready_button" in img.filename:
                wait(5)  # combat actions resolving
        wait(0.5)
    return no_ideal_options_counter


def treasure_select_to_encounter_select():
    info("treasure_select_to_encounter_select()")
    click(config.TREASURE_SELECTION_CLICKING_POINT)
    click(config.TAKE_BUTTON)
    wait(3)
    recognize_checkpoint()


def rewards_collection_to_bounty_select():
    info("rewards_collection_to_bounty_select()")
    collect_rewards()
    click(config.REWARDS_DONE_BUTTON)
    wait(5)
    proceed_at_bounty_complete()
    wait(3)


def bounty_select_to_bounty_select_loop():
    number_of_bounties_cleared = 0
    while True:
        recognize_checkpoint()
        if checkpoint == Checkpoint.BOUNTY_SELECT:
            info(f"Number of bounties cleared so far: {number_of_bounties_cleared}. Starting bounty...")
            info(f"###################################################################################")
            bounty_select_to_encounter_select()
        bounty_cleared = False
        while not bounty_cleared:
            encounter_select_to_merc_played()
            merc_played_to_battle()
            battle_loop()
            if checkpoint == Checkpoint.TREASURE_SELECT:
                treasure_select_to_encounter_select()
            elif checkpoint == Checkpoint.REWARDS_COLLECTION:
                bounty_cleared = True
                number_of_bounties_cleared += 1
                rewards_collection_to_bounty_select()
            else:
                raise CheckpointError(f"Expected either TREASURE_SELECT or REWARDS_COLLECTION but it is {checkpoint}")


def influx():
    recognize_checkpoint()
    if checkpoint == Checkpoint.BOUNTY_SELECT:
        bounty_select_to_bounty_select_loop()
    elif checkpoint == Checkpoint.ENCOUNTER_SELECT:
        bounty_select_to_bounty_select_loop()  # same but skips a bit based on checkpoint todo: better way
    else:
        raise CheckpointError(f"{checkpoint} not supported for influx yet!")


def activate_logging():
    def log_exceptions(exc_type, exc_value, exc_traceback):
        logging.error("########## EXCEPTION ##########", exc_info=(exc_type, exc_value, exc_traceback))
        sys.__excepthook__(exc_type, exc_value, exc_traceback)  # calls default excepthook

    file_handler = logging.FileHandler(filename='hs_merc_bot.log')
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s', handlers=handlers)
    sys.excepthook = log_exceptions
    info("########## START ##########")


def test():
    # raise ExpectedOnScreenError("I was expecting something else on the screen right now!")
    # detect_treasure()
    # detect_reward()
    if detect_treasure():
        print(True)
    else:
        print(False)


def main():
    activate_logging()
    begin_countdown()
    # test()
    influx()


if __name__ == "__main__":
    main()
