"""
hs_merc_bot.py
author: roelantvanderhilst@gmail.com
Before you start the script, make sure starting conditions are correct.
"""
import pyautogui
import config
import enum
import card_in_hand_positions as hand  # todo: get rid of this dependency
from merc_lib import click, wait
from xyrella_blademaster_rokara_strategy import XyrellaBlademasterRokaraStrategy

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25
strat = XyrellaBlademasterRokaraStrategy()


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


checkpoint = Checkpoint.UNKNOWN
direction_switch = "left_to_right"


def detect_played_button():
    times_to_try = 60
    for i in range(times_to_try):
        if i % 5 == 0:
            print(f"Trying to detect Played button ({i + 1}/{times_to_try})...")
        played_button_region_screenshot = pyautogui.screenshot(region=config.PLAYED_BUTTON_REGION)
        if pyautogui.locate(played_button_region_screenshot, config.PLAYED_BUTTON_IMG, confidence=0.9):
            return True
        elif i < times_to_try - 1:
            wait(1)
    raise ExpectedOnScreenError(f"Could not detect Played button after {times_to_try} tries!")


def detect(image):
    location = pyautogui.locateCenterOnScreen(image, confidence=0.9)
    if location:
        print(f"Detected {image.filename} on screen.")
        return location


def go_battle():
    global checkpoint
    checkpoint = Checkpoint.TO_BATTLE
    print("go_battle()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(10)
    detect_played_button()


def go_task():
    print("go_task()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(0.5)
    click(config.THIRD_VISITOR_LOCATION)
    click(config.CHOOSE_VISITOR_BUTTON)
    wait(0.5)
    click(config.CHOOSE_VISITOR_BUTTON)
    wait(3)


def go_res():
    print("go_res()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(5)


def go_warp():
    print("go_warp()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(5)


def go_boon():
    print("go_boon()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(0.5)
    click(config.TREASURE_SELECTION_CLICKING_POINT)
    wait(3)


def go_pick_up():
    print("go_pick_up()")
    print("WARNING: THIS IS RISKY! WE MIGHT DIE WITH THIS!")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(0.5)
    click(config.TREASURE_SELECTION_CLICKING_POINT)
    wait(5)


def go_sabotage():
    print("go_sabotage()")
    click(config.ENCOUNTER_CONFORMATION_BUTTON_LOCATION)
    wait(10)  # because it might take long when the map is really big


def try_for(image):
    global direction_switch
    x_coords = None
    if direction_switch == "left_to_right":
        x_coords = config.TRY_ENCOUNTER_X_COORDS
        direction_switch = "right_to_left"
    elif direction_switch == "right_to_left":
        x_coords = config.TRY_ENCOUNTER_X_COORDS[::-1]
        direction_switch = "left_to_right"
    for x_coord in x_coords:
        location = (x_coord, 500)
        click(location)
        if detect(image):
            return True
    return False


def encounter_selection():
    print("encounter_selection()")
    loop_count = 0
    while checkpoint == Checkpoint.ENCOUNTER_SELECT:
        loop_count += 1
        if loop_count > 5:
            raise TakesTooLongError("Keeps going through encounter selection loop!")
        if detect(config.ENCOUNTER_SELECTION_VISIT_BUTTON_IMG):
            if detect(config.TASK_CUE_IMG):
                go_task()
                continue
            elif detect(config.RES_CUE_IMG):
                go_res()
                continue
            elif detect(config.SABOTAGE_CUE_IMG):
                go_sabotage()
                continue
            else:
                raise ExpectedOnScreenError("Visit button highlighted but no TASK, RES or SABOTAGE cue!")
        elif detect(config.ENCOUNTER_SELECTION_PLAY_BUTTON_IMG):
            go_battle()
            continue
        elif detect(config.ENCOUNTER_SELECTION_REVEAL_BUTTON_IMG):
            go_boon()
            continue
        elif detect(config.ENCOUNTER_SELECTION_WARP_BUTTON_IMG):
            go_warp()
            continue
        elif detect(config.ENCOUNTER_SELECTION_PICK_UP_BUTTON_IMG):
            go_pick_up()
            continue
        elif try_for(config.ENCOUNTER_SELECTION_VISIT_BUTTON_IMG):
            if detect(config.TASK_CUE_IMG):
                go_task()
                continue
        if try_for(config.ENCOUNTER_SELECTION_PLAY_BUTTON_IMG):
            go_battle()
            continue
        elif try_for(config.ENCOUNTER_SELECTION_VISIT_BUTTON_IMG):
            if detect(config.RES_CUE_IMG):
                go_res()
                continue
            elif detect(config.SABOTAGE_CUE_IMG):
                go_sabotage()
                continue
            else:
                raise ExpectedOnScreenError("Visit button highlighted but no TASK, RES or SABOTAGE cue!")
        elif try_for(config.ENCOUNTER_SELECTION_WARP_BUTTON_IMG):
            go_warp()
            continue
        elif try_for(config.ENCOUNTER_SELECTION_REVEAL_BUTTON_IMG):
            go_boon()
            continue
        elif try_for(config.ENCOUNTER_SELECTION_PICK_UP_BUTTON_IMG):
            go_pick_up()
            continue


def proceed_at_bounty_complete():
    if pyautogui.locateCenterOnScreen(config.BOUNTY_COMPLETE_IMG, confidence=0.9):
        click(config.BOUNTY_COMPLETE_OK_BUTTON)
    else:
        raise ExpectedOnScreenError(f"Could not detect BOUNTY_COMPLETE_IMG")


def click_rewards():  # better done with collect_rewards? (12345 keyboard input)
    for location in config.reward_locations:
        click(location)


def collect_rewards():
    """
    With keyboard input (12345).
    """
    pyautogui.press('1')
    pyautogui.press('2')
    pyautogui.press('3')
    pyautogui.press('4')
    pyautogui.press('5')


def encounter_loop():
    bounties_done = 0
    while True:
        recognize_checkpoint()
        if not checkpoint == Checkpoint.ENCOUNTER_SELECT:
            raise CheckpointError("Expected encounter select screen here!")
        print(f"Bounties done: {bounties_done}. Starting bounty...")
        encounter_selection()
        if detect_played_button():
            click(config.PLAYED_BUTTON)
        battle_loop()
        recognize_checkpoint()
        if checkpoint == Checkpoint.TREASURE_SELECT:
            treasure_select_to_encounter_select()
        elif checkpoint == Checkpoint.REWARDS_COLLECTION:
            click_rewards()  # this can be done with 12345
            click(config.REWARDS_DONE_BUTTON)
            wait(5)
            proceed_at_bounty_complete()
            wait(3)
            bounties_done += 1
            print("DONE! WE SHOULD BE AT THE BOUNTIES SCREEN WITH FIRST SELECTED AND CHOOSE BUTTON READY TO GO.")
            bounty_select_to_encounter_select()


def begin_countdown():
    for i in range(config.BEGIN_DELAY):
        print(f"Starting bot in {config.BEGIN_DELAY - i} seconds...")
        wait(1)


def detect_reward():
    for i in range(2):
        if pyautogui.locateCenterOnScreen(config.REWARD_IMG, confidence=0.87):
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
    print(checkpoint)


def bounty_select_to_encounter_select():
    click(config.BOUNTY_SELECTION_CHOOSE_BUTTON)
    wait(1)
    click(config.PARTY_SELECTION_CHOOSE_BUTTON)
    wait(1)
    click(config.PARTY_LOCK_IN_BUTTON)
    wait(5)  # This is where it scrolls down the bounty map
    recognize_checkpoint()


def encounter_select_to_merc_played():
    encounter_selection()


def cariel_xyrella_blademaster_456_play_mercs():
    # # this is where you play the 2, 4 and 6 card positions in case of farm train team
    # # 1, 4, 6 with xyrella instead of rokara
    # # click(config.CARD_2_OF_6)
    # click(config.CARD_1_OF_6)
    # click(config.RIGHT_SIDE_OF_BOARD)
    # click(config.CARD_3_OF_5)
    # click(config.RIGHT_SIDE_OF_BOARD)
    # click(config.CARD_4_OF_4)
    # click(config.RIGHT_SIDE_OF_BOARD)
    click(hand.CARD_4_OF_6)
    click(config.RIGHT_SIDE_OF_BOARD)
    click(hand.CARD_4_OF_5)
    click(config.RIGHT_SIDE_OF_BOARD)
    click(hand.CARD_4_OF_4)
    click(config.RIGHT_SIDE_OF_BOARD)
    click(config.READY_BUTTON)
    wait(5)


def merc_played_to_battle():
    print("merc_played_to_battle()")
    strat.play_mercs()


def first_ability_target_enemy_minion():
    click(config.SAFE_BET_FIRST_ABILITY_LOCATION)
    click(config.SAFE_BET_ENEMY_MINION_LOCATION)


def battle_loop():
    global checkpoint
    battle_loop_times = 60
    weird_situation_resolution_strategy_alternation = "yellow_button_strat"
    no_ideal_options_counter = -1
    for i in range(battle_loop_times):
        no_ideal_options_counter += 1
        if no_ideal_options_counter > 5:  # failsafe for unusual combat situation
            if weird_situation_resolution_strategy_alternation == "yellow_button_strat":
                print("Something is weird! Going to click YELLOW ready button this time...")
                click(config.READY_BUTTON)
                weird_situation_resolution_strategy_alternation = "target_first_ability_strat"
                no_ideal_options_counter = -1
            elif weird_situation_resolution_strategy_alternation == "target_first_ability_strat":
                print("Something is weird! Trying to target an ability this time...")
                first_ability_target_enemy_minion()
                weird_situation_resolution_strategy_alternation = "yellow_button_strat"
                no_ideal_options_counter = -1
            else:
                raise ValueError(
                    "weird_situation_resolution_strategy_alternation should always be one of the two possible values, "
                    "namely: 'yellow_button_strat' or 'target_first_ability_strat'!")
            wait(5)  # combat actions resolving
        if detect(config.PICK_ONE_TREASURE_IMG):
            print("No battle taking place (treasure). Returning from battle_loop...")
            checkpoint = Checkpoint.TREASURE_SELECT
            return
        elif detect_reward():
            print("No battle taking place (rewards). Returning from battle_loop...")
            checkpoint = Checkpoint.REWARDS_COLLECTION
            return
        print(f"battle_loop() {i + 1}/{battle_loop_times}...")
        # no_ideal_options_counter = specific_pluggable_battle_loop_core(no_ideal_options_counter)
        no_ideal_options_counter = strat.battle_loop_core(no_ideal_options_counter)
    raise TakesTooLongError("Should have moved on from battle phase by now!")


def specific_pluggable_battle_loop_core(no_ideal_options_counter):
    # for img in config.battle_action_imgs:
    for img in config.targeted_battle_action_imgs:
        loc = pyautogui.locateCenterOnScreen(img, confidence=0.9)
        if loc:
            no_ideal_options_counter = -1
            print(f"Detected {img.filename}! Clicking...")
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
    print("treasure_select_to_encounter_select()")
    click(config.TREASURE_SELECTION_CLICKING_POINT)
    click(config.TAKE_BUTTON)
    wait(3)
    recognize_checkpoint()


def rewards_collection_to_bounty_select():
    print("rewards_collection_to_bounty_select()")
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
            print(f"Number of bounties cleared so far: {number_of_bounties_cleared}. Starting bounty...")
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


def test():
    battle_loop()


def main():
    begin_countdown()
    # test()
    influx()
    # screenshot = pyautogui.screenshot("images/encounter_text.png", region=config.ENCOUNTER_TEXT_REGION)


if __name__ == "__main__":
    main()
