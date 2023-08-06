import unittest

from phases.commands.Base import Base


class TestRun(unittest.TestCase):
    projectFolder = "tests/data-gen"
    configFile = "tests/data/min.yaml"
    c2 = "tests/data/c2.yaml"

    def testLoadConfig(self):
        base = Base({})
        fullConfig = base.loadConfig(self.configFile, root=True)
        projectConfig = fullConfig["config"]
        assert projectConfig["before"] == "before"
        assert projectConfig["test"] == "main"
        assert projectConfig["after"] == "after"
        assert projectConfig["overwrite"] == "after"
        assert projectConfig["overwriteMain"] == "main"

        assert projectConfig["beforeF"] == "before"
        assert projectConfig["afterF"] == "after"
        assert projectConfig["overwriteF"] == "after"
        assert projectConfig["overwriteMainF"] == "main"
