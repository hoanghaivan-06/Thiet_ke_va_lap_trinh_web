// LAB 1: Working with an array of prediction samples

// 1. Create an array of prediction samples
const predictions = [
    { id: 1, name: "Nguyen Van A", result: 85 },
    { id: 2, name: "Tran Van B", result: 72 },
    { id: 3, name: "Le Van C", result: 91 },
    { id: 4, name: "Pham Van D", result: 65 },
    { id: 5, name: "Hoang Van E", result: 78 }
];


// 2. Filter the array by a condition using a for loop
// Find students whose result >= 80

const filteredPredictions = [];

for (let i = 0; i < predictions.length; i++) {
    if (predictions[i].result >= 80) {
        filteredPredictions.push(predictions[i]);
    }
}

console.log("Filtered predictions:");
console.log(filteredPredictions);


// 3. Function that sums the result field

function sumResults(predictions) {
    let sum = 0;

    for (let i = 0; i < predictions.length; i++) {
        sum += predictions[i].result;
    }

    return sum;
}

console.log("Total result:");
console.log(sumResults(predictions));


// 4. Function that finds the object with the largest result

function findLargestResult(predictions) {
    let largest = predictions[0];

    for (let i = 1; i < predictions.length; i++) {
        if (predictions[i].result > largest.result) {
            largest = predictions[i];
        }
    }

    return largest;
}

console.log("Prediction with the largest result:");
console.log(findLargestResult(predictions));


// 5. Convert the sum function to an arrow function

const sumResultsArrow = (predictions) => {
    let sum = 0;

    for (let i = 0; i < predictions.length; i++) {
        sum += predictions[i].result;
    }

    return sum;
};

console.log("Total result using arrow function:");
console.log(sumResultsArrow(predictions));





const form = document.getElementById("priceForm");
const message = document.getElementById("message");

form.addEventListener("submit", function(event) {

    event.preventDefault();

    // Clear previous message
    message.innerHTML = "";

    // Get values from form
    const location = document.getElementById("location").value.trim();
    const area = document.getElementById("area").value.trim();
    const bedrooms = document.getElementById("bedrooms").value.trim();

    // Check required fields
    if (location === "" || area === "" || bedrooms === "") {

        const error = document.createElement("p");

        error.textContent = "Please fill in all required fields.";
        error.style.color = "red";

        message.appendChild(error);

        return;
    }

    // Check bedrooms
    if (Number(bedrooms) <= 0) {

        const error = document.createElement("p");

        error.textContent = "Bedrooms must be a positive number.";
        error.style.color = "red";

        message.appendChild(error);

        return;
    }

    // Success
    const success = document.createElement("p");

    success.textContent = "Ready to submit";
    success.style.color = "green";

    message.appendChild(success);
});
