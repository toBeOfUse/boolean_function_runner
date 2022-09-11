I created this repository to evaluate arbitrary Boolean functions written in the form we've been using in my Advanced Digital Design class. This form consists of single-letter variable names alongside parentheses, `'` meaning NOT, `+` meaning OR, and sometimes `*` or `.` meaning AND. Examples include `AB+BC` and `((xz)'(x'z')'(x'y)')'`.

The Expression class parses a string in that form and creates an equivalent Python expression, which it can then evaluate given a mapping of variable names to values. It utilizes the TruthTable class to enable equality comparisons between Expressions and the ability to see what inputs they are different for.

The TruthTable class evaluates an Expression for every possible variable state and stores the results. A TruthTable object can be displayed as a string in the typical form. It can also be compared for equality with other TruthTable objects, which enables Expressions to be so compared as well.

Example code:

```python
simple_and = Expression("xy")
assert not simple_and.evaluate({"x": True, "y": False})
assert simple_and.evaluate({"x": True, "y": True})
simple_or = Expression("x+y")
print(simple_and.first_difference(simple_or))  # > different when x=False, y=True

sum_of_products = Expression("xz + x'z' + x'y")
nand_version = Expression("((xz)'(x'z')'(x'y)')'")
nor_version = Expression("(x'+z')'+(x+z)'+(x+y')'")
assert sum_of_products == nand_version
assert sum_of_products == nor_version
print(sum_of_products.truth_table())
"""
x       y       z       result
0       0       0       1
0       0       1       0
0       1       0       1
0       1       1       1
1       0       0       0
1       0       1       1
1       1       0       0
1       1       1       1
"""
```
