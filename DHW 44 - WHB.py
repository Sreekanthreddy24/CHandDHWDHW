"""
This Script tests the "Outdoor Temperature" disabling condition for the Sources in PCM5
"""
import sys

from configs.Config import *
from libs_EM.EMClassManager import EMClassManager
import random

em = EMClassManager(em_config)

# TEST
Test_title = 'DHW 44 - WHB'     # HERE THE NAME OF THE CASE
Test_case = "C272208"      # HERE THE ID OF THE CASE
Script_Ver = "1"
Framework_Ver = "1.6.0"
Class_Ver = "1.4.0"

Link_TC_LL = "https://comodel.mtsintra.network/testrail/index.php?/cases/view/272208"       # HERE THE LINK OF THE TC LL

em.add_Comment(Test_title)
em.add_Comment(f"TestCase: {Test_case} - Script Version: {Script_Ver}")
# dsfhj
print("Start test")
em.test_passed = True

# Variables and Constants

SOURCE = "WHB"
CH_DHW_1 = "CH"                    # STEP 1: Can be "CH" if we want disable the source for CH or "DHW" if we want disable the source for DHW
CH_DHW_3 = "DHW"                     # STEP 3: Can be "CH" if we want disable the source for CH or "DHW" if we want disable the source for DHW


# START - VARIABLES
MACROSTATE_ST = 4                   # MacroState of Start
CYCLE_ST = 16                       # Cycle of Start
STATUS_ST = 44                       # Starting HEM - Status

# STEP 1
MACROSTATE_1 = 4                   # MacroState of Step 1
CYCLE_1 = 16                       # Cycle of Step 1
STATUS_1 = 44                       # HEM - Status of Step 1

# STEP 2
MACROSTATE_2 = 4                   # MacroState of Step 2
CYCLE_2 = 16                       # Cycle of Step 2
STATUS_2 = 44                       # HEM - Status of Step 2

# STEP 3
MACROSTATE_3 = 4                   # MacroState of Step 3
CYCLE_3 = 16                       # Cycle of Step 3
STATUS_3 = 44                       # HEM - Status of Step 3

# STEP 4
MACROSTATE_4 = 4                   # MacroState of Step 4
CYCLE_4 = 16                       # Cycle of Step 4
STATUS_4 = 44                       # HEM - Status of Step 4

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

    if SOURCE == "BK":
        em.bk_Enabling()
        em.wait_Time(2)
    elif SOURCE == "WHB":
        em.whb_Enabling()
        em.wait_Time(2)

    # EXPECTED RESULT 2

    hem_status_2 = em.read_DGTO("HEM - Status")
    current_cycle_2 = em.read_DGTO("ENERGY_MANAGER_CURRENT_CYCLE")
    macro_2 = em.read_DGTO("EM - MacroState")

    if hem_status_2 == STATUS_2 and current_cycle_2 == CYCLE_2 and macro_2 == MACROSTATE_2 and em.check_Loads():
        em.add_Comment(f"Expected Result Step 2 OK", background_color="SUCCESS")

    else:
        em.add_Comment(f"Expected Result Step 2 NOT OK", background_color="ERROR")
        em.test_passed = False
        # close communication
        print("Test passed" if em.test_passed else "Test failed")
        del em
        sys.exit()

    # STEP 3

    if SOURCE == "BK" and CH_DHW_3 == "DHW":
        em.bk_Disabling(9)
        em.wait_Time(2)
    elif SOURCE == "BK" and CH_DHW_3 == "CH":
        em.bk_Disabling(8)
        em.wait_Time(2)
    elif SOURCE == "WHB" and CH_DHW_3 == "DHW":
        em.whb_Disabling(7)
        em.wait_Time(2)
    elif SOURCE == "WHB" and CH_DHW_3 == "CH":
        em.whb_Disabling(1)
        em.wait_Time(2)

    # EXPECTED RESULT 3

    hem_status_3 = em.read_DGTO("HEM - Status")
    current_cycle_3 = em.read_DGTO("ENERGY_MANAGER_CURRENT_CYCLE")
    macro_3 = em.read_DGTO("EM - MacroState")

    if hem_status_3 == STATUS_3 and current_cycle_3 == CYCLE_3 and macro_3 == MACROSTATE_3:
        status_transition = True
    else:
        status_transition = False

    if status_transition and SOURCE == "BK" and em.check_Loads(bk_available=False):
        em.add_Comment(f"Expected Result Step 3 OK", background_color="SUCCESS")

    elif status_transition and SOURCE == "WHB" and em.check_Loads(whb_available=False):
        em.add_Comment(f"Expected Result Step 3 OK", background_color="SUCCESS")

    else:
        em.add_Comment(f"Expected Result Step 3 NOT OK", background_color="ERROR")
        em.test_passed = False
        # close communication
        print("Test passed" if em.test_passed else "Test failed")
        del em
        sys.exit()

    # STEP 4

    if SOURCE == "BK":
        em.bk_Enabling()
        em.wait_Time(2)
    elif SOURCE == "WHB":
        em.whb_Enabling()
        em.wait_Time(2)

    # EXPECTED RESULT 4

    hem_status_4 = em.read_DGTO("HEM - Status")
    current_cycle_4 = em.read_DGTO("ENERGY_MANAGER_CURRENT_CYCLE")
    macro_4 = em.read_DGTO("EM - MacroState")

    if hem_status_4 == STATUS_4 and current_cycle_4 == CYCLE_4 and macro_4 == MACROSTATE_4 and em.check_Loads():
        em.add_Comment(f"Expected Result Step 4 OK", background_color="SUCCESS")

    else:
        em.add_Comment(f"Expected Result Step 4 NOT OK", background_color="ERROR")
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