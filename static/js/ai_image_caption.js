const preview = document.getElementById('preview');
const input = document.getElementById('imageInput');
const loader = document.getElementById('loader');

input.onchange = e => {
    const file = e.target.files[0];
    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    }
};

async function uploadImage() {
    const file = input.files[0];
    if (!file) {
        alert("Please upload an image first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    loader.style.display = "block"; 
    document.getElementById('caption').textContent = "-";
    document.getElementById('tags').textContent = "-";

    try {
        const response = await fetch("http://127.0.0.1:8000/upload_image", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        document.getElementById('caption').textContent = data.caption;
        document.getElementById('tags').textContent = data.tags.join(", ");
    } catch (err) {
        alert("Something went wrong while uploading the image!");
        console.error(err);
    } finally {
        loader.style.display = "none"; 
    }
}