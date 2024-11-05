const username = document.getElementById("namebox").value;
const password = document.getElementById("passbox").value;
const btn = document.getElementById("continue");

btn.addEventListener("click", async function() {
    console.log("username: " + username + " password: " + password)

    let re = /\w+\d+\W+/
    if (!(re.test(password))) {
        window.alert("Password is invalid! Must include at least a character, a digit, and a special character");
    }

    
})