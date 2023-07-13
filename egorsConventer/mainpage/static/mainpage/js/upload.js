document.getElementById('upload-button').addEventListener('click', function(e) {
  e.preventDefault();  // Отменяет действие по умолчанию, чтобы не переходить по ссылке

  // Создает элемент input типа file для выбора файла
  var input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';  // Ограничивает выбор только изображений

  // Открывает панель выбора файла
  input.click();

  // Обрабатывает событие выбора файла
  input.addEventListener('change', function() {
    var file = input.files[0];  // Получает выбранный файл

    // Создает объект FormData для отправки файла на сервер
    var formData = new FormData();
    formData.append('image', file);

    // Отправляет файл на сервер с помощью AJAX-запроса
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload/', true);  // Замените '/upload/' на URL-адрес вашего представления для загрузки файла
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');  // Подставьте CSRF-токен Django
    xhr.onload = function() {
      if (xhr.status === 200) {
        // Обновляет страницу после успешной загрузки файла
        location.reload();
      }
    };
    xhr.send(formData);
  });
});