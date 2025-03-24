document.addEventListener('DOMContentLoaded', function() {
    const dueDateField = document.getElementById('due_date');

    if (dueDateField) {
        new tempusDominus.TempusDominus(dueDateField, {
            localization: {
                locale: 'ru',
                format: 'yyyy-MM-dd HH:mm'
            },
            display: {
                components: {
                    decades: true,
                    year: true,
                    month: true,
                    date: true,
                    hours: true,
                    minutes: true,
                    seconds: false
                }
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    let currentSelectedCourseId = null;

    document.querySelector('.carousel').addEventListener('click', (event) => {
        const item = event.target.closest('.carousel-item');
        if (item) {
            currentSelectedCourseId = item.dataset.courseId;
            document.getElementById('course_id_input').value = currentSelectedCourseId;
            console.log('Выбран курс с ID:', currentSelectedCourseId);
        }
    });

    document.getElementById('newPostForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const submitButton = document.getElementById('submitButton');
        const loadingIndicator = document.getElementById('loadingIndicator');

        submitButton.style.display = 'none';
        loadingIndicator.style.display = 'block';

        const formData = new FormData(this);

        fetch('/create_assignment', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сервера');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert(data.message);
                window.location.reload();
            } else {
                alert(`Ошибка: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке данных');
        });
    });
});
