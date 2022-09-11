import re
import logging

class Expression:
    log = logging.Logger("Expression")
    def __init__(self, raw_string: str):
        raw_string = raw_string.replace('’', "'")
        self.raw_string = raw_string
        literal_re = re.compile(r"[A-Za-z]\'?")
        # TODO: ability to prime paranthesized groups. add )' case to regex,
        # deal with by going backward to ( on same level and inserting a "not"
        # before it
        token_re = re.compile(literal_re.pattern + r"|\*|\.|\+|\(|\)")
        tokens = token_re.findall(raw_string)
        literals = set()
        self.log.debug(f"parsing raw expression: {raw_string}")
        self.log.debug(f"extracted raw tokens: {tokens}")
        processed_tokens = []
        for i, token in enumerate(tokens):
            if literal_re.match(token) is not None:
                if len(token) == 2:
                    processed_tokens.append(f"(not {token[0]})")
                else:
                    processed_tokens.append(token)
                if (
                    i != len(tokens)-1 and 
                    literal_re.match(tokens[i+1]) is not None
                ):
                    processed_tokens.append(f"and")
                literals.add(token[0])
            elif token == "*" or token == ".":
                processed_tokens.append("and")
            elif token == "+":
                processed_tokens.append("or")
            else:
                processed_tokens.append(token)
            
        self.expr = " ".join(processed_tokens)
        self.compiled_expr = compile(self.expr, "<string>", "eval")
        self.literals = sorted(list(literals))
        
        self.log.debug(f"derived python expression: {self.expr}")
        self.log.debug(f"collected variables: {self.literals}")
    
    @staticmethod
    def get_values_string(values: dict[str, bool]) -> str:
        return ', '.join([f'{x}={y}' for x, y in values.items()])
    
    def first_difference(self, other: "Expression") -> str:
        #TODO: test. also: refactor so that temporary truth tables aren't being
        #potentially expensively made and then thrown away?
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
        #TODO: refactor so that temporary truth tables aren't being
        #potentially expensively made and then thrown away?
        return TruthTable(self) == TruthTable(other)

class TruthTable:
    def __init__(self, expr: Expression):
        self.expr = Expression(expr.raw_string)  # defensive copy
        self.states: dict[str, bool] = {}
        for i in range(self.states_count):
            bits = bin(i)[2:]
            bits = "0"*(len(expr.literals)-len(bits)) + bits
            values = {}
            for i, literal in enumerate(expr.literals):
                values[literal] = bool(int(bits[i]))
            self.states[bits] = expr.evaluate(values)
    
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
