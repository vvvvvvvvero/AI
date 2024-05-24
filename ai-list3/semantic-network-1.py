from experta import *

class Printer(Fact):
    """Information about the printer"""
    pass

class Capability(Fact):
    """Capabilities of the printer"""
    pass

class InkCartridge(Fact):
    """Information about ink cartridges"""
    pass

class PrinterElement(Fact):
    """Elements of the printer"""
    pass

class PrinterPanelElement(Fact):
    """Elements of the printer panel"""
    pass

class StatusDiode(Fact):
    """Status diodes of the printer"""
    pass


class PrinterKnowledgeEngine(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Printer(name='Brother DCP-T225', type='color_printer', category='inkjet_printer',
                      connectivity='wireless_printer', function='multifunction_printer')

        yield Capability(name='Brother DCP-T225', action='can_print', mode='black_and_white')
        yield Capability(name='Brother DCP-T225', action='can_print', mode='color')
        yield Capability(name='Brother DCP-T225', action='can_scan', mode='black_and_white')
        yield Capability(name='Brother DCP-T225', action='can_scan', mode='color')
        yield Capability(name='Brother DCP-T225', action='can_copy', mode='black_and_white')
        yield Capability(name='Brother DCP-T225', action='can_copy', mode='color')
        yield Capability(name='Brother DCP-T225', action='can_print_via_wifi')
        yield Capability(name='Brother DCP-T225', action='can_print_via_usb')

        yield InkCartridge(color='black', code='btD60BK')
        yield InkCartridge(color='cyan', code='bt5000C')
        yield InkCartridge(color='magenta', code='bt5000M')
        yield InkCartridge(color='yellow', code='bt5000Y')

        yield PrinterElement(name='power_cable')
        yield PrinterElement(name='usb_cable')
        yield PrinterElement(name='paper_tray')
        yield PrinterElement(name='paper')
        yield PrinterElement(name='printhead')
        yield PrinterElement(name='black_ink_cartridge')
        yield PrinterElement(name='cyan_ink_cartridge')
        yield PrinterElement(name='yellow_ink_cartridge')
        yield PrinterElement(name='magenta_ink_cartridge')

        yield PrinterPanelElement(name='power_button')
        yield PrinterPanelElement(name='start_color_button')
        yield PrinterPanelElement(name='start_mono_button')
        yield PrinterPanelElement(name='fast_copy_button')

        yield StatusDiode(name='led_diode_power')
        yield StatusDiode(name='led_diode_warning')
        yield StatusDiode(name='ink_led_diode')
        yield StatusDiode(name='wifi_diode_button')

    # czy drukarka jest bezprzewodowa
    @Rule(Capability(name='Brother DCP-T225', action='can_print_via_wifi'))
    def is_wireless(self):
        print("Yes, the printer is wireless.")

    # czy drukarka potrafi skanować kolorowe dokumenty
    @Rule(Capability(name='Brother DCP-T225', action='can_scan', mode='color'))
    def can_scan(self):
        print("Yes, the printer has scanning in color capabilities.")

    # jakie są dostępne tryby drukowania
    @Rule(Capability(name='Brother DCP-T225', action='can_print', mode=MATCH.mode))
    def print_modes(self, mode):
        print(f"The printer can print in the following mode: {mode}")

    # jakie są elementy drukarki
    @Rule(PrinterElement(name=MATCH.name))
    def printer_elements(self, name):
        print(f"The printer includes the following element: {name}")

    # jakie są dostępne farby i ich numery
    @Rule(InkCartridge(color=MATCH.color, code=MATCH.code))
    def list_ink_cartridges(self, color, code):
        print(f"The {color} ink cartridge number is: {code}")


if __name__ == "__main__":
    engine = PrinterKnowledgeEngine()
    engine.reset()
    engine.run()
