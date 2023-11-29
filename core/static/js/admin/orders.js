document.getElementById("id_status").addEventListener("change", (event) => {
    event.currentTarget.closest("form").submit()
})