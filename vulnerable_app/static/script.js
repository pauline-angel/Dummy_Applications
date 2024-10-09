// Expose sensitive information in JavaScript file
var config = {
    apiKey: "12345-ABCDE",
    secretToken: "token123",
    password: "password123",
    phone: "123",
    phoneno: "97823764582",
    email: "test@yopmail.com",
    session: "ejhrwbfkeuwgwbii13u38923bc873278vbe8b82ciu238bv23"
};

console.log("API Key:", config.apiKey);
console.log("Secret Token:", config.secretToken);
console.log("Password:",config.password);
console.log("Phone:",config.phone);
console.log("Phonenumber:",config.phoneno);
console.log("Email:",config.email);
console.log("Session ID:",config.session);

// Potential DOM-based XSS vulnerability
function showAlert() {
    var userInput = prompt("Enter some text:");
    if (userInput) {
        document.getElementById("userInput").innerHTML = "You entered: " + userInput;
    }
}
