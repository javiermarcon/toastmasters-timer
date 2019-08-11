import unittest
from telenium.tests import TeleniumTestCase


class TestTestCase(TeleniumTestCase):
    cmd_entrypoint = [u'/home/javier/proyectos/toastmaster/kivy-timer/src/main.py']

    def test_new_test(self):
        self.cli.wait_click('//RootWidget//Button[@text~="Start"]', timeout=5)
    #class UITestCase(TeleniumTestCase):
    #cmd_entrypoint = ["main.py"]

    #def test_guiclock(self):
    #    self.assertExists("//RootWidget//Button[@text~=\"Start\"]", timeout=2)
    #    self.cli.wait_click("//RootWidget//Button[@text=\"Start\"]", timeout=2)
    #    #self.assertNotExists("//Label[@text~=\"Reset\"]", timeout=2)



if __name__ == '__main__':
    unittest.main()