function showCustomAlert(message) {
            var alertContent = document.getElementById('alertContent');
            alertContent.innerText = message;
            var customOverlay = document.getElementById('customOverlay');
            var customAlert = document.getElementById('customAlert');
            customOverlay.style.display = 'block';
            customAlert.style.display = 'block';
        }

        function hideCustomAlert() {
            var customOverlay = document.getElementById('customOverlay');
            var customAlert = document.getElementById('customAlert');
            customOverlay.style.display = 'none';
            customAlert.style.display = 'none';
        }

        document.getElementById('uploadForm').addEventListener('submit', function(event) {
            event.preventDefault();
            var form = this;
            var formData = new FormData(form);
            fetch(form.action, {
                method: form.method,
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showCustomAlert('Данные успешно загружены и добавлены в базу данных!');
                } else {
                    showCustomAlert('Произошла ошибка при загрузке данных в базу данных!');
                }
            })
            .catch(error => {
                console.error('Произошла ошибка:', error);
                showCustomAlert('Произошла ошибка при отправке запроса на сервер!');
            });
        });