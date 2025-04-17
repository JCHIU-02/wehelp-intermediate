let token = localStorage.getItem("token");
authenticateUser(token)
getOrder()

async function authenticateUser(token){
    let response = await fetch("/api/user/auth", {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
        });
    let data = await response.json();
        
    if (!data["data"]) {
        window.location.href = "/";
    }    
    else{
        document.body.style.display = "block"
    }
}

//fetch 訂單資訊，status=0 渲染成功資訊，status=1 渲染失敗資訊
async function getOrder(){
    let url = window.location.href
    let orderNumber = url.split("=")[1]
    let token = localStorage.getItem("token");
    let response = await fetch(`/api/order/${orderNumber}`,{
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
    })
    let data = await response.json()
    let orderData = data["data"]
    if(orderData["status"] == 0){
        renderPaymentSuccessPage(orderData)
    }
    else{
        renderPaymentFailedPage(orderData)
    }
}


function renderPaymentSuccessPage(data){
    let img = document.querySelector(".thankyou.booking-data-img")
        img.src = data["trip"]["attraction"]["image"]
        let paymentResult = document.querySelector(".payment-headline")
        paymentResult.classList.add("success")
        paymentResult.textContent = "付款完成，感謝訂購！"
        let paymentContent = document.querySelector(".payment-content")
        paymentContent.textContent = "您已成功預定的行程如下："
        let attraction = document.querySelector(".thankyou-attraction")
        let orderNumber = document.querySelector(".thankyou.order-number")
        let date = document.querySelector(".thankyou.date")
        let time = document.querySelector(".thankyou.time")
        let address = document.querySelector(".thankyou.place")
        orderNumber.textContent = `訂單編號：${data["number"]}`
        attraction.textContent = `景點：${data["trip"]["attraction"]["name"]}`
        date.textContent = `日期：${data["trip"]["date"]}`
        address.textContent = `地點：${data["trip"]["attraction"]["address"]}`
        if(data["trip"]["time"] == "morning"){
            time.textContent = "時間：早上 9 點到下午 4 點"
        }
        else{
            time.textContent = "時間：下午 2 點到晚上 9 點"
        }
        let note = document.querySelector(".thankyou.note")
        note.textContent = "請記得將預定行程加到行事曆或截圖喔，期待與您相見。"
        let orderDatacontainer = document.querySelector(".thankyou.booking-data-container")
        orderDatacontainer.style.display = "flex"
}

function renderPaymentFailedPage(data){
    let paymentResult = document.querySelector(".payment-headline")
    let cartLink = paymentResult.querySelector("a")
    paymentResult.prepend("付款失敗，請至")
    cartLink.textContent = " 預定行程 "
    paymentResult.append("重新付款。")
    let paymentContent = document.querySelector(".payment-content")
    paymentContent.textContent = `您的訂單編號：${data["number"]}`
    let footer = document.querySelector(".footer.thankyou")
    footer.style.position = "fixed"
    footer.style.bottom = "0"
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