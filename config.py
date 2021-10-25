from PIL import Image

BEGIN_DELAY = 5

NUMBER_OF_BATTLES = 4  # 4 for the most basic bounty (barrens_one)
BOUNTY_SELECTION_CHOOSE_BUTTON = (1500, 850)
PARTY_SELECTION_CHOOSE_BUTTON = (1400, 900)
PARTY_LOCK_IN_BUTTON = (840, 625)
ENCOUNTER_SELECTION_PLAY_BUTTON = (1525, 840)
encounter_locations = ((625, 494), (888, 495), (526, 519), (760, 516), (1033, 522))
TRY_ENCOUNTER_X_COORDS = (375, 450, 525, 600, 675, 750, 825, 900, 975, 1050, 1125)
reward_locations = ((1030, 316), (1349, 796), (704, 764), (764, 309), (1334, 419), (1204, 883), (636, 750))

RIGHT_SIDE_OF_BOARD = (1268, 624)
FIRST_VISITOR_LOCATION = (630, 421)
SECOND_VISITOR_LOCATION = (942, 430)
THIRD_VISITOR_LOCATION = (1244, 434)
CHOOSE_VISITOR_BUTTON = (935, 737)
HARMLESS_CLICK_LOCATION = (915, 901)
SAFE_BET_ENEMY_MINION_LOCATION = (939, 296)
SAFE_BET_FIRST_ABILITY_LOCATION = (829, 484)
SAFE_BET_ALLY_MERC_LOCATION = (914, 713)

PLAYED_BUTTON_REGION = (1470, 450, 190, 90)
PLAYED_BUTTON = (1565, 495)
READY_BUTTON_REGION = (1507, 468, 128, 42)
READY_BUTTON = (1571, 489)
CLICK_TO_CONTINUE_REGION = (806, 1016, 309, 28)
CLICK_TO_CONTINUE = (960, 1030)
PICK_ONE_TREASURE_REGION = (990, 194, 290, 18)
TREASURE_SELECTION_CLICKING_POINT = (1105, 457)
ENCOUNTER_CONFORMATION_BUTTON_LOCATION = (1529, 838)
ENCOUNTER_SELECTION_PLAY_BUTTON_REGION = (1469, 786, 125, 110)
TAKE_BUTTON = (1142, 861)
REWARDS_DONE_BUTTON = (998, 615)
BOUNTY_COMPLETE_REGION = (800, 81, 300, 50)
BOUNTY_COMPLETE_OK_BUTTON = (956, 879)
REWARD_REGION = (750, 305, 33, 29)
BOSS_INFO_REGION = (1442, 12, 120, 26)
ENCOUNTER_TEXT_REGION = (1454, 15, 137, 21)

FELWOOD_BOUNTY_5 = (813, 683)

PLAYED_BUTTON_IMG = Image.open("images/played_button.png")
ARCANE_EXPLOSION_IMG = Image.open("images/arcane_explosion.png")
ARCANE_SALVO_IMG = Image.open("images/arcane_salvo.png")
FLURRY_IMG = Image.open("images/flurry.png")
CARIEL_TARGETED_ATTACK = Image.open("images/cariel_targeted_attack.png")
XYRELLA_TARGETED_ATTACK = Image.open("images/xyrella_targeted_attack.png")
BLADEMASTER_TARGETED_ATTACK = Image.open("images/blademaster_targeted_attack.png")
ROKARA_TARGETED_ATTACK = Image.open("images/rokara_targeted_attack.png")
GREEN_READY_BUTTON_IMG = Image.open("images/green_ready_button.png")
CLICK_TO_CONTINUE_IMG = Image.open("images/click_to_continue.png")
CLICK_TO_CONTINUE_IMG2 = Image.open("images/click_to_continue2.png")
CLICK_TO_CONTINUE_IMG3 = Image.open("images/click_to_continue3.png")

battle_action_imgs = [
    ARCANE_EXPLOSION_IMG,
    FLURRY_IMG,
    ARCANE_SALVO_IMG,
    CLICK_TO_CONTINUE_IMG,
    GREEN_READY_BUTTON_IMG,  # best order for farm train
    CLICK_TO_CONTINUE_IMG2,
    CLICK_TO_CONTINUE_IMG3,
]

targeted_battle_action_imgs = [
    CARIEL_TARGETED_ATTACK,
    XYRELLA_TARGETED_ATTACK,
    BLADEMASTER_TARGETED_ATTACK,
    CLICK_TO_CONTINUE_IMG,
    GREEN_READY_BUTTON_IMG,  # best order?
    CLICK_TO_CONTINUE_IMG2,
    CLICK_TO_CONTINUE_IMG3,
]

ENCOUNTER_SELECTION_PLAY_BUTTON_IMG = Image.open("images/encounter_selection_play_button.png")
ENCOUNTER_SELECTION_WARP_BUTTON_IMG = Image.open("images/encounter_selection_warp_button.png")
ENCOUNTER_SELECTION_VISIT_BUTTON_IMG = Image.open("images/encounter_selection_visit_button.png")
ENCOUNTER_SELECTION_REVEAL_BUTTON_IMG = Image.open("images/encounter_selection_reveal_button.png")
ENCOUNTER_SELECTION_PICK_UP_BUTTON_IMG = Image.open("images/encounter_selection_pick_up_button.png")

BOUNTY_COMPLETE_IMG = Image.open("images/bounty_complete.png")
REWARD_IMG = Image.open("images/reward.png")
REWARD_IMG2 = Image.open("images/reward2.png")
PICK_ONE_TREASURE_IMG = Image.open("images/pick_one_treasure.png")
PICK_ONE_TREASURE_IMG2 = Image.open("images/pick_one_treasure2.png")
PICK_ONE_TREASURE_IMG3 = Image.open("images/pick_one_treasure3.png")
PICK_ONE_TREASURE_IMG4 = Image.open("images/pick_one_treasure4.png")
KEEP_OR_REPLACE_TREASURE_IMG = Image.open("images/keep_or_replace_treasure.png")
BOSS_INFO_IMG = Image.open("images/boss_info.png")
ENCOUNTER_TEXT_IMG = Image.open("images/encounter_text.png")
ENCOUNTER_HEROIC_TEXT_IMG = Image.open("images/encounter_heroic_text.png")
SPUD_TEXT_IMG = Image.open("images/spud_text.png")
RES_CUE_IMG = Image.open("images/res_cue.png")
TASK_CUE_IMG = Image.open("images/task_cue.png")
SABOTAGE_CUE_IMG = Image.open("images/sabotage_cue.png")
NEERU_FIREBLADE_IMG = Image.open("images/neeru_fireblade.png")
CORRUPTED_ANCIENT = Image.open("images/corrupted_ancient.png")
