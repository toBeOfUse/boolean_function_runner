import logging
from boolean import Expression, TruthTable

if __name__ == "__main__":
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    Expression.log.addHandler(ch)
    simple_and = Expression("xy")
    print()
    simple_or = Expression("x+y")
    print()
    passthrough = Expression("F")
    print()
    assert passthrough.evaluate({"F": True})
    assert not passthrough.evaluate({"F": False})
    assert not simple_and.evaluate({"x": True, "y": False})
    assert simple_and.evaluate({"x": True, "y": True})
    assert simple_or.evaluate({"x": False, "y": True})
    assert not simple_or.evaluate({"x": False, "y": False})
    print()
    and_and_or = Expression("AB+BC")
    assert not and_and_or.evaluate({"A": False,"B": True, "C": False})
    assert and_and_or.evaluate({"A": True,"B": True, "C": False})
    assert and_and_or.evaluate({"A": False,"B": True, "C": True})
    print()
    print("Expression working 👍")
    
    Expression.log.removeHandler(ch)

    ab_plus_cd = Expression("ab+cd")
    ab_plus_cd_table = TruthTable(ab_plus_cd)
    print()
    print("truth table for ab+cd:")
    print(ab_plus_cd_table)
    for state, result in ab_plus_cd_table.states.items():
        if state[0:2] == "11" or state[2:4] == "11":
            assert result
        else:
            assert not result
    assert ab_plus_cd_table == TruthTable(Expression("ab+cd+dc+ba"))
    longer_one = Expression("ab+bcd")
    print(ab_plus_cd.raw_string+" and "+longer_one.raw_string+" are:")
    difference = ab_plus_cd.first_difference(longer_one)
    print(difference)
    assert "a=False, b=False, c=True, d=True" in difference
    print("TruthTable working 👍")
