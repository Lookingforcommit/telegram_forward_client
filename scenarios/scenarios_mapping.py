# (c) @Lookingforcommit

from typing import Dict

from scenarios.scenarios_classes.links_deletion import TextLinksDeletionScenario
from scenarios.scenarios_classes.sample_scenario import SampleScenario
from scenarios.scenarios_classes.base import BaseScenario
from scenarios.scenarios_classes.text_deletion import TextDeletionScenario
from scenarios.scenarios_classes.text_insertion import TextInsertionScenario
from scenarios.scenarios_classes.text_replacement import TextReplacementScenario
from scenarios.scenarios_classes.regex_empty import RegexEmptyScenario

OBJECTS_MAPPING: Dict[str, BaseScenario] = {
    "sample_scenario": SampleScenario(),
    "text_replacement": TextReplacementScenario(),
    "text_deletion": TextDeletionScenario(),
    "text_insertion": TextInsertionScenario(),
    "links_deletion": TextLinksDeletionScenario(),
    "regex_empty":  RegexEmptyScenario(),
}
