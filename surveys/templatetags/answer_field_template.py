from django import template

register = template.Library()


@register.simple_tag
def draw_answer(parser, token):
    try:
        tag_name, question_type, answer_id, answer_text = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Не переданы необходимые параметры: question_type, answer_id, answer_text")
    return AnswerNodeObject(question_type, answer_id, answer_text)


class AnswerNodeObject(template.Node):
    """Шаблон отображения ответов в опросе"""
    def __init__(self, question_type, answer_id, answer_text):
        self.question_type = template.Variable(question_type)
        self.answer_id = template.Variable(answer_id)
        self.answer_text = template.Variable(answer_text)

    def get_answer_field_template(self, question_type, answer_id, answer_text):
        template = {
            2: f"""
                <div class="custom-control custom-radio">
                    <input type="radio" id="{answer_id}" name="answer" class="custom-control-input">
                    <label class="custom-control-label" for="{answer_id}">{answer_text}</label>
                </div> 
            """,
            3: f"""
                <div class="custom-control custom-checkbox">
                    <input type="checkbox" class="custom-control-input" id="{answer_id}">
                    <label class="custom-control-label" for="{answer_id}">{answer_text}</label>
                </div>
            """
        }

        return template[question_type]

    def render(self, context):
        resolve_question_type = self.question_type.resolve(context)
        resolve_answer_id = self.answer_id.resolve(context)
        resolve_answer_text = self.answer_text.resolve(context)
        return self.get_answer_field_template(
            resolve_question_type,
            resolve_answer_id,
            resolve_answer_text
        )


register.tag('draw_answer', draw_answer)
