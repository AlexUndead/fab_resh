from django import template

register = template.Library()


@register.simple_tag
def draw_survey_result(parser, token):
    try:
        tag_name, result = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Не передан массив с результатами опроса")
    return AnswerNodeObject(result)


class AnswerNodeObject(template.Node):
    """Шаблон отображения результатов опроса"""
    def __init__(self, result):
        self.result = template.Variable(result)

    def get_survey_result_template(self, result):
        full_template = ''

        for answer_result_id in result:
            template = f"""
                <div class="question card mb-4 shadow-sm">
                    <div class="card-header">{result[answer_result_id]['question']}</div>
                    <div class="card-body">
                    """ + \
                       self.get_answer_template(result[answer_result_id]) \
                       + """
                    </div>
                </div>
                    """

            full_template += template

        return full_template

    def get_answer_template(self, answer_result):
        template = {
            'success': """
                <div class="alert alert-success" role="alert">{}</div>
            """,
            'error': """
                <div class="alert alert-danger" role="alert">{}</div>
            """,
            'open': """
                <div class="alert alert-warning" role="alert">{}</div>
            """
        }

        if answer_result['type'] == 1:
            answer_template = template['open'].format(answer_result['value'])
        elif answer_result['correctly']:
            answer_template = template['success'].format(str(answer_result['value']))
        else:
            answer_template = template['error'].format(str(answer_result['value'])) + \
                              template['success'].format(str(answer_result['correct_answer']))

        return answer_template


    def render(self, context):
        resolve_result = self.result.resolve(context)

        return self.get_survey_result_template(resolve_result)


register.tag('draw_survey_result', draw_survey_result)
