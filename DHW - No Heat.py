"""
This Script tests the "Outdoor Temperature" disabling condition for the Sources in PCM5
"""
import sys
# hari pr
from configs.Config import *
from libs_EM.EMClassManager import EMClassManager
import random

em = EMClassManager(em_config)

# TEST
Test_title = 'DHW - No Heat'     # HERE THE NAME OF THE CASE
Test_case = "C272207"      # HERE THE ID OF THE CASE
Script_Ver = "1"
Framework_Ver = "1.6.0"
Class_Ver = "1.4.0"

Link_TC_LL = "https://comodel.mtsintra.network/testrail/index.php?/cases/view/272207"       # HERE THE LINK OF THE TC LL

em.add_Comment(Test_title)
em.add_Comment(f"TestCase: {Test_case} - Script Version: {Script_Ver}")

print("Start test")
em.test_passed = True

# Variables and Constants

SOURCE = "WHB"
CH_DHW_1 = "DHW"                    # STEP 1: Can be "CH" if we want disable the source for CH or "DHW" if we want disable the source for DHW



# START - VARIABLES
MACROSTATE_ST = 4                   # MacroState of Start
CYCLE_ST = 16                       # Cycle of Start
STATUS_ST = 44                       # Starting HEM - Status

# STEP 1
MACROSTATE_1 = 9                   # MacroState of Step 1
CYCLE_1 = 10                       # Cycle of Step 1
STATUS_1 = 210                       # HEM - Status of Step 1

# STEP 2
MACROSTATE_2 = 4                   # MacroState of Step 2
CYCLE_2 = 16                       # Cycle of Step 2
STATUS_2 = 41                       # HEM - Status of Step 2


# Preconditions

em.hp_Enabling()
em.aux_Enabling()

if SOURCE == "BK":
    em.bk_Enabling()
elif SOURCE == "WHB":
    em.whb_Enabling()

# em.tdm_Enabling()

# STARTUP

em.state_Transition(0, 45, 190, reset=True)


# EXPECTED RESULT STARTUP

if em.read_DGTO("HEM - Status") == 190 and em.check_Loads():

    em.add_Comment("STARTUP OK", background_color="SUCCESS")

    # PRECONDITION AFTER STARTUP

    em.state_Transition(MACROSTATE_ST, CYCLE_ST, STATUS_ST, reset=True)

    em.wait_Time(2)

    # EXPECTED RESULT PRECONDITION

    hem_status_st = em.read_DGTO("HEM - Status")

    if hem_status_st == STATUS_ST and em.check_Loads():

        em.add_Comment(f"Expected Result PRECONDITION OK", background_color="SUCCESS")

    else:
        em.add_Comment(f"Expected Result PRECONDITION NOT OK", background_color="ERROR")
        em.test_passed = False
        # close communication
        print("Test passed" if em.test_passed else "Test failed")
        del em
        sys.exit()

    # STEP 1

    if SOURCE == "BK" and CH_DHW_1 == "DHW":
        em.bk_Disabling(9)
        em.wait_Time(2)
    elif SOURCE == "BK" and CH_DHW_1 == "CH":
        em.bk_Disabling(8)
        em.wait_Time(2)
    elif SOURCE == "WHB" and CH_DHW_1 == "DHW":
        em.whb_Disabling(7)
        em.wait_Time(2)
    elif SOURCE == "WHB" and CH_DHW_1 == "CH":
        em.whb_Disabling(1)
        em.wait_Time(2)

    em.hp_Disabling(2)
    em.aux_Disabling(3)
    # EXPECTED RESULT 1

    hem_status_1 = em.read_DGTO("HEM - Status")
    current_cycle_1 = em.read_DGTO("ENERGY_MANAGER_CURRENT_CYCLE")
    macro_1 = em.read_DGTO("EM - MacroState")

    if hem_status_1 == STATUS_1 and current_cycle_1 == CYCLE_1 and macro_1 == MACROSTATE_1 and em.check_Loads():
        em.add_Comment(f"Expected Result Step 1 OK", background_color="SUCCESS")

    else:
        em.add_Comment(f"Expected Result Step 1 NOT OK", background_color="ERROR")
        em.test_passed = False
        # close communication
        print("Test passed" if em.test_passed else "Test failed")
        del em
        sys.exit()

    # STEP 2
    em.hp_Enabling()

    # EXPECTED RESULT 2

    hem_status_2 = em.read_DGTO("HEM - Status")
    current_cycle_2 = em.read_DGTO("ENERGY_MANAGER_CURRENT_CYCLE")
    macro_2 = em.read_DGTO("EM - MacroState")

    if hem_status_2 == STATUS_2 and current_cycle_2 == CYCLE_2 and macro_2 == MACROSTATE_2 and em.check_Loads(whb_available=False, aux_available=False):
        em.add_Comment(f"Expected Result Step 2 OK", background_color="SUCCESS")

    else:
        em.add_Comment(f"Expected Result Step 2 NOT OK", background_color="ERROR")
        em.test_passed = False
        # close communication
        print("Test passed" if em.test_passed else "Test failed")
        del em
        sys.exit()


else:
    em.add_Comment("STARTUP NOT OK", background_color="ERROR")
    em.test_passed = False

print("Test passed" if em.test_passed else "Test failed")

# close communication
del em