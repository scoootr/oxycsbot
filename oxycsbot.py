#!/usr/bin/env python3
"""A simple chatbot that directs students to office hours of CS professors."""

from chatbot import ChatBot

class OxyCSBot(ChatBot):
    """A simple chatbot that directs students to office hours of CS professors."""

    STATES = [
        'waiting',
        'specific_faculty',
        'unknown_faculty',
        'unrecognized_faculty',
    ]

    TAGS = {
        # intent
        'office hours': 'office-hours',
        'OH': 'office-hours',
        'help': 'office-hours',

        # professors
        'kathryn': 'kathryn',
        'leonard': 'kathryn',
        'justin': 'justin',
        'li': 'justin',
        'jeff': 'jeff',
        'miller': 'jeff',
        'celia': 'celia',
        'hsing-hau': 'hsing-hau',

        # generic
        'thanks': 'thanks',
        'okay': 'success',
        'bye': 'success',
        'yes': 'yes',
        'yep': 'yes',
        'no': 'no',
        'nope': 'no',
    }

    PROFESSORS = [
        'celia',
        'hsing-hau',
        'jeff',
        'justin',
        'kathryn',
    ]

    def __init__(self):
        """Initialize the OxyCSBot.

        The `professor` member variable stores whether the target
        professor has been identified.
        """
        super().__init__(default_state='waiting')
        self.professor = None

    def get_office_hours(self, professor):
        """Find the office hours of a professor.

        Arguments:
            professor (str): The professor of interest.

        Returns:
            str: The office hours of that professor.
        """
        office_hours = {
            'celia': 'F 12-1:45pm; F 2:45-4:00pm',
            'hsing-hau': 'T 1-2:30pm; Th 10:30am-noon',
            'jeff': 'unknown',
            'justin': 'T 1-2pm; W noon-1pm; F 3-4pm',
            'kathryn': 'MWF 4-5pm',
        }
        return office_hours[professor]

    def get_office(self, professor):
        """Find the office of a professor.

        Arguments:
            professor (str): The professor of interest.

        Returns:
            str: The office of that professor.
        """
        office = {
            'celia': 'Swan 216',
            'hsing-hau': 'Swan 302',
            'jeff': 'Fowler 321',
            'justin': 'Swan B102',
            'kathryn': 'Swan B101',
        }
        return office[professor]

    # "waiting" state functions

    def respond_from_waiting(self, message, tags):
        self.professor = None
        if 'office-hours' in tags:
            for professor in self.PROFESSORS:
                if professor in tags:
                    self.professor = professor
                    return self.go_to_state('specific_faculty')
            return self.go_to_state('unknown_faculty')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.finish('confused')

    # "specific_faculty" state functions

    def on_enter_specific_faculty(self):
        response = '\n'.join([
            f"{self.professor.capitalize()}'s office hours are {self.get_office_hours(self.professor)}",
            'Do you know where their office is?',
        ])
        return response

    def respond_from_specific_faculty(self, message, tags):
        if 'yes' in tags:
            return self.finish('success')
        else:
            return self.finish('location')

    # "unknown_faculty" state functions

    def on_enter_unknown_faculty(self):
        return "Who's office hours are you looking for?"

    def respond_from_unknown_faculty(self, message, tags):
        for professor in self.PROFESSORS:
            if professor in tags:
                self.professor = professor
                return self.go_to_state('specific_faculty')
        return self.go_to_state('unrecognized_faculty')

    # "unrecognized_faculty" state functions

    def on_enter_unrecognized_faculty(self):
        return ' '.join([
            "I'm not sure I understand - are you looking for",
            "Celia, Hsing-hau, Jeff, Justin, or Kathryn?",
        ])

    def respond_from_unrecognized_faculty(self, message, tags):
        for professor in self.PROFESSORS:
            if professor in tags:
                self.professor = professor
                return self.go_to_state('specific_faculty')
        return self.finish('fail')

    # "finish" functions

    def finish_confused(self):
        return "Sorry, I'm just a simple bot that can't understand much. You can ask me about office hours though!"

    def finish_location(self):
        return f"{self.professor.capitalize()}'s office is in {self.get_office(self.professor)}"

    def finish_success(self):
        return 'Great, let me know if you need anything else!'

    def finish_fail(self):
        return "I've tried my best but I still don't understand. Maybe try asking other students?"

    def finish_thanks(self):
        return "You're welcome!"


if __name__ == '__main__':
    OxyCSBot().chat()
