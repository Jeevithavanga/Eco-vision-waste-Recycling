import unittest

from disposal.disposal_rules import get_disposal_recommendation

class TestDisposalRules(unittest.TestCase):

    def test_battery(self):
        result = get_disposal_recommendation("Battery")
        self.assertTrue(result["success"])
        self.assertFalse(result["ordinary_bin"])
        self.assertTrue(result["special_facility_required"])

    def test_plastic(self):
        result = get_disposal_recommendation("Plastic Bottle")
        self.assertTrue(result["success"])
        self.assertEqual(result["category"], "Plastic")

    def test_e_waste(self):
        result = get_disposal_recommendation("E-Waste")
        self.assertTrue(result["success"])
        self.assertEqual(result["category"], "Electronic Waste")

    def test_unknown_category(self):
        result = get_disposal_recommendation("Unknown Item")
        self.assertFalse(result["success"])

    def test_empty_category(self):
        result = get_disposal_recommendation("")
        self.assertFalse(result["success"])

    def test_missing_category(self):
        result = get_disposal_recommendation(None)
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()