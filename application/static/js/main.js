console.log('Я молодец, я загрузил страницу!')

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