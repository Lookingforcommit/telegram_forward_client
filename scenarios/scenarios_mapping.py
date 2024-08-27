# (c) @Lookingforcommit

from typing import Dict

from scenarios.scenarios_classes.sample_scenario import SampleScenario
from scenarios.scenarios_classes.base import BaseScenario

OBJECTS_MAPPING: Dict[str, BaseScenario] = {
    "sample_scenario": SampleScenario(),
}
