from rest_framework.serializers import ChoiceField


class LabelChoiceField(ChoiceField):
    '''поля выбора, которое работает с лейблами'''
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)
