"""
AIMLMarker class
Designed to work with the online DEWIS marking and feedback system
author james.smith@uwe.ac.uk
2024.
"""
from __future__ import annotations

import random
import re
import sys
from io import StringIO
from os.path import exists
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import aiml


class Capturing(list):
    def __enter__(self):
        self._stderr = sys.stderr
        sys.stderr = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stderr = self._stderr


class AIMLMarker:
    def __init__(
        self,
        question_file: str = "portfolio-questions-and-responses-2025.txt",
        num_questions: int = 45,
        context_question_ids=None,
    ):
        """Bland constructor.

        Parameter
        ---------
        question_file (str): name of text file holding sets of questions
                             and responses to be produced
                             default the 2025 questions
        num_questions (int): number of question-response pairs
                             default 45
        context_question_ids (int): list of indexes of the context-dependent questions
                            ( that need to be answered in context of previous question)
                            default: None but gets populated if default value for
                            question file is used
        """

        # declare some object variables and storage
        self.checkbot = None
        self.num_categories: int = 0
        self.score: int = 0
        self.feedback_str: str = ""
        self.ok_to_proceed: bool = True
        self.responses_file_name: str = ""
        self.feedback_file_name: str = ""
        self.questions: list = []
        self.responses: list = []
        self.order: list = []

        # details from parameters
        self.NUMQS: int = num_questions
        self.context_questions: list = context_question_ids
        self.question_file: str = question_file
        # can't specify default values for list param
        if self.question_file == "portfolio-questions-and-responses-2025.txt":
            self.context_questions = [35, 42, 44]

        # check parameters are valid
        if not exists(self.question_file):
            self.feedback_str += (
                f"ERROR: the question file called {self.question_file} "
                "is missing from this directory.\n"
                "You need to fix this problem before you can continue.\n"
            )
        if not isinstance(self.context_questions, list):
            self.feedback_str += "Error: context_questions should be a list of ints.\n"
        else:
            for idx in self.context_questions:
                if not isinstance(idx, int):
                    self.feedback_str += (
                        f"Error: non-integer context question index found {idx}.\n"
                    )
                else:
                    if idx < 0 or idx >= self.NUMQS:
                        self.feedback_str = (
                            f"Error passed invalid index {idx} "
                            f"outside the range 0-{self.NUMQS-1}"
                        )
        print(self.feedback_str)

    def syntax_check_aiml(self, aiml_filename: str = "student.aiml"):
        """Loads the student's aiml file and checks it parses ok.

        Parameters
        ----------
        aiml_filename(str) : name of file to read aiml from
        """

        if not exists(aiml_filename):
            self.feedback_str += (
                f"====> ERROR - there is no file in this directory "
                f"with the name {aiml_filename}.\n"
                "=====> Fix this problem before you continue.\n"
            )
            self.ok_to_proceed = False

        if self.ok_to_proceed:  # parse the student aiml
            parser = make_parser()
            parser.setContentHandler(ContentHandler())

            try:
                parser.parse(aiml_filename)
                self.feedback_str += (
                    f"AIML file {aiml_filename} passes basic xml syntax checks.\n"
                )
            except Exception as e:
                self.feedback_str += (
                    f"AIMLfile {aiml_filename} FAILS basic xml syntax checks.\n"
                    "This message gives you further details of the "
                    f" including the line number where the problem occurred\n{e}\n"
                    "HINT: Usually this occurs when you forget to close a tag-pair"
                    " a line or so earlier in your file"
                )
                with open(aiml_filename) as f:
                    lines = f.read()
                self.feedback_str += "here it is:\nxxxxxx"
                self.feedback_str += lines
                self.feedback_str += ":xxxxxxxxx"

                self.ok_to_proceed = False

        if self.ok_to_proceed:  # update names of outputs
            self.feedback_str += "Passed aiml-specific syntax check.\n"
            try:
                self.responses_file_name = aiml_filename[:-5] + "-responses.txt"
                self.feedback_file_name = aiml_filename[:-5] + "-feedback.txt"
            except NameError as err:
                self.feedback_str += f"ERROR: Got error {err} creating output files. \n"
                self.ok_to_proceed = False

    def feedback_markers_aiml(self, aiml_filename: str = "student.aiml") -> dict:
        """Reads students aiml file look for factors that affect feedback.

        Parameters:
        -----------
        aiml_filename(str): name of file with student's aiml in
        """
        student_lines = []
        with open(aiml_filename) as file:
            student_lines = [line.rstrip() for line in file]

        usage: dict = {
            "<srai": 0,
            "<set": 0,
            "*": 0,
            "_": 0,
            "^": 0,
            "#": 0,
            "<star": 0,
            "<that": 0,
            "<condition": 0,
            "duplicates": 0,
        }
        # check for language constructs
        for line in student_lines:
            for key in usage.keys():
                if key in line:
                    usage[key] += 1
        usage["wildcard"] = usage["*"] + usage["_"] + usage["^"] + usage["#"]

        # check whether information has been duplicated
        repeats = [0] * self.NUMQS
        for line in student_lines:
            for q in range(self.NUMQS):
                answer = self.responses[q]
                if answer in line:
                    repeats[q] += 1

        other_duplicates = [11, 28]
        for i in range(self.NUMQS):
            if (
                repeats[i] < 2
                or i + 1 in self.context_questions
                or i in other_duplicates
            ):
                pass
            else:
                usage["duplicates"] += 1

        return usage

    def load_questions(self):
        """Loads questions and desired responses from file."""
        if not exists(self.question_file):
            self.feedback_str += (
                f"ERROR: the question file called {self.question_file} "
                "is missing from this directory.\n"
                "You need to fix this problem before you can continue.\n"
            )
            self.ok_to_proceed = False

        if self.ok_to_proceed:
            # read the questions and answers in
            # Using readline()
            with open(self.question_file) as q_file:
                this_q = 0
                errstr = ""
                while True:
                    # Get next line from file
                    line = q_file.readline()
                    if not line:
                        errstr += "unexpected end of file reading question file.\n"
                        break
                    # should be a question
                    elif line[0] != "Q":
                        errstr += "didn't get expected question marker Q.\n"
                        break
                    elif int(line[1:3]) != this_q:
                        errstr += "question had wrong number.\n"
                        break
                    else:
                        self.questions.append(line[5:-1])

                    line = (
                        q_file.readline()
                    )  # next line should be the corresponding answer
                    if not line:
                        errstr += "unexpected end of file.\n"
                        break
                    elif line[0] != "A":
                        errstr += "didn't get expected answer marker A.\n"
                        break
                    elif int(line[1:3]) != this_q:
                        errstr += "answer had wrong number.\n"
                        break
                    else:
                        self.responses.append(line[5:-1])
                    this_q += 1
                    # then read the empty line separating QnA paits
                    line = q_file.readline()

                    # if line is empty
                    # end of file is reached
                    if not line:
                        break

            # check file was read correctly
            if errstr != "":
                self.feedback_str + errstr
                print(f"Error reading question file {errstr}- cannot proceed.\n")
                self.ok_to_proceed = False

            # make a shuffled order to ask them in
            if this_q > 0 and self.ok_to_proceed:
                # shuffle the order of the questions
                # except the **three** context-dependent ones
                toremove = []
                for idx in self.context_questions:
                    toremove.append(idx - 1)
                    toremove.append(idx)
                # print(toremove)
                # make a shuffled list with the numbers 1...NUMQs except the ones above in
                for i in range(self.NUMQS):
                    if i not in toremove:
                        self.order.append(i)
                random.shuffle(self.order)

                # put the context dependent Qs and precursors back in at the end
                for q in toremove:
                    self.order.append(q)

                for i in range(self.NUMQS):
                    if i not in self.order:
                        errstr += (
                            f"question {i} is missing after shuffling the order.\n"
                        )

                # check that there are the right number
                if this_q < self.NUMQS:
                    errstr += f"ERROR, only {this_q} question-answer pairs read.\n"
                elif (
                    len(self.questions) < self.NUMQS or len(self.responses) < self.NUMQS
                ):
                    errstr += "ERROR, somehow not all questions & responses have been saved.\n"
                if errstr == "":
                    self.feedback_str += (
                        f"{this_q} question-response pairs read for testing your bot.\n"
                    )
                else:
                    self.feedback_str += errstr
                    self.ok_to_proceed = False

    def makebot(self):
        """Makes the chatbot with an empty brain."""
        self.checkBot = aiml.Kernel()
        self.checkBot.verbose(True)

    def preprocess_single_input(self, the_input: str):
        # run the input through the 'normal' subber- only wortks for a single sentence
        subbed1 = self.checkBot._subbers["normal"].sub(the_input).upper()
        subbed2 = re.sub(self.checkBot._brain._puncStripRE, " ", subbed1)
        return subbed2

    def __check_and_store_responses(self) -> tuple[int, int, int]:
        """Ask the questions, check and store the responses.

        Returns:
        --------
        number of correct answers (int)
        number of context-dependent questions correctly answered (int)
        number of questions for which no matching category found(int)
        """

        # initialise score
        num_correct = 0
        num_contextqs_correct = 0
        num_no_match = 0

        if not isinstance(self.checkBot, aiml.Kernel):
            self.feedback_str += (
                "Error __check_and_store_responses() called before bot initialised.\n"
            )
            self.ok_to_proceed = False
            return 0, 0, 0

        with open(self.responses_file_name, "w") as responses_file:
            for q in range(self.NUMQS):
                thisq = self.order[q]
                # get bot's response to question
                bot_response = self.checkBot.respond(self.questions[thisq])
                if bot_response == "":
                    num_no_match += 1
                responses_file.write(f"Q{thisq:2d}: {self.questions[thisq]}\n")
                responses_file.write(f"Expected response: {self.responses[thisq]}\n")
                responses_file.write(f"Your bot response: {bot_response}\n")
                # check if it matches the required input
                if bot_response == self.responses[thisq]:
                    responses_file.write("*** Question answered correctly\n\n")
                    num_correct += 1
                    if thisq in self.context_questions:
                        num_contextqs_correct += 1
                else:
                    responses_file.write("Question answered incorrectly\n\n")
                    debug_str = (
                        "\t The input gets preprocessed by your bot as :\n"
                        f"\t{self.preprocess_single_input(self.questions[thisq])}"
                    )
                    if q > 0:
                        debug_str += (
                            "\t value for the <that> variable "
                            "which might affect matches is:"
                            f'\t{self.checkBot.getPredicate("_outputHistory")[-2]}\n\n'
                        )
                    responses_file.write(debug_str)
            # write final line to log file and exit
            responses_file.write(
                f" In total you got {num_correct} questions correct.\n"
            )
        return num_correct, num_contextqs_correct, num_no_match

    def strip_rubbish(self, aiml_filename: str):
        """Strips out junk inserted before the aiml header tag."""
        tag = "<aiml>"
        lines_to_write = []
        tag_found = False

        with open(aiml_filename, encoding="utf8") as in_file:
            for line in in_file:
                if line.strip() == tag:
                    tag_found = True
                if tag_found:
                    lines_to_write.append(line)
        with open(aiml_filename, "w", encoding="utf8") as out_file:
            out_file.writelines(lines_to_write)

    def test_aiml(self, aiml_filename: str = "student.aiml"):
        """The main test method.

        Parameters:
        -----------
        aiml_file_name (str): name of file containing student's knowledge base
            default is student.aiml
        """
        self.strip_rubbish(aiml_filename)
        self.syntax_check_aiml(aiml_filename)
        if not self.ok_to_proceed:
            print(self.feedback_str)
            print(
                "Fix this problem then re-run the AIMLMarker object's test_aiml method.\n"
            )
            return

        # ok so far
        if self.checkbot is None:
            self.makebot()
        self.checkBot.resetBrain()

        # learn aiml from file with reporting
        with Capturing() as output:
            self.checkBot.learn(aiml_filename)
            self.num_categories = self.checkBot.numCategories()
        if output or self.num_categories == 0:
            for message in output:
                self.feedback_str += (
                    f"ERROR: AIML-specific syntax problem: {message}\n"
                    "Usually this occurs if a category does not "
                    "have exactly one pattern and template.\n"
                )
            self.feedback_str += "Empty or broken aiml file, unable to proceed.\n"
            self.ok_to_proceed = False
            return

        self.feedback_str += (
            f"After reading your file the bot has {self.num_categories} categories.\n"
        )

        language_usage = self.feedback_markers_aiml(aiml_filename)

        # At last - see how the bot answers
        correct, context_correct, no_match = self.__check_and_store_responses()

        # calculate final score
        self.score = correct
        if correct < self.NUMQS:
            self.feedback_str += (
                f"Your bot answered {self.NUMQS-correct} questions incorrectly.\n"
                f"File {self.responses_file_name} has more details of your bots responses.\n"
                "Common mistakes are typos or extra spaces.\n"
            )
            if no_match > 0:
                self.feedback_str += (
                    f"For {no_match} questions "
                    "your bot did not have a matching category.\n"
                )
            context_errors = len(self.context_questions) - context_correct
            if context_errors > 0:
                self.feedback_str += (
                    f"Your bot answered incorrectly for {context_errors} questions "
                    "that require a sense of context.\n"
                    "To answer these you will need to use "
                    "<that> tag pairs in your categories, "
                    "or to access the value held in the bot's <that/> "
                    "variable (predicate).\n"
                )

        # if all questions correct then we start rewarding go solutions
        if correct == self.NUMQS:
            if self.num_categories < 10:
                self.score = 100
                self.feedback_str += (
                    "Congratulations,you score 100 "
                    "because you have beaten Jim's attempt!\n"
                )
            elif self.num_categories == 10:
                self.score = 90
                self.feedback_str += (
                    "Congratulations, you score 90 "
                    "because you have matched Jim's attempt!\n"
                )
            else:
                self.score = 90 - self.num_categories
                self.feedback_str += (
                    f"You score {self.score} "
                    "because your bot answered every question correctly "
                    f"using {self.num_categories} categories.\n"
                )
                # Add conditional feedback
                if language_usage["<srai"] == 0:
                    self.feedback_str += (
                        "You can improve your score by generalising "
                        "using <srai> tag pairs.\n"
                    )
                if language_usage["wildcard"] == 0:
                    self.feedback_str += (
                        "You can improve your score by using wildcards "
                        "such as * or _ in your patterns.\n"
                    )
                if language_usage["<star"] == 0:
                    self.feedback_str += (
                        "You can improve your score by using <star> "
                        "tag pairs or the shortcut  <star/>"
                        " in category templates to retrieve values matched by wildcards.\n"
                    )
                if language_usage["<set"] == 0:
                    self.feedback_str += (
                        "You can improve your score by using "
                        "<set> tag pairs to creating variables "
                        "so you can store what the conversation is talking about.\n"
                    )
                if language_usage["<that"] == 0:
                    self.feedback_str += (
                        "You can improve your score by using <that> tag pairs to "
                        "recall the bot's previous responses,  "
                        "which tells you what the conversation was about.\n"
                    )
                if language_usage["<condition"] == 0:
                    self.feedback_str += (
                        "You can improve your score by using <condition> and "
                        "<get>tag pairs "
                        "within a category's template to change the bot's response "
                        "depending on values your (or the bot) have stored in variables.\n"
                    )

        # penalise duplicates
        if language_usage["duplicates"] > 1:
            self.score = min(self.score, 65)
            self.feedback_str += (
                "Your knowledge base duplicated information (answers), "
                "so you mark is restricted to a maximum of 65.\n"
            )

        with open(self.feedback_file_name, "w") as feedback_file:
            feedback_file.write(self.feedback_str)

    def results_onscreen(self):
        """Displays results on screen."""
        print(f"The score is {self.score}.\n")
        print(
            f" Question-by-question details are stored in {self.responses_file_name}.\n"
        )
        print(
            f"The feedback is stored in {self.feedback_file_name} "
            "and here it is for quick reference:\n"
        )
        with open(self.feedback_file_name) as f:
            for line in f:
                print(line)
