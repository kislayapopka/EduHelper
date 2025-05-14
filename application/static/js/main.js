document.addEventListener('DOMContentLoaded', function() {
    const mainDateInput = document.getElementById('post_due_date');
    if (mainDateInput) {
        const td = new tempusDominus.TempusDominus(mainDateInput, {
            display: {
                components: {
                    decades: false,
                    year: true,
                    month: true,
                    date: true,
                    hours: true,
                    minutes: true,
                    seconds: false
                },
                buttons: {
                    today: true,
                    clear: true,
                    close: true
                },
                theme: 'light'
            },
            localization: {
                locale: 'ru',
                format: 'dd.MM.yyyy HH:mm',
                startOfTheWeek: 1
            }
        });

        console.log('TempusDominus инициализирован:', td);
        mainDateInput.addEventListener('click', () => console.log('Поле даты кликнуто'));
    }
});

document.addEventListener('DOMContentLoaded', function() {
        const infoCheckbox = document.getElementById('post_is_info');
        if (!infoCheckbox) {
            console.error('Чекбокс с ID "post_is_info" не найден!');
            return;
        }
        const fieldsToToggle = [
            {id: 'post_due_date', type: 'input'},
            {id: 'post_attached_files', type: 'input'},
            {selector: 'label[for="post_due_date"]'},
            {selector: 'label[for="post_attached_files"]'},
            {id: 'file_help_text', type: 'text'}
        ];
        const elements = fieldsToToggle.map(item => {
            if (item.id) {
                const el = document.getElementById(item.id);
                if (!el) console.error(`Элемент с ID "${item.id}" не найден!`);
                return el;
            }
            if (item.selector) {
                const el = document.querySelector(item.selector);
                if (!el) console.error(`Элемент с селектором "${item.selector}" не найден!`);
                return el;
            }
            return null;
        }).filter(el => el !== null);

        function toggleFields() {
            const isInfo = infoCheckbox.checked;
            console.log('Переключение состояния. Инфо-пост:', isInfo);
            elements.forEach(element => {
                const formGroup = element.closest('.form-group');
                if (!formGroup) {
                    console.warn('Элемент не находится внутри .form-group:', element);
                    return;
                }

                formGroup.style.display = isInfo ? 'none' : 'block';

                const inputs = formGroup.querySelectorAll('input, textarea, select');
                inputs.forEach(input => {
                    input.disabled = isInfo;
                    console.log(`Состояние элемента ${input.id}: ${input.disabled ? 'disabled' : 'enabled'}`);
                });
            });
        }

        toggleFields();
        infoCheckbox.addEventListener('change', toggleFields);
    });