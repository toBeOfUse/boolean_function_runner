import re
import logging

class Expression:
    log = logging.Logger("Expression")
    def __init__(self, raw_string: str):
        raw_string = raw_string.replace('’', "'")
        self.raw_string = raw_string
        literal_re = re.compile(r"[A-Za-z]\'?")
        token_re = re.compile(literal_re.pattern + r"|\*|\.|\+|\(|\)\'|\)")
        tokens = token_re.findall(raw_string)
        literals = set()
        self.log.debug(f"parsing raw expression: {raw_string}")
        self.log.debug(f"extracted raw tokens: {tokens}")
        processed_tokens = []
        for i, token in enumerate(tokens):
            is_literal = literal_re.match(token) is not None
            if is_literal:
                if len(token) == 2:
                    processed_tokens.append("not")
                processed_tokens.append(token[0])
                literals.add(token[0])
            elif token == ")'":
                # deal with an inverted parenthesized group by going back to the
                # beginning of the group and putting "not" in front of it
                processed_tokens.append(")")
                pos = len(processed_tokens)-1
                level = 0
                while True:
                    past_token = processed_tokens[pos]
                    if past_token == ")":
                        level += 1
                    elif past_token == "(":
                        level -= 1
                    if level == 0:
                        processed_tokens.insert(pos, "not")
                        break
                    pos -= 1
            elif token == "*" or token == ".":
                processed_tokens.append("and")
            elif token == "+":
                processed_tokens.append("or")
            else:
                processed_tokens.append(token)
            if (
                    (is_literal or token == ")" or token == ")'") and
                    i != len(tokens)-1
            ):
                # if we're currently looking at a literal or close-parenthesis
                # and the next token is a literal or open-parenthesis, insert
                # the implicit "and"
                next_token = tokens[i+1]
                if (
                    literal_re.match(next_token) is not None or
                    next_token == "("
                ):
                    processed_tokens.append(f"and")
            
        self.expr = " ".join(processed_tokens)
        self.compiled_expr = compile(self.expr, "<string>", "eval")
        self.literals = sorted(list(literals))
        
        self.log.debug(f"derived python expression: {self.expr}")
        self.log.debug(f"collected variables: {self.literals}")

        # note: internal state of Expression object should never change after
        # construction
    
    @staticmethod
    def get_values_string(values: dict[str, bool]) -> str:
        return ', '.join([f'{x}={y}' for x, y in values.items()])
    
    def first_difference(self, other: "Expression") -> str:
        # TODO: refactor so that temporary truth tables aren't being potentially
        # expensively made and then thrown away? same as __eq__
        bits = TruthTable(self).first_difference(TruthTable(other))
        if bits is None:
            return "expressions are equal"
        values = {}
        for literal, bit in zip(self.literals, bits):
            values[literal] = bool(int(bit))
        return "different when "+self.get_values_string(values)

    
    def evaluate(self, values: dict[str, bool]):
        for literal in self.literals:
            if literal not in values:
                raise ValueError(
                    f"missing argument for {literal} while "
                    f"evaluating {self.raw_string}"
                )
        result = eval(self.compiled_expr, {}, values)
        values_string = self.get_values_string(values)
        self.log.debug(f"{self.raw_string} with {values_string} is {result}")
        return result
    
    def __eq__(self, other: "Expression") -> bool:
        # TODO: refactor so that temporary truth tables aren't being potentially
        # expensively made and then thrown away? same as first_difference
        return TruthTable(self) == TruthTable(other)

class TruthTable:
    def __init__(self, expr: Expression):
        self.expr = expr
        self.states: dict[str, bool] = {}
        for i in range(self.states_count):
            bits = bin(i)[2:]
            bits = "0"*(len(expr.literals)-len(bits)) + bits
            values = {}
            for i, literal in enumerate(expr.literals):
                values[literal] = bool(int(bits[i]))
            self.states[bits] = expr.evaluate(values)
        
        # note: internal state of TruthTable should not change after
        # construction
    
    @property
    def states_count(self):
        return 2**len(self.expr.literals)
    
    def __repr__(self):
        table_string = "\t".join(self.expr.literals+["result"])+"\n"
        for state, result in self.states.items():
            table_string += "\t".join(state)+"\t"+str(int(result))+"\n"
        return table_string + "\n"
    
    def first_difference(self, other: "TruthTable") -> str | None:
        #TODO: test
        if self.states_count != other.states_count:
            raise ValueError("different number of variables")
        for state in self.states:
            if other.states[state] != self.states[state]:
                return state
        return None
    
    def __eq__(self, other: "TruthTable") -> bool:
        return self.first_difference(other) is None
            

if __name__ == "__main__":
    expr_one = Expression(input("Enter expression: ").strip())
    expr_two = Expression(input("Enter another: ").strip())
    print(expr_one.first_difference(expr_two))
