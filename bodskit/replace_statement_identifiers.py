import json
import sys
from collections import OrderedDict
from uuid import uuid4

from jsonpath_rw import jsonpath, parse
import jsonpatch

class ReplaceStatementIdentifiers:

    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

    def handle(self):
        with open(self.input_filename) as f:
            package = json.load(f, object_pairs_hook=OrderedDict)
        new_package = self.replace_statement_ids_in_package(package)
        with open(self.output_filename, 'w+') as f:
            json.dump(new_package, f, indent=4, separators=(',', ': '))

    def expressions_from_paths(self, paths):
        return [parse(path) for path in paths]

    def path_to_patch_path(self, path):
        path = path.replace("].", "/")
        path = path.replace("[", "/")
        path = path.replace(".", "/")
        return path

    def dict_of_paths_from_expressions(self, expressions, jsono):
        paths = {}
        for exp in expressions:
            statement_ids = [(match.value, str(match.full_path)) for match in exp.find(jsono)]
            for i_d in statement_ids:
                if paths.get(i_d[0]) is None:
                    paths[i_d[0]] = [self.path_to_patch_path(i_d[1])]
                else:
                    paths[i_d[0]].append(self.path_to_patch_path(i_d[1]))
        return paths

    def patch_from_path_dict(self, path_dict):
        patch_list = []
        for k, v in path_dict.items():
            new_uuid = str(uuid4())
            for path in v:
                patch = {'op': 'replace',
                         'path': path,
                         'value': new_uuid}
                patch_list.append(patch)
        return jsonpatch.JsonPatch(patch_list)

    def replace_statement_ids_in_package(self, package):
        paths = ['[*]..statementID',
                 '[*]..describedByEntityStatement',
                 '[*]..describedByPersonStatement']
        expressions = self.expressions_from_paths(paths)
        path_dict = self.dict_of_paths_from_expressions(expressions, package)
        patch = self.patch_from_path_dict(path_dict)
        return patch.apply(package)

