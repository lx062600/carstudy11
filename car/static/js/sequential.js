
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault();

        var form = event.target;
        var answerInput = form.querySelector('input[name="answer"]:checked');

        if (!answerInput) {
            alert('请选择一个答案！');
            return;
        }

        console.log(answerInput.id);
        console.log(answerInput.dataset.answer);
        var selectedAnswerTitle = answerInput.id;
        var correctAnswer = answerInput.dataset.answer;

        var isCorrect = selectedAnswerTitle === correctAnswer;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');

        xhr.onload = function() {
            if (this.status === 200) {
                var response = JSON.parse(this.responseText);
                showFeedback(isCorrect, response.skill_explain, response.answer, response.next_url);
            } else {
                alert('提交答案时发生错误，请重试。');
            }
        };

        xhr.send(new URLSearchParams(new FormData(form)).toString());
    });

    function showFeedback(isCorrect, skillExplain, answerText, nextUrl) {
        var feedbackElement = document.getElementById('feedback');
        var skillExplainElement = document.getElementById('skillExplain');

        feedbackElement.innerHTML = '';
        skillExplainElement.innerHTML = '';

        var feedbackIcon = document.createElement('i');
        feedbackIcon.classList.add('fas');
        feedbackIcon.style.color = isCorrect ? 'green' : 'red';
        feedbackElement.appendChild(feedbackIcon);

        if (isCorrect) {
            feedbackIcon.classList.add('fa-check-circle');
            feedbackElement.textContent = ' 正确！';
            setTimeout(function() {
                window.location.href = nextUrl;
            }, 500);
        } else {
            feedbackIcon.classList.add('fa-times-circle');
            feedbackElement.textContent = ' 错误！';
            skillExplainElement.textContent = '正确答案是：' + answerText + '。' + skillExplain;
            skillExplainElement.style.display = 'block';
        }

        feedbackElement.style.display = 'block';
    }