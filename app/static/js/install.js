document.addEventListener('DOMContentLoaded', () => {
    const checkButton = document.getElementById('check-button');
    const installButton = document.querySelector('button[type="submit"]');
    const form = document.getElementById('install-form');

    installButton.disabled = true;
    installButton.style.backgroundColor = '#696969';

    let dbHost, dbUser, dbPassword, dbName, dbPort, dbPrefix;

    checkButton.addEventListener('click', () => {
        dbHost = document.getElementById('db_host').value.trim();
        dbUser = document.getElementById('db_user').value.trim();
        dbPassword = document.getElementById('db_password').value.trim();
        dbName = document.getElementById('db_name').value.trim();
        dbPort = document.getElementById('db_port').value.trim();
        dbPrefix = document.getElementById('db_prefix').value.trim();
        
        if (!dbHost || !dbUser || !dbPassword || !dbName || !dbPort) {
            showToast('Заполните поля для подключения к базе данных!', 'error');
            return;
        }

        if (isNaN(dbPort) || dbPort <= 0) {
            showToast('Неверный формат для поля порт!', 'error');
            return;
        }

        fetch('/check_db_connection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                db_host: dbHost,
                db_user: dbUser,
                db_password: dbPassword,
                db_name: dbName,
                db_port: dbPort,
                db_prefix: dbPrefix
            }),
        })
        .then(response => {
            if (response.ok) {
                installButton.disabled = false; 
                installButton.style.backgroundColor = '';
                showToast('Подключение к базе данных успешно!', 'success');
            } else {
                return response.json().then(data => {
                    installButton.disabled = true; 
                    installButton.style.backgroundColor = '#cccccc';
                    showToast(data.detail || 'Не удалось подключиться к базе данных!', 'error');
                });
            }
        })
        .catch(error => {
            installButton.disabled = true; 
            installButton.style.backgroundColor = '#cccccc';
            showToast('Произошла ошибка при проверке подключения!', 'error');
        });
    });

    installButton.addEventListener('click', (event) => {
        event.preventDefault(); 

        const steamApiKey = document.getElementById('steam_api_key').value.trim();
        const steamAdmin = document.getElementById('steam_64_general_admin').value.trim();

        if (!steamApiKey || !steamAdmin) {
            showToast('Заполните поля Steam!', 'error');
            return;
        }

        const formData = {
            steam_api_key: steamApiKey,
            steam_64_general_admin: steamAdmin,
            db_host: dbHost,
            db_user: dbUser,
            db_password: dbPassword,
            db_name: dbName,
            db_port: dbPort,
            db_prefix: dbPrefix
        };

        fetch('/go_install', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => {
            if (response.ok) {
                showToast('Установка прошла успешно!', 'success');
            } else {
                return response.json().then(data => {
                    showToast(data.detail || 'Ошибка при установке!', 'error');
                });
            }
        })
        .catch(error => {
            showToast('Произошла ошибка при установке!', 'error');
        });
    });
});
