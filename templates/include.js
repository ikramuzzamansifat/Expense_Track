// Fetch the content of the child.html file
fetch('base.html')
    .then(response => response.text())
    .then(data => {
        // Insert the content into the 'content' div of the base.html file
        document.getElementById('content').innerHTML = data;
    })
    .catch(error => {
        console.error(error);
    });
