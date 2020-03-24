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
        'yes_company',
        'no_company',
        'yes_position',
        'no_position',
        'transition_interview',
        'interview_yes',
        'interview_no',
        'interview_decision',
        'start_interview',
        'weaknesses',
        'weakness_feedback',
        'strength',
        'strength_feedback',
        'challenge',
        'challenge_feedback',
        'experience',
        'experience_feedback',
        'end_interview',
    ]

    TAGS = {
        # intent
        'help': 'hello',
        'hello': 'hello',
        'hey': 'hello',
        'hi': 'hello',
        'cool': 'introduction',
        'awesome': 'introduction',
        'interview': 'interview',
        'Yes':'transition_interview',
        'Sure':'transition_interview',

        # generic
        'thanks': 'thanks',
        'okay': 'success',
        'bye': 'success',
        'yes': 'yes',
        'yep': 'yes',
        'yeah': 'yes',
        'no': 'no',
        'nope': 'no',
        "I don't know": 'no',
        "I'm not sure": 'no',

        # positive
        'confident' : 'positive',
        'good' : 'positive',
        'great' : 'positive',
        'improve' : 'positive',
        'improved' : 'positive',
        'better' : 'positive',
        'awesome' : 'positive',

        # negative
        'negative' : 'negative',
        'bad' : 'negative',
        'nervous' : 'negative',
        'unhappy' : 'negative',
        'dumb' : 'negative',

    }

    YES = [
        'yes',
    ]

    NO = [
        'no',
    ]
    POSITIVE = [
        'positive',
    ]
    NEGATIVE = [
        'negative',
    ]

    PROFESSORS = [
        'yes',
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

    # "unknown_faculty" state functions
    def on_enter_introduction(self):
        return "Hi, I am SIA, your student interview assistant. I am here to help you work on your interviewing skills. What is your name?"
    def respond_from_introduction(self,message,tags):
        return self.go_to_state('save_name')#temp

    def on_enter_save_name(self):
        return "I look forward to working with you!"
    def respond_from_save_name(self,message,tags):
        return self.go_to_state('identify_company')

    def on_enter_identify_company(self):
        return "Is there a specific company you are planning to apply to, and if so, what is it?"
    def respond_from_identify_company(self,message,tags):
        for comp in self.NO:
            if comp in tags:
                self.note = note
                return self.go_to_state('yes_company')
        return self.go_to_state('no_company')

    def on_enter_yes_company(self):
        return  "Great! What position are you applying for?"
    def respond_from_yes_company(self,message,tags):
        return self.go_to_state('yes_position')

    def on_enter_no_company(self):
        return "That's alright! Is there a role you have in mind?"
    def respond_fom_no_company(self,message,tags):
        return self.go_to_state('yes_position')

    def on_enter_yes_position(self):
        return "Wow, that sounds like a great role!"
    def respond_from_yes_position(self, message, tags):
        return self.go_to_state('transition_interview')

    def on_enter_no_position(self):
        return "That's alright!"
    def respond_from_no_position(self, message, tags):
        return self.go_to_state('transition_interview')

    def on_enter_transition_interview(self):
        return "Would you like to start a casual mock interview? It would only take around five minutes. I’ll ask you some of the most common interview questions and give you a few pointers in parenthesis along the way."

    def respond_from_transition_interview(self,message,tags):
        for note in self.YES:
            if note in tags:
                self.note = note
                return self.go_to_state('interview_yes')
        return self.go_to_state('interview_no')

    def on_enter_interview_yes(self):
        return "Great, let’s begin! Remember, you should treat this as if it was a “real” interview, so be purposeful with your words. I’ll be right back, I’m gonna change into my suit and tie!"
    def respond_from_interview_yes(self, message, tags):
        return self.go_to_state('start_interview')

    def on_enter_interview_no(self):
        return "Unfortunately, the best way for me to give you feedback would be through conversation."
    def respond_from_interview_no(self,message,tags):
        return self.finish('fail')

    def on_enter_start_interview(self):
        return "Good morning. I’m SIA, pleased to meet you. I’ll be interviewing you today."
    def respond_from_start_interview(self,message,tags):
        return self.go_to_state('experience')

    def on_enter_experience(self):
        return "Do you have any work experience or extracurriculars?"
    def respond_from_experience(self,message,tags):
        return self.go_to_state('experience_feedback')

    def on_enter_experience_feedback(self):
        return "(When talking about your past experiences, make sure to reference specific positions and skills relevant to the position you are applying for. However, be honest with your answer. Any experience counts! If you have little to no paid work experience, include some valuable extracurriculars.)"
    def respond_from_experience_feedback(self,message,tags):
        return self.go_to_state('weaknesses')

    def on_enter_weaknesses(self):
        return "What is a weakness that you have?"
    def respond_from_weaknesses(self,message,tags):
        return self.go_to_state('weakness_feedback')

    def on_enter_weakness_feedback(self):
        return "(So, this is a tough one. You want to be honest about your answer, but you also want to pick a weakness that won’t hurt your chances of getting the position that you’re going for.)"
    def respond_from_weakness_feedback(self,message,tags):
        return self.go_to_state('strength')

    def on_enter_strength(self):
        return "What are some of your strengths?"
    def respond_from_strength(self,message,tags):
        return self.go_to_state('strength_feedback')

    def on_enter_strength_feedback(self): #x
        return "(Although all strengths are valuable, make sure that the strengths that you select are appropriate for the position you are applying to. It may help to use the job description or requirements to guide your answer for this question.)"
    def respond_from_strength_feedback(self,message,tags):
        return self.go_to_state('challenge')

    def on_enter_challenge(self):
        return "Describe a time you were struggling with a challenge. How did you overcome it and what did you learn?"
    def respond_from_challenge(self,message,tags):
        return self.go_to_state('challenge_feedback')

    def on_enter_challenge_feedback(self):
        return "(One important thing to remember about this question is that you want to make sure that this challenge adds to your sense of person or adds to the interviewer’s perception of you. What does your experience with this challenge and how you overcame it tell the interviewer about you?)"
    def respond_from_challenge_feedback(self,message,tags):
        return self.go_to_state('end_interview')

    def on_enter_end_interview(self):
        return "We’re finally done for today! It was nice chatting with you. How did you feel about the mock interview?"
    def respond_from_end_interview(self,message,tags):
        for pos in self.POSITIVE:
            if pos in tags:
                self.pos = pos
                return self.finish('positive')
        for neg in self.NEGATIVE:
            if neg in tags:
                self.neg = neg
                return self.finish('negative')
        return self.finish('neutral')


    # "finish" functions
    def finish_positive(self):
        return "Awesome! Glad I could help!"

    def finish_negative(self):
        return "Trust me it wasn’t that bad. Feel free to come back for more practice! See you!"

    def finish_neutral(self):
        return "Well, it was nice talking to you! I hope you were able to gain something from this."

    def finish_confused(self):
        """Send a message and go to the default state."""
        return "I'm sorry, I don't quite understand."

    def finish_fail(self):
        """Send a message and go to the default state."""
        return "I've tried my best but I still don't understand. Maybe try asking other students?"

    def finish_thanks(self):
        """Send a message and go to the default state."""
        return "You're welcome!"


if __name__ == '__main__':
    OxyCSBot().chat()
