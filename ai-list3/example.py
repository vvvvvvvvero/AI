from experta import *

class LEDState(Fact):
    """ Represents the current state of the printer's LEDs. """
    error = Field(str, mandatory=True)
    power = Field(str, mandatory=True)
    warning = Field(str, mandatory=True)
    ink = Field(str, mandatory=True)


class Problem(Fact):
    """ Represents a problem identified by its type and associated state. """
    type = Field(str, mandatory=True)
    state = Field(str, mandatory=True)


class Cause(Fact):
    """ Represents what element is causing which problem and under what state. """
    element = Field(str, mandatory=True)
    problem_type = Field(str, mandatory=True)
    state = Field(str, mandatory=True)


class Solution(Fact):
    """ Represents solutions to problems. """
    problem = Field(str, mandatory=True)
    action = Field(str, mandatory=True)


class PrinterElement(Fact):
    """ Represents physical elements of the printer. """
    element = Field(str, mandatory=True)


class PrinterKnowledgeEngine(KnowledgeEngine):
    @DefFacts()
    def _initial_facts(self):
        yield Problem(type='no_power', state='not_plugged_in')
        yield Problem(type='off', state='turned_off')
        yield Problem(type='dont_print', state='paper_jam')
        yield Problem(type='dont_print', state='no_paper')
        yield Problem(type='dont_print', state='incorrect_paper_size')
        yield Problem(type='dont_print', state='paper_tray_not_inserted')

        yield Cause(element='power_cable', problem_type='no_power', state='not_plugged_in')
        yield Cause(element='power_button', problem_type='off', state='turned_off')
        yield Cause(element='paper', problem_type='dont_print', state='no_paper')
        yield Cause(element='paper_tray', problem_type='dont_print', state='paper_tray_not_inserted')
        yield Cause(element='paper', problem_type='dont_print', state='incorrect_paper_size')
        yield Cause(element='paper', problem_type='dont_print', state='paper_jam')

        yield Solution(problem='no_paper', action='Insert paper.')
        yield Solution(problem='not_plugged_in', action='Plug in the power cable.')
        yield Solution(problem='turned_off', action='Turn on the printer.')
        yield Solution(problem='paper_tray_not_inserted', action='Insert the paper tray properly.')
        yield Solution(problem='incorrect_paper_size', action='Insert proper paper size.')
        yield Solution(problem='paper_jam', action='Remove the paper jam.')

        yield PrinterElement(element='paper_tray')
        yield PrinterElement(element='power_cable')
        yield PrinterElement(element='paper')
        yield PrinterElement(element='power_button')
        yield PrinterElement(element='power_cable')

    @Rule(LEDState(error=MATCH.error, power=MATCH.power, warning=MATCH.warning, ink=MATCH.ink),
          Problem(type=MATCH.type, state=MATCH.error))
    def define_problem_by_led(self, error, power, warning, ink, type):
        self.declare(Fact(problem_type=type, problem_state=error))
        print(f"Problem defined by LED: {error} with State - Power: {power}, Warning: {warning}, Ink: {ink} as {type}")

    @Rule(Fact(problem_type=MATCH.type, problem_state=MATCH.error),
          Cause(element=MATCH.element, problem_type=MATCH.type, state=MATCH.error))
    def define_cause(self, element, type, error):
        self.declare(Fact(problem_cause=element))
        print(f"Problem: {type} caused by {element} under state: {error}")

    @Rule(Fact(problem_type=MATCH.type, problem_state=MATCH.error),
          Solution(problem=MATCH.error, action=MATCH.action))
    def troubleshoot(self, type, error, action):
        print(f"Troubleshooting - Problem: {type}, Error: {error}. Recommended Action: {action}")


if __name__ == "__main__":
    engine = PrinterKnowledgeEngine()
    engine.reset()

    # Provide the specific LED state that represents the issue
    engine.declare(LEDState(error='no_paper', power='on', warning='on', ink='off'))
    engine.run()
