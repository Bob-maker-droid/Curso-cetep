
function irParaSelecao() {
  window.location.href = "Teladeseleção.html"; 
}


function saveChanges() {
    const selectedCourse = document.getElementById('course-select').value;
    const editableElements = document.querySelectorAll('.editable');
    const content = [];

    editableElements.forEach(el => {
        content.push(el.innerHTML);
    });

    localStorage.setItem(`courseContent-${selectedCourse}`, JSON.stringify(content));
    alert(`Alterações para o curso de ${selectedCourse} salvas com sucesso!`);
}

function loadEditorContent() {
    const selectedCourse = document.getElementById('course-select').value;
    const editableElements = document.querySelectorAll('.editable');
    const savedContent = localStorage.getItem(`courseContent-${selectedCourse}`);

    if (savedContent) {
        const content = JSON.parse(savedContent);
        editableElements.forEach((el, i) => {
            el.innerHTML = content[i] || "";
        });
    } else {
        // Conteúdo padrão
        const defaultContent = [
            "Título do Curso",
            "Descrição do curso...",
            "Horários",
            "Adicione as informações sobre os horários aqui.",
            "Contatos",
            "Adicione as informações de contato aqui."
        ];
        editableElements.forEach((el, i) => {
            el.innerHTML = defaultContent[i] || "";
        });
    }
}

// Função para atualizar a página pública (se tiver)
function loadCourseContent(courseName) {
    const savedContent = localStorage.getItem(`courseContent-${courseName}`);
    if (!savedContent) return;

    const content = JSON.parse(savedContent);
    const ids = [
        'course-title',
        'course-description',
        'schedule-section-title',
        'schedule-section-text',
        'contact-section-title',
        'contact-section-text'
    ];

    ids.forEach((id, i) => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = content[i] || "";
    });
}
