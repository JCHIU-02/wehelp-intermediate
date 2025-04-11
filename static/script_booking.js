let token = localStorage.getItem("token");

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
    return data["data"];
}


authenticateUser(token).then(userData => {

    if (userData){
        fetch('/api/booking',{
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
        })
        .then(response => response.json())
        .then(data => {

            //render page view
            if (data["data"]){
                let bookingData = data["data"]
                let userName = userData["name"]
                let userNameSpan = document.querySelector(".booking-headline > span")
                let attractionName = document.querySelector(".booking-data-title > span")
                let dateSpan = document.querySelector(".booking-data.date > span")
                let timeSpan = document.querySelector(".booking-data.time > span")
                let priceSpan = document.querySelector(".booking-data.price > span")
                let addressSpan = document.querySelector(".booking-data.place > span")
                let img = document.querySelector(".booking-data-img")
                userNameSpan.textContent = userName
                attractionName.textContent = bookingData["attraction"]["name"]
                dateSpan.textContent = bookingData["date"]
                priceSpan.textContent = "新台幣 "+ bookingData["price"]+ " 元"
                addressSpan.textContent = bookingData["attraction"]["address"]
                img.src = bookingData["attraction"]["image"]

                if(bookingData["time"] == "morning"){
                    timeSpan.textContent = "早上 9 點到下午 4 點"
                }
                else{
                    timeSpan.textContent = "下午 2 點到晚上 9 點"
                }
                document.body.style.display = "block"
            }
            else{
                let bookingSection = document.querySelector(".booking-main")
                bookingSection.replaceChildren()
                let pTag = document.createElement("p")
                pTag.classList.add("booking-headline")
                pTag.textContent = "目前沒有任何預定的行程。"
                bookingSection.appendChild(pTag)
                let footer = document.getElementById("footer")
                footer.style.position = "fixed"
                footer.style.bottom = "0"
                document.body.style.display = "block"
            }
        })
    }
})



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