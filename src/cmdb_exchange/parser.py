from copy import deepcopy


class Parser:
    def visit(self, node):
        visit_node_name = 'visit_' + type(node).__name__
        try:
            visit_node = getattr(self, visit_node_name, None)
        except:
            raise RuntimeError(
                'No {} method'.format('visit_' + type(node).__name__))
        return visit_node(node)


class FlatDataParser(Parser):

    def __init__(self):
        self._collected_info = {}
        self.result = []
        self.key = ''

    def visit_list(self, node) -> None:
        for k, v in enumerate(node):
            self.visit(v)
            self.result.append(deepcopy(self._collected_info))

    def visit_dict(self, node) -> None:
        for key, value in node.items():
            self.key = key
            self.visit(value)

    def visit_int(self, node) -> None:
        self._collected_info[self.key] = node

    def visit_str(self, node) -> None:
        self._collected_info[self.key] = node

    def visit_bool(self, node) -> None:
        self._collected_info[self.key] = node
