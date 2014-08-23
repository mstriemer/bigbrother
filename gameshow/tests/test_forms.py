import unittest

from gameshow.forms import TeamForm


class TestTeamForm(unittest.TestCase):
    def test_blank_name_is_allowed(self):
        form = TeamForm({'name': ''})
        assert form.is_valid
