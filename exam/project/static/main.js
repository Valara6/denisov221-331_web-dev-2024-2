const easyMDE = new EasyMDE({element: document.getElementById('description')});
function isImage(file) {
    return file.type.startsWith('image/')
}

document.getElementById('cover').onchange = function () {
    const file = this.files[0];
    if (isImage(file)) {
        let src = URL.createObjectURL(file);
        document.getElementById('image').src = src;
    } else {
        alert('Выбранный файл не является изображением.');
    }
};

document.querySelector('.previews').addEventListener('click', function() {
    console.log("зашел");
    document.getElementById('cover').click();
});

const dropzone = document.getElementById('dropzone');
const image = document.getElementById('image');

dropzone.addEventListener('dragover', function(event) {
    event.preventDefault();
});

dropzone.addEventListener('drop', function(event) {
    event.preventDefault();

    const files = event.dataTransfer.files;

    if (files.length === 0) return;

    const file = files[0];

    if (isImage(file)) {
        let inputfield = document.getElementById("cover").classList.remove("is-invalid")
        let msg = document.getElementById("msg-image").textContent = "           "
        const reader = new FileReader();

        reader.onload = function(event) {
            image.src = event.target.result;
        };

        reader.readAsDataURL(file);
    } else {
        let inputfield = document.getElementById("cover").classList.add("is-invalid")
        let msg = document.getElementById("msg-image").textContent = "Можно загрузить только изображении"
    }
});
