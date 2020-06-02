from .models import Answer, Question


class SurveyValidator:
    """Класс для проверки результатов прохождения опроса|Обязательно переписать!!!"""
    def __init__(self, customer_result):
        self.customer_result = customer_result

    def get_validator(self, question_id):
        validators = {
            1: self.open_answer_validator,
            2: self.single_answer_validator,
            3: self.multiple_answer_validator,
        }

        return validators[question_id]

    def get_correct_answers(self, question_id):
        answer_correct_type_id = 2
        return Answer.objects.select_related('question').filter(
            type=answer_correct_type_id,
            question_id__in=question_id,
        )

    def open_answer_validator(self, correct_answers, customer_question_id, customer_answer):
        customer_answer['question'] = Question.objects.get(id=customer_question_id).text
        customer_answer['correctly'] = None

    def single_answer_validator(self, correct_answers, customer_question_id, customer_answer):
        correct_answer = correct_answers.filter(question_id=customer_question_id).first()
        correct_answer_text = correct_answer.text
        correctly = True if correct_answer_text == customer_answer['value'] else False
        customer_answer['question'] = correct_answer.question.text
        customer_answer['correctly'] = correctly
        customer_answer['correct_answer'] = correct_answer_text

    def multiple_answer_validator(self, correct_answers, customer_question_id, customer_answer):
        correct_answer = correct_answers.filter(question_id=customer_question_id)
        correct_answer_set = {answer.text for answer in correct_answer}
        correctly = True if correct_answer_set == set(customer_answer['value']) else False
        customer_answer['question'] = correct_answer.first().question.text
        customer_answer['correctly'] = correctly
        customer_answer['correct_answer'] = correct_answer_set

    def validation(self):
        correct_answers = self.get_correct_answers(self.customer_result.keys())
        for customer_answer in self.customer_result:
            validator = self.get_validator(self.customer_result[customer_answer]['type'])
            validator(correct_answers, customer_answer, self.customer_result[customer_answer])

        return self.customer_result


