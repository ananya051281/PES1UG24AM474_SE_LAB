import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# Membership plan branches
def test_unknown_plan():
    with pytest.raises(ValueError):
        membership_cost("weekly", 25, False, False)


def test_age_below_14():
    with pytest.raises(ValueError):
        membership_cost("monthly", 13, False, False)


def test_senior_discount():
    assert membership_cost("monthly", 60, False, False) == 1125


def test_student_discount():
    assert membership_cost("monthly", 20, True, False) == 1350


def test_regular_non_student():
    assert membership_cost("monthly", 30, False, False) == 1500


def test_trainer_monthly():
    assert membership_cost("monthly", 30, False, True) == 3500


def test_trainer_yearly():
    assert membership_cost("yearly", 30, False, True) == 13500


def test_senior_with_trainer():
    assert membership_cost("yearly", 65, False, True) == 10500


# Gym entry branches
def test_inactive_plan():
    assert can_enter(10, False, False, "M") is False


def test_before_opening():
    assert can_enter(4, True, False, "M") is False


def test_opening_boundary():
    assert can_enter(5, True, False, "M") is True


def test_closing_boundary():
    assert can_enter(22, True, False, "M") is True


def test_after_closing():
    assert can_enter(23, True, False, "M") is False


def test_normal_slot():
    assert can_enter(10, True, False, "M") is True


def test_women_slot_female():
    assert can_enter(10, True, True, "F") is True


def test_women_slot_male():
    assert can_enter(10, True, True, "M") is False


# BMI decision branches
def test_invalid_height():
    with pytest.raises(ValueError):
        bmi_category(70, 0)


def test_underweight():
    assert bmi_category(45, 1.70) == "underweight"


def test_normal_bmi():
    assert bmi_category(65, 1.70) == "normal"


def test_overweight_bmi():
    assert bmi_category(80, 1.70) == "overweight"


def test_obese_bmi():
    assert bmi_category(100, 1.70) == "obese"