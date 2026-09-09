// Lấy các phần tử từ DOM
const houseForm = document.getElementById("houseForm");
const messageContainer = document.getElementById("messageContainer");
const predictionContainer = document.getElementById("predictionContainer");


// Đăng ký sự kiện submit cho Form
houseForm.addEventListener("submit", async function (event) {
  // 1. Chặn hành vi load lại trang mặc định của Form
  event.preventDefault();

  // Yêu cầu "Finished early": Xóa thông báo cũ trước khi hiển thị thông báo mới
  messageContainer.innerHTML = "";
  predictionContainer.innerHTML = "";


  // Lấy giá trị từ các trường input
  const addressVal = document.getElementById("address").value.trim();
  const bedroomsVal = document.getElementById("bedrooms").value.trim();
  const bedroomsNum = Number(bedroomsVal);

  // 2. Validate dữ liệu (Kiểm tra rỗng và bedrooms phải là số dương > 0)
  if (addressVal === "" || bedroomsVal === "") {
    showError("Vui lòng điền đầy đủ tất cả các trường bắt buộc!");
    return;
  }

  if (isNaN(bedroomsNum) || bedroomsNum <= 0) {
    showError("Số phòng ngủ (bedrooms) phải là một số dương lớn hơn 0!");
    return;
  }

  // 3. Xử lý khi dữ liệu hợp lệ (Success)
  showSuccess("Ready to submit");

   try {

    const response = await fetch("data.json");

    const data = await response.json();

    const prediction = data.predicted_price;

    const predictionMsg = document.createElement("p");

    predictionMsg.textContent =
      "Predicted house price: $" + prediction;

    predictionMsg.style.fontWeight = "bold";
    predictionMsg.style.fontSize = "20px";

    predictionContainer.appendChild(predictionMsg);

  } catch (error) {

    console.error("Lỗi khi lấy prediction:", error);

    showError("Không thể lấy prediction từ server.");

  }

});

// Hàm hiển thị lỗi màu đỏ bằng createElement & appendChild
function showError(message) {
  const errorMsg = document.createElement("p");
  errorMsg.textContent = message;
  errorMsg.style.color = "red";
  errorMsg.style.fontWeight = "bold";
  
  messageContainer.appendChild(errorMsg);
}

// Hàm hiển thị thông báo thành công
function showSuccess(message) {
  const successMsg = document.createElement("p");
  successMsg.textContent = message;
  successMsg.style.color = "green";
  successMsg.style.fontWeight = "bold";
  
  messageContainer.appendChild(successMsg);
}

// Lab1
function getData() {
    return new Promise(function(resolve) {

        setTimeout(function() {
            resolve("Data đã nhận được!");
        }, 3000);

    });
}
// ==========================================
// Cách 1: Dùng .then()
// ==========================================

console.log("===== DÙNG .then() =====");

getData()
    .then(function(data) {
        console.log("Data:", data);
    });

// ==========================================
// Cách 2: Dùng async/await
// ==========================================
console.log("===== DÙNG async/await =====");

async function test() {

    let data = await getData();

    console.log("Data:", data);
}

test();

/// lab2
async function loadUsers() {
    // 1. Gọi API
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

