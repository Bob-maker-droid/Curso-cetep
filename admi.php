<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $texto = $_POST['textoCurso'];

    // Salva em um arquivo txt
    file_put_contents("curso_info.txt", $texto);

    // Redireciona de volta para o painel com status
    header("Location: admin.html?status=ok");
    exit();
}
?>
