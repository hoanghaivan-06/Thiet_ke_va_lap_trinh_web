// Lấy các phần tử từ DOM
const houseForm = document.getElementById("houseForm");
const messageContainer = document.getElementById("messageContainer");

// Đăng ký sự kiện submit cho Form
houseForm.addEventListener("submit", function (event) {
  // 1. Chặn hành vi load lại trang mặc định của Form
  event.preventDefault();

  // Yêu cầu "Finished early": Xóa thông báo cũ trước khi hiển thị thông báo mới
  messageContainer.innerHTML = "";

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

// ==========================================
// TEST PROMISE
// ==========================================

console.log("===== TEST PROMISE =====");

Promise.resolve(100)
    .then(function(data) {

        console.log("data =", data);

        return "Hello World";
    })
    .then(function(data) {

        console.log("data từ Promise trước =", data);

    })
    .catch(function(error) {

        console.error("Lỗi:", error);

    });


// ==========================================
// TEST FETCH
// ==========================================

console.log("===== TEST FETCH =====");

console.log("A");

fetch("https://jsonplaceholder.typicode.com/users")

    .then(function(response) {

        console.log("1. Đã nhận response");

        console.log("response =", response);

        // response.json() trả về Promise
        return response.json();

    })

    .then(function(data) {

        console.log("2. Đã có data");

        console.log("data =", data);

        console.log("User đầu tiên =", data[0]);

    })

    .catch(function(error) {

        console.error("Fetch lỗi:", error);

    });

console.log("C");