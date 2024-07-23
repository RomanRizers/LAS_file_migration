
// Открываем модальное окно при нажатии на кнопку
document.getElementById('rename-table-button').addEventListener('click', function() {
    document.getElementById('rename-table-modal').style.display = 'block';
});
document.getElementsByClassName('close')[0].addEventListener('click', function() {
    document.getElementById('rename-table-modal').style.display = 'none';
});

window.onclick = function(event) {
    var modal = document.getElementById('rename-table-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};


 // JavaScript для подтверждения удаления таблицы
document.addEventListener("DOMContentLoaded", function() {
var deleteButtons = document.querySelectorAll(".delete-table-button");

    deleteButtons.forEach(function(button) {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            var confirmDelete = confirm("Вы уверены, что хотите удалить эту таблицу?");
            if (confirmDelete) {
                 var form = button.closest("form");
                 form.submit();
            }
        });
    });
});