"""A simple chatbot that directs students to office hours of CS professors."""

from chatbot import ChatBot


class  OxyCSBot(ChatBot):
    """A simple chatbot that directs students to office hours of CS professors."""

    STATES = [
        'waiting',
        'specific_faculty',
        'unknown_faculty',
        'unrecognized_faculty',
        'introduction',
        'save_name',
        'indentify_company',
        'save_company'
    ]

    TAGS = {

        'interview':'interview',
        # company name
        'kathryn': 'kathryn',
        'leonard': 'kathryn',
        'justin': 'justin',
        'li': 'justin',
        'jeff': 'jeff',
        'miller': 'jeff',
        'celia': 'celia',
        'hsing-hau': 'hsing-hau',
        'umit': 'umit',
        'yalcinalp': 'umit',

        # job description
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
        'umit',
    ]

    def __init__(self):
        """Initialize the OxyCSBot.
        The `professor` member variable stores whether the target professor has
        been identified.
        """
        super().__init__(default_state='waiting')
        self.name = None


    def get_office(self, professor):
        """Find the office of a professor.
        Arguments:
            professor (str): The professor of interest.
        Returns:
            str: The office of that professor.
        """
        office = {
            'celia': 'Swan 232',
            'hsing-hau': 'Swan 302',
            'jeff': 'Fowler 321',
            'justin': 'Swan B102',
            'kathryn': 'Swan B101',
            'umit': 'Swan 226',
        }
        return office[professor]

    # "waiting" state functions

    def respond_from_waiting(self, message, tags):
        """Decide what state to go to from the "waiting" state.
        Parameters:
            message (str): The incoming message.
            tags (Mapping[str, int]): A count of the tags that apply to the message.
        Returns:
            str: The message to send to the user.
        """
        self.name = None
        if 'interview' in tags:
            return self.go_to_state('introduction')
        elif 'thanks' in tags:
            return self.finish('generic')
        else:
            return self.finish('confused')

    def on_enter_introduction(self):
        # Send a message when entering the introduction state.
        response = '\n'.join([
            "Hi I am, I am here to help you work on your interviewing skills.",
            "What is your name?"
        ])
        return response, self.go_to_state('save_name')

    def on_enter_save_name(self, message, tags):
        """ Define name of user
        Parameters:
            message (str): The incoming message.
            tags (Mapping[str, int]): A count of the tags that apply to the message.
        Returns:
            str: The message to send to the user.
        """

        """ must parse message and save name to self.name?"""

        response = '\n'.join([
            f"Hi, {self.name}, I am looking forward to helping you work on your interview skills.",
        ]),

        return response, self.go_to_state('indentify_company')

    def on_enter_identify_company(self, message, tags):
        response = '\n'.join([
            "Is there a specific company you are planning to apply to, and if so, what is it?"
        ])
        return response, self.go_to_state('save_company')

    def on_enter_save_company(self,message,tags):
        if 'yes' in tags:
            # assign self.company to inputted company name
            response = '\n'.join([
                "Great! What position are you applying for?"
            ])
            return self.go_to_state('position')
        elif 'no' in tags:
            response = '\n'.join([
                "No problem! How about a specific position?"
            ])
            return self.go_to_state('position')
        else:
            response = '\n'.join([
                "Okay."
            ])
            return self.go_to_state('position')

    def on_enter_position(self, message, tags):
        if 'yes' in tags:
            response = '\n'.join([
                "Wow, that sounds like an amazing opportunity!"
            ])
        elif 'no' in tags:
            response = '\n'.join([
                "Don't worry that's fine! I'll still prepare you for whatever comes your way"
            ])
        else:
            response = '\n'.join([
                "Okaym thanks for letting me know."
            ])
        return response, self.go_to_state('transition_interview')

    def on_enter_transition_interview(self):
        response = '\n'.join([
            "Would you like to start a casual mock interview?",
            "It would only take around five minutes.",
            "I’ll ask you some of the most common interview questions",
            "and give you a few pointers in parenthesis along the way."
        ])
        return response, self.go_to_state('interview_decision')

    def on_enter_interview_decision(self, message, tags):
        if 'yes' in tags:
            response = '\n'.join([
                "Great, let’s begin! Remember, you should treat this as if it was a “real” interview,",
                " so be purposeful with your words. I’ll be right back, I’m gonna change into my suit and tie!"
                ])
            return response, self.go_to_state('start_interview')
        elif 'no' in tags:
            response = '\n'.join([
                "Unfortunately, the best way for me to give you feedback would be through conversation."
            ])
            return response, self.finish('generic')
        else:
            response = '\n'.join([
                "Sorry, could you please clarify."
            ])
            return response, self.go_to_state('interview_decision')

    def on_enter_start_interview(self):
        response = '\n'.join([
            f"Good morning {self.name}. I’m Siri , pleased to meet you.",
            " I’ll be interviewing you today."
        ])
        return response, self.go_to_state('strengths_question')






    def on_enter_specific_faculty(self):
        """Send a message when entering the "specific_faculty" state."""
        response = '\n'.join([
            f"{self.professor.capitalize()}'s office hours are {self.get_office_hours(self.professor)}",
            'Do you know where their office is?',
        ])
        return response


    def respond_from_specific_faculty(self, message, tags):
        """Decide what state to go to from the "specific_faculty" state.
        Parameters:
            message (str): The incoming message.
            tags (Mapping[str, int]): A count of the tags that apply to the message.
        Returns:
            str: The message to send to the user.
        """
        if 'yes' in tags:
            return self.finish('success')
        else:
            return self.finish('location')

    # "unknown_faculty" state functions

    def on_enter_unknown_faculty(self):
        """Send a message when entering the "unknown_faculty" state."""
        return "Who's office hours are you looking for?"

    def respond_from_unknown_faculty(self, message, tags):
        """Decide what state to go to from the "unknown_faculty" state.
        Parameters:
            message (str): The incoming message.
            tags (Mapping[str, int]): A count of the tags that apply to the message.
        Returns:
            str: The message to send to the user.
        """
        for professor in self.PROFESSORS:
            if professor in tags:
                self.professor = professor
                return self.go_to_state('specific_faculty')
        return self.go_to_state('unrecognized_faculty')

    # "unrecognized_faculty" state functions

    def on_enter_unrecognized_faculty(self):
        """Send a message when entering the "unrecognized_faculty" state."""
        return ' '.join([
            "I'm not sure I understand - are you looking for",
            "Celia, Hsing-hau, Jeff, Justin, Kathryn, or Umit?",
        ])

    def respond_from_unrecognized_faculty(self, message, tags):
        """Decide what state to go to from the "unrecognized_faculty" state.
        Parameters:
            message (str): The incoming message.
            tags (Mapping[str, int]): A count of the tags that apply to the message.
        Returns:
            str: The message to send to the user.
        """
        for professor in self.PROFESSORS:
            if professor in tags:
                self.professor = professor
                return self.go_to_state('specific_faculty')
        return self.finish('fail')

    # "finish" functions

    def finish_negative(self):
        """Send a message and go to the default state."""
        return "Trust me it wasn’t that bad. Feel free to come back for more practice! See you!"

    def finish_positive(self):
        """Send a message and go to the default state."""
        return 'Awesome! Glad I could help!'

    def finish_generic(self):
        """Send a message and go to the default state."""
        return "Well, it was nice talking to you! I hope you were able to gain something from this experience."

    =

if __name__ == '__main__':
    OxyCSBot().chat()
