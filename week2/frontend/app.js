// ==========================================================
// WEEK 3 - OLD CODE
// ==========================================================

// Code Lab 1 và Lab 2 của tuần trước được giữ lại dưới dạng
// comment để tham khảo.
// Không chạy trong Lab 3.

/*

// =========================
// LAB 1 - Promise
// =========================

function getData() {
    return new Promise(function(resolve) {

        setTimeout(function() {
            resolve("Data đã nhận được!");
        }, 3000);

    });
}


// Cách 1: Dùng .then()

console.log("===== DÙNG .then() =====");

getData()
    .then(function(data) {
        console.log("Data:", data);
    });


// Cách 2: Dùng async/await

console.log("===== DÙNG async/await =====");

async function test() {

    let data = await getData();

    console.log("Data:", data);
}

test();


// =========================
// LAB 2 - Fetch API
// =========================

async function loadUsers() {

    const response = await fetch(
        "https://jsonplaceholder.typicode.com/users"
    );

    const users = await response.json();

    const tbody = document.querySelector("#user-table tbody");

    users.forEach(function(user) {

        const row = document.createElement("tr");

        row.innerHTML =
            `<td>${user.id}</td><td>${user.name}</td>`;

        tbody.appendChild(row);
    });
}

loadUsers();

*/


// ==========================================================
// WEEK 5 - LAB 3
// FastAPI + Frontend Integration
// ==========================================================


// =========================
// Load items from FastAPI
// =========================

async function loadItems() {

    try {

        const response = await fetch("/items");

        if (!response.ok) {
            throw new Error("Failed to fetch items");
        }

        const data = await response.json();

        // Lab 4 - response is now an envelope
        const items = data.items;

        console.log("Items from FastAPI:", items);
        console.log("Total:", data.total);
        console.log("Skip:", data.skip);
        console.log("Limit:", data.limit);


        const itemList = document.getElementById("item-list");

        if (!itemList) {
            return;
        }

        itemList.innerHTML = "";

        items.forEach(function(item) {

            const li = document.createElement("li");

            li.textContent =
                `${item.id} - ${item.name} - ${item.price} VND`;

            itemList.appendChild(li);

        });

    } catch (error) {

        console.error("Error loading items:", error);

    }
}

loadItems();