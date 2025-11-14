$db = new PDO('sqlite:banco.db')
$db->exec("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT, email TEXT UNIQUE, senha TEXT)");

$nome = $_POST['nome'];
$email = $_POST['email'];
$senha = password_hash($_POST['senha'], PASSWORD_DEFAULT);

$stmt = $db->prepare("INSERT INDO usuarios (nome, email, senha) VALUES (?,?,?)");
$result = $stmt->execute([$nome, $email, $senha]);

if ($result) {
    echo "usuarios registrado com sucesso!";
}
else {
    echo "Erro ao registrar: ".$stmt->errorInfo()[2];
}