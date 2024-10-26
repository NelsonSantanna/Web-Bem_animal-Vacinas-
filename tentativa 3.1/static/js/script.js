// script.js
function showMessage() {
    alert('Cadastro concluído com sucesso!');
}

function showMessage() {
    $.ajax({
        url: '/register',  // URL da rota que você vai criar
        type: 'POST',
        data: { /* Dados do cadastro */ },
        success: function(response) {
            alert(response.message);  // Exibe a resposta do servidor
        },
        error: function(error) {
            alert('Erro ao cadastrar!');
        }
    });
}