function loadElements(url, elemId) {
    fetch(url)
        .then(response => {
            let elem = document.getElementById(elemId);
            elem.innerHTML = response.json()
                .then(data => {
                    let elem = document.getElementById(elemId);
                    elem.innerHTML = JSON.stringify(data);
                });
        })
        .catch(error => console.log(error));
}

loadElements("/api/departments", "departments");
loadElements("/api/employees", "employees");