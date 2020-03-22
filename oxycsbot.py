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
        'introduction',
        'save_name',
        'identify_company',
        'save_company',
        'position',
        'transition_interview',
        'interview_decision',
        'start_interview',
        'weaknesses',
        'weakness_feedback',
        'challenge',
        'challenge_feedback',
        'experience',
    ]

    TAGS = {
        # intent
        'office hours': 'office-hours',
        'OH': 'office-hours',
        'help': 'office-hours',
        'hello': 'hello',
        'hey': 'hello',
        'hi': 'hello',
        'cool': 'introduction',
        'awesome': 'introduction',
        'interview': 'interview',
        'Yes':'transition_interview',
        'Sure':'transition_interview',


        # professors
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
        'umit',
    ]

    def __init__(self):
        """Initialize the OxyCSBot.
        The `professor` member variable stores whether the target professor has
        been identified.
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
            'celia': 'unknown',
            'hsing-hau': 'MW 3:30-4:30pm; F 11:45am-12:45pm',
            'jeff': 'W 4-5pm; Th 12:50-1:50pm; F 4-5pm',
            'justin': 'T 3-4pm; W 2-3pm; F 4-5pm',
            'kathryn': 'MF 4-5:30pm',
            'umit': 'M 3-5pm; W 10am-noon, 3-5pm',
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
        self.professor = None
        if 'hello' in tags:
            return self.go_to_state('introduction')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.finish('confused')

    # "specific_faculty" state functions

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
    def on_enter_introduction(self):
        return "I am here to help you work on your interviewing skills. What is your name?"
    def respond_from_introduction(self,message,tags):
        return self.go_to_state('save_name')

    def on_enter_save_name(self):
        return "Hi, I am looking forward to helping you work on your interview skills."
    def respond_from_save_name(self,message,tags):
        return self.go_to_state('identify_company')

    def on_enter_identify_company(self):
        return "Is there a specific company you are planning to apply to, and if so, what is it?"
    def respond_from_identify_company(self,message,tags):
        return self.go_to_state('save_company')

    def on_enter_save_company(self):
        return "Great! What position are you applying for?"

    def respond_from_save_company(self,message,tags):
        return self.go_to_state('unknown_faculty')
"""
    def on_enter_position(self):
        return "Okay thanks for letting me know."

    def respond_from_position(self,message,tags):
        return self.go_to_state('transition_interview')

    def on_enter_transition_interview(self):
        return "Would you like to start a casual mock interview? It would only take around five minutes. I’ll ask you some of the most common interview questions and give you a few pointers in parenthesis along the way."
    def respond_from_transition_interview(self,message,tags):
        return self.go_to_state("unknown_faculty")

    def respond_from_transition_interview(self,message,tags):
        return self.go_to_state('interview_decision')

    def on_enter_interview_decision(self):
        if 'yes' in self.TAGS:
            self.response = "Great, let’s begin! Remember, you should treat this as if it was a real interview, so be purposeful with your words. I’ll be right back, I’m gonna change into my suit and tie!"
            return self.response
        elif 'no' in self.TAGS:
            self.response = "Unfortunately, the best way for me to give you feedback would be through conversation."
            return self.response
        else:
            self.response = "Sorry, could you please clarify."
            return self.response
    def respond_from_interview_decision(self,message,tags):
        return self.go_to_state('unknown_faculty')

    def on_enter_start_interview(self):
        self.count = 10
        response = "Good morning. I’m SIA, pleased to meet you. I’ll be interviewing you today."
        return response

    def on_enter_weaknesses(self):
        self.count = 10
        response = "What is a weakness that you have?"
        return response

    def on_enter_weakness_feedback(self):
        self.count = 11
        response = "(So, this is a tough one. You want to be honest about your answer,",
        "but you also want to pick a weakness that won’t hurt your chances of getting the position that you’re going for.)"
        return response

    def on_enter_challenge(self):
        self.count = 12
        response = "Describe a time you were struggling with a challenge. How did you overcome it and what did you learn?"
        return response

    def on_enter_challenge_feedback(self):
        self.count = 13
        response = "(One important thing to remember about this question is",
        " that you want to make sure that this challenge adds to your sense of",
        "person or adds to the interviewer’s perception of you. What does your ",
        "experience with this challenge and how you overcame it tell the interviewer",
        " about you?)"
        return response

    def on_enter_experience(self):
        self.count = 14
        response = "Do you have any work experience or extracurriculars?"
        return response

"""
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

    def finish_confused(self):
        """Send a message and go to the default state."""
        return "Sorry, I'm just a simple bot that can't understand much. You can ask me about office hours though!"

    def finish_location(self):
        """Send a message and go to the default state."""
        return f"{self.professor.capitalize()}'s office is in {self.get_office(self.professor)}"

    def finish_success(self):
        """Send a message and go to the default state."""
        return 'Great, let me know if you need anything else!'

    def finish_fail(self):
        """Send a message and go to the default state."""
        return "I've tried my best but I still don't understand. Maybe try asking other students?"

    def finish_thanks(self):
        """Send a message and go to the default state."""
        return "You're welcome!"


if __name__ == '__main__':
    OxyCSBot().chat()
