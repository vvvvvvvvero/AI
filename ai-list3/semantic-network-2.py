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
        # yield LEDState(error='not_plugged_in', power='off', warning='off', ink='off')
        # yield LEDState(error='turned_off', power='off', warning='off', ink='off')
        # yield LEDState(error='paper_jam', power='blink', warning='blink', ink='off')
        # yield LEDState(error='no_paper', power='on', warning='on', ink='off')
        # yield LEDState(error='paper_tray_not_inserted', power='on', warning='on', ink='off')
        # yield LEDState(error='incorrect_paper_size', power='on', warning='blink', ink='off')

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

        yield Solution(problem='no_paper', action='insert a paper')
        yield Solution(problem='not_plugged_in', action='insert a power cable')
        yield Solution(problem='turned_off', action='turn on the printer')
        yield Solution(problem='paper_tray_not_inserted', action='insert a paper tray properly')
        yield Solution(problem='incorrect_paper_size', action='insert a proper paper size')
        yield Solution(problem='paper_jam', action='remove a paper jam')

        yield PrinterElement(element='paper_tray')
        yield PrinterElement(element='power_cable')
        yield PrinterElement(element='paper')
        yield PrinterElement(element='power_button')
        yield PrinterElement(element='power_cable')

    # @Rule(Solution(problem=MATCH.error, action=MATCH.action))
    # def define_solution(self, error, action):
    #     print(f"To resolve '{error}', action required: {action}")

    @Rule(LEDState(error=MATCH.error, power=MATCH.power, warning=MATCH.warning, ink=MATCH.ink),
          Problem(type=MATCH.type, state=MATCH.error))
    def define_problem_by_led(self, error, power, warning, ink, type):
        print(f"Problem defined by LED: {error} with State - Power: {power}, Warning: {warning}, Ink: {ink} as {type}")

    @Rule(Cause(element=MATCH.element, problem_type=MATCH.type, state=MATCH.error),
          PrinterElement(element=MATCH.element),
          LEDState(error=MATCH.error, power=MATCH.power, warning=MATCH.warning, ink=MATCH.ink))
    def define_cause(self, element, type, power, warning, ink):
        print(f"Problem: {type} caused by {element} under LED State: Power={power}, Warning={warning}, Ink={ink}")

    @Rule(LEDState(error=MATCH.error, power=MATCH.power, warning=MATCH.warning, ink=MATCH.ink),
          Solution(problem=MATCH.error, action=MATCH.action))
    def troubleshoot(self, error, power, warning, ink, action):
        print(
            f"Troubleshooting - Error: {error}, LED State: Power={power}, Warning={warning}, Ink={ink}. Recommended Action: {action}")


if __name__ == "__main__":
    engine = PrinterKnowledgeEngine()
    engine.reset()

    print('no paper')
    engine.declare(LEDState(error='no_paper', power='on', warning='on', ink='off'))
    engine.run()
    print()

    print('not plugged in')
    engine.declare(LEDState(error='not_plugged_in', power='off', warning='off', ink='off'))
    engine.run()
    print()

    print('incorrect paper size')
    engine.declare(LEDState(error='incorrect_paper_size', power='off', warning='blink', ink='off'))
    engine.run()
    print()

    print('paper jam')
    engine.declare(LEDState(error='paper_jam', power='blink', warning='blink', ink='off'))
    engine.run()
    print()
