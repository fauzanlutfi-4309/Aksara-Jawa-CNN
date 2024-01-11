
function previewImage(input) {
    var preview = document.getElementById('uploadedImage');
    var imageSection = document.querySelector('.image-section');

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            imageSection.style.display = 'block';
        };

        reader.readAsDataURL(input.files[0]);
    } else {
        preview.src = '';
        imageSection.style.display = 'none';
    }
}

function validateForm() {
    var fileInput = document.getElementById('imageUpload');
    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        alert('Pilih gambar terlebih dahulu.');
        return false;
    }
    return true;
}
