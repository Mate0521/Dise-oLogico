import re

class BooleanConverter:
    def convert_expression(self, expr):
        prev = None
        while prev != expr:
            prev = expr
            expr = self._replace_xnor(expr)
            expr = self._replace_xor(expr)
        return expr

    def _replace_xor(self, expr):
        # Busca la forma más a la izquierda de "algo xor algo"
        pattern = re.compile(r'(\([^\(\)]+\)|[A-Z])\s*xor\s*(\([^\(\)]+\)|[A-Z])')
        while re.search(pattern, expr):
            expr = re.sub(pattern, lambda m: f"(({m.group(1)} and not {m.group(2)}) or (not {m.group(1)} and {m.group(2)}))", expr)
        return expr

    def _replace_xnor(self, expr):
        pattern = re.compile(r'(\([^\(\)]+\)|[A-Z])\s*xnor\s*(\([^\(\)]+\)|[A-Z])')
        while re.search(pattern, expr):
            expr = re.sub(pattern, lambda m: f"(({m.group(1)} and {m.group(2)}) or (not {m.group(1)} and not {m.group(2)}))", expr)
        return expr