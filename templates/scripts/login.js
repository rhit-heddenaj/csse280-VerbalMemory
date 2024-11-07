
window.addEventListener("load", function() {
    document.getElementById('namebox').value = '';
    document.getElementById('passbox').value = '';
    document.getElementById('passbox2').value = '';
})

const btn = document.getElementById("continue");

btn.addEventListener("click",  function() {
    const username = document.getElementById("namebox").value;
    const password = document.getElementById("passbox").value;
    const pass2 = document.getElementById("passbox2").value;
    if (password != pass2) {
        window.alert("Passwords do not match!");
        return;
    }

    let re = /\w+\d+\W+/
    if (!(re.test(password))) {
        window.alert("Password is invalid! Must include at least a character, a digit, and a special character");
        return;
    }
})