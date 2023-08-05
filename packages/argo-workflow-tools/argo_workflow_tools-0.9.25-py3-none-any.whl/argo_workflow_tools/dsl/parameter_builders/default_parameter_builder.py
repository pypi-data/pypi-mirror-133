from typing import Callable
from typing import Set

from argo_workflow_tools.dsl.parameter_builders.parameter_builder import (
    ParameterBuilder,
)


class DefaultParameterBuilder(ParameterBuilder):
    def __init__(
        self,
        type_annotation: type,
        file_prefix: str = "/tmp",
    ):
        super().__init__()
        self.file_prefix = file_prefix
        self.type_annotation = type_annotation

    def imports(self) -> Set[str]:
        return {"import json"}

    def artifact_path(self, parameter_name: str) -> str:
        return f"{self.file_prefix}/{parameter_name}.json"

    def variable_from_input(
        self, parameter_name: str, variable_name: str, function: Callable
    ) -> str:
        if self.type_annotation.__name__ == "_empty":
            raise ValueError(
                "DefaultParameterBuilder uses type annotations to generate serializers for types, "
                f"yet parameter '{parameter_name}' in function '{function}' does not provide any. "
                "annotate your input parameter, or set a specific ParameterBuilder in the decorator. "
            )
        if self.type_annotation == str:
            return f"{variable_name}_raw = '{{{{inputs.parameters.{parameter_name}}}}}'\n" + \
                   f"try:\n" + \
                   f"    {variable_name} = json.loads({variable_name}_raw)\n" + \
                   "except:\n" + \
                   f'    {variable_name} = {variable_name}_raw\n'
        else:
            f"{variable_name}=json.loads('{{{{inputs.parameters.{parameter_name}}}}}')"

    def variable_to_output(
        self, parameter_name: str, variable_name: str, function: Callable
    ) -> str:
        return f"with open('{self.artifact_path(parameter_name)}', 'a') as file:\n  file.write(json.dumps({variable_name}))"


