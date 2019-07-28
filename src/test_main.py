import pytest
from tools import simulate
import datetime

from simulator_fixture import simulator

@pytest.mark.parametrize("params", [{}])
@simulate
def test_main(simulator):
    # test root has label with current time
    _clock_test(simulator)
    _check_chronometer_label(simulator)
    # assert button quantity
    simulator.assert_count("//RootWidget//Button", 2)
    # assert buttons label in main screen
    simulator.assert_text("//RootWidget//Button[1]", "Start")
    simulator.assert_text("//RootWidget//Button[2]", "Reset")
    # test the start and stop of the chronometer
    simulator.tap("//RootWidget//Button[1]")
    simulator.assert_text("//RootWidget//Button[1]", "Stop")
    simulator.tap("//RootWidget//Button[1]")
    simulator.assert_text("//RootWidget//Button[1]", "Start")
    _check_chronometer_label(simulator, 1)
    simulator.tap("//RootWidget//Button[2]")
    _check_chronometer_label(simulator)

def _clock_test(simulator):
    """ Check the clock. This validation should be called at least twice
        to make sure the clock works fine"""
    # the tester lasts 2 seconds to validate so the time has to be checked for 2 seconds after
    eval_time = datetime.datetime.now() + datetime.timedelta(seconds=2)
    eval_text = '{}..'.format(eval_time.strftime('%H:%M:'))
    simulator.assert_attr_regexp("//RootWidget//ClockLabel", 'text', eval_text)

def _check_chronometer_label(simulator, seconds=0):
    """ Checks the label of the chronometer"""
    text_to_check = "[b]00:{:02d}.[size=40]00[/size][/b]".format(seconds)
    simulator.assert_text("//RootWidget//TimerLabel", text_to_check)
