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

document.getElementById('newPostForm').addEventListener('submit',
    function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/create_assignment', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/assignments'; // Перенаправление на страницу заданий
        } else {
            alert('Ошибка при создании задания...');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке данных');
    });
});
