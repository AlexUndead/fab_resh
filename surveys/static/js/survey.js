function Survey(survey){
    this.survey = survey;
    this.questions = survey.find('.question');
    this.surveyErrors = {};
    this.getCSRFTokenValue = function(){
        /*Получение значения CSRF Token*/
        return $('input[name="csrfmiddlewaretoken"]').val()
    };
    this.surveyResult = {
    };
    this.textareaValidator = function(question){
        /*Валидатор вопросов с открытым ответом*/
        var textareaValue = question.find("textarea").val();

        if(!textareaValue){
            this.surveyErrors[question.attr('id')] = 'Введите свой вариант ответа';
        } else {
            this.surveyResult[question.attr('id')] = textareaValue;
        }
    };
    this.radioValidator = function(question){
        /*Валидатор вопроса с единственным ответом*/
        var checkedRadio = question.find("input[type='radio']:checked");

        if(!checkedRadio.length){
            this.surveyErrors[question.attr('id')] = 'Нужно выбрать хотя-бы один варинат ответа';
        } else {
            this.surveyResult[question.attr('id')] = checkedRadio.siblings('label').text();
        }
    };
    this.checkboxValidator = function(question){
        /*Валидатор вопроса с множетвенным ответом*/
        var checkedCheckboxes = question.find("input[type='checkbox']:checked");
        if(!checkedCheckboxes.length){
            this.surveyErrors[question.attr('id')] = 'Нужно выбрать хотя-бы один варинат ответа';
        } else {
            var checkboxValues = []

            checkedCheckboxes.each(function(){
                var checkbox = $(this)
                var checkboxValue = checkbox.siblings('label').text()

                checkboxValues.push(checkboxValue);
            })

            this.surveyResult[question.attr('id')] = checkboxValues;
        }
    };
    this.validators = {
        1:this.textareaValidator,
        2:this.radioValidator,
        3:this.checkboxValidator,
    };
    this.removeErrors = function(){
        /*Удаление всех ошибок в полях*/
        $('.card-footer').remove()
    }
    this.renderErrors = function(){
        /*Отображение всех ошибок в полях*/
        for(idQuestion in this.surveyErrors){
            var questionWithError = $('#'+idQuestion)
            var errorCardBody = questionWithError.find('.card-body')
            var errorCardFooter = questionWithError.find('.card-footer')

            if(!errorCardFooter.length){
                errorCardBody.after('<div class="card-footer border-danger text-danger">' + this.surveyErrors[idQuestion] + '</div>')
            }
        }
    }
    this.runValidation = function(){
        /*Запуск функции валидатора зависящую от типа вопроса*/
        var surveySelf = this;

        this.removeErrors();
        this.questions.each(function(){
            var question = $(this)
            var questionType = question.data('question-type')
            var validator = surveySelf.validators[questionType].bind(surveySelf)

            validator(question);
        })
    }
    this.isValid = function(){
        /*Проверка наличие ошибок*/
        this.runValidation()

        return this.errorsIsEmpty(this.surveyErrors) ? true : false
    }
    this.errorsIsEmpty = function(){
        /*Проверка объекта ошибок на пустоту*/
        return JSON.stringify(this.surveyErrors) == '{}';
    }
    this.send = function(){
        /*Отправка данных по опросу*/
        $.ajax({
            url: '/surveys/result/save/',
            type: 'POST',
            headers: {"X-CSRFToken": this.getCSRFTokenValue()},
            data: JSON.stringify({'result': this.surveyResult}),
            success: function(){
                console.log('success');
            },
            dataType: 'json',
            contentType: 'application/json',
        })
    }
}

$(document).ready(function(){
    $('#survey').submit(function(){
        var survey = new Survey($(this));

        (survey.isValid()) ? survey.send() : survey.renderErrors();
        event.preventDefault();
    })
});

