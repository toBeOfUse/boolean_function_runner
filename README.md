I created this repository to evaluate arbitrary Boolean functions written in the form we've been using in my Advanced Digital Design class. This form consists of single-letter variable names alongside parentheses, `'` meaning NOT, `+` meaning OR, and sometimes `*` or `.` meaning AND. Examples include `AB+BC` and `((xz)'(x'z')'(x'y)')'`.

The Expression class parses a string in that form and creates an equivalent Python expression, which it can then evaluate given a mapping of variable names to values.

The TruthTable class evaluates an Expression for every possible variable state and stores the results. A TruthTable object can be displayed as a string in the typical form. It can also be compared with another TruthTable object; if the TruthTable objects for two different Expressions are equal, then the expressions are algebraically equivalent.
