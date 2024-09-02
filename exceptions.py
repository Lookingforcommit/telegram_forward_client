# (c) @Lookingforcommit
# TODO: Add exceptions classes for bot commands processing

from abc import abstractmethod


class ScenariosExecutionException(Exception):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class ScenarioException(ScenariosExecutionException):
    def __init__(self, stage_number: int, scenario_name: str, exc: str):
        self.error_message = f"Error executing scenario {scenario_name} for stage #{stage_number}: \n{exc}"

    def __str__(self):
        return self.error_message


class PreprocessCopyingException(ScenariosExecutionException):
    def __init__(self, message_id: int, exc: str):
        self.error_message = f"Error copying message {message_id} for scenarios execution: \n{exc}"

    def __str__(self):
        return self.error_message
