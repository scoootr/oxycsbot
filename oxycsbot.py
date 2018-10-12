#!/usr/bin/env python3

import re
from collections import Counter

class ChatBot:

    STATES = []
    TAGS = {}

    def __init__(self, default_state=None):
        if default_state is None:
            self.default_state = self.STATES[0]
        else:
            if default_state not in self.STATES:
                print(' '.join([
                    f'WARNING:',
                    f'The default state {default_state} is listed as a state.',
                    f'Perhaps you mean {self.STATES[0]}?',
                ]))
        self.state = self.default_state
        self.tags = {}
        self._check_states()
        self._check_tags()

    def _check_states(self):
        for state in self.STATES:
            prefixes = []
            if state != self.default_state:
                prefixes.append('on_enter')
            prefixes.append('respond_from')
            for prefix in prefixes:
                if not hasattr(self, f'{prefix}_{state}'):
                    print(' '.join([
                        f'WARNING:',
                        f'State "{state}" is defined',
                        f'but has no response function self.{prefix}_{state}',
                    ]))

    def _check_tags(self):
        for phrase in self.TAGS:
            tags = self.TAGS[phrase]
            if isinstance(tags, str):
                self.TAGS[phrase] = [tags]
            tags = self.TAGS[phrase]
            assert isinstance(tags, (tuple, list)), ' '.join([
                'ERROR:',
                'Expected tags for {phrase} to be str or List[str]',
                f'but got {tags.__class__.__name__}',
            ])

    def go_to_state(self, state, *args, **kwargs):
        assert state in self.STATES, f'state "{state}" is not defined'
        response = getattr(self, f'on_enter_{state}')(*args, **kwargs)
        self.state = state
        return response

    def chat(self):
        try:
            message = input('> ')
            while message.lower() not in ('exit', 'quit'):
                print()
                print(f'{self.__class__.__name__}: {self.respond(message)}')
                print()
                message = input('> ')
        except (EOFError, KeyboardInterrupt):
            print()
            exit()


    def respond(self, message):
        tags = self._get_tags(message)
        return getattr(self, f'respond_from_{self.state}')(message, tags)

    def finish(self, manner):
        response = getattr(self, f'finish_{manner}')()
        self.state = self.default_state
        return response

    def _get_tags(self, message):
        counter = Counter()
        msg = message.lower()
        for phrase, tags in self.TAGS.items():
            if re.search(r'\b' + phrase.lower() + r'\b', msg):
                counter.update(tags)
        return counter


class OxyCSBot(ChatBot):

    STATES = [
        'waiting',
        'specific_faculty',
        'unknown_faculty',
        'unrecognized_faculty',
    ]

    TAGS = {
        # intent
        'office hours': 'office-hours',
        'help': 'office-hours',

        # professors
        'kathryn': 'kathryn',
        'leonard': 'kathryn',
        'justin': 'justin',
        'li': 'justin',

        # generic
        'thanks': 'thanks',
        'okay': 'success',
        'bye': 'success',
        'yes': 'yes',
        'yep': 'yes',
        'no': 'no',
        'nope': 'no',
    }


    def __init__(self):
        super().__init__()
        self.faculty = None

    def default_response(self):
        return "Sorry, I'm just a simple bot that understands a few things. You can ask me about office hours though!"

    def get_office_hours(self, faculty):
        office_hours = {
            'kathryn': 'MWF 4-5pm',
            'justin': 'T 1-2pm; W noon-1pm; F 3-4pm',
        }
        return office_hours[faculty]

    def get_office(self, faculty):
        office_hours = {
            'kathryn': 'Swan B101',
            'justin': 'Swan B102',
        }
        return office_hours[faculty]

    def respond_from_waiting(self, message, tags):
        if 'office-hours' in tags:
            for faculty in ['justin', 'kathryn']:
                if faculty in tags:
                    self.faculty = faculty
                    return self.go_to_state('specific_faculty')
            return self.go_to_state('unknown_faculty')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.default_response()

    def on_enter_specific_faculty(self):
        response = '\n'.join([
            f"{self.faculty.capitalize()}'s office hours are {self.get_office_hours(self.faculty)}",
            'Do you know where their office is?',
        ])
        return response

    def respond_from_specific_faculty(self, message, tags):
        if 'yes' in tags:
            return self.finish('success')
        else:
            return self.finish('location')

    def on_enter_unknown_faculty(self):
        return "Who's office hours are you looking for?"

    def respond_from_unknown_faculty(self, message, tags):
        for faculty in ['justin', 'kathryn']:
            if faculty in tags:
                self.faculty = faculty
                return self.go_to_state('specific_faculty')
        return self.go_to_state('unrecognized_faculty')

    def on_enter_unrecognized_faculty(self):
        return "I'm not sure I understand - are you looking for Kathryn Leonard, or Justin Li?"

    def respond_from_unrecognized_faculty(self, message, tags):
        for faculty in ['justin', 'kathryn']:
            if faculty in tags:
                self.faculty = faculty
                return self.go_to_state('specific_faculty')
        return self.finish('fail')

    def finish_location(self):
        response = f"{self.faculty.capitalize()}'s office is in {self.get_office(self.faculty)}"
        self.faculty = None
        return response

    def finish_success(self):
        return 'Great, let me know if you need anything else!'

    def finish_fail(self):
        return "I've tried my best but I still don't understand. Maybe try asking other students?"

    def finish_thanks(self):
        return "You're welcome!"

    def finish_cancel(self):
        return "Okay, just let me know if you need anything else!"


def main():
    OxyCSBot().chat()


if __name__ == '__main__':
    main()
