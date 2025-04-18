let token = localStorage.getItem("token");
authenticateUser(token)
getBooking()

//check user status
async function authenticateUser(token){
    let response = await fetch("/api/user/auth", {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
        });
    let data = await response.json();
        
    if (!data["data"]) {
        window.location.href = "/";
    }    
}

//fetch booking data
async function getBooking(){
    let response = await fetch('/api/booking', {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    })
    let data = await response.json()
    let bookingData = data["data"]

    //render page view
    if (bookingData){
        renderBookingData(bookingData)
    }
    else{
        renderEmptyBookingData()
    }        
}

function renderBookingData(data){
    let attractionName = document.querySelector(".booking-data-title > span")
    let dateSpan = document.querySelector(".booking-data.date > span")
    let timeSpan = document.querySelector(".booking-data.time > span")
    let priceSpan = document.querySelector(".booking-data.price > span")
    let addressSpan = document.querySelector(".booking-data.place > span")
    let img = document.querySelector(".booking-data-img")
    let totalPrice = document.querySelector(".booking-page-form.price > span")
    attractionName.textContent = data["attraction"]["name"]
    dateSpan.textContent = data["date"]
    priceSpan.textContent = "新台幣 "+ data["price"]+ " 元"
    addressSpan.textContent = data["attraction"]["address"]
    img.src = data["attraction"]["image"]
    totalPrice.textContent = priceSpan.textContent

    if(data["time"] == "morning"){
        timeSpan.textContent = "早上 9 點到下午 4 點"
    }
    else{
        timeSpan.textContent = "下午 2 點到晚上 9 點"
    }
    document.body.style.display = "block"
}

function renderEmptyBookingData(){
    let bookingSection = document.querySelector(".booking-main")
    bookingSection.replaceChildren()
    let pTag = document.createElement("p")
    pTag.classList.add("booking-headline")
    pTag.textContent = "目前沒有任何預定的行程。"
    bookingSection.appendChild(pTag)
    let footer = document.querySelector(".footer.booking")
    footer.style.position = "fixed"
    footer.style.bottom = "0"
    document.body.style.display = "block"
}


//logout
let logoutBtn = document.getElementById("nav-logout-btn")
logoutBtn.addEventListener('click', function(){
    localStorage.removeItem("token")
    window.location.reload()
})

//to homepage
let webTitle = document.getElementById("nav-headline")
webTitle.addEventListener('click', function(){
    window.location.href = '/';
})

//delete
let deleteBtn = document.querySelector(".booking-data-icon-container")
deleteBtn.onclick = function(){
    let token = localStorage.getItem("token");
    fetch("/api/booking", {
        method:"DELETE",
        headers: {
            "Content-Type":"application/json",
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data.ok){
            window.location.reload()
        }
    })
}
