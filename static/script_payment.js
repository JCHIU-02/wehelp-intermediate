//TapPay
let fields = {
    number: {
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'CVV'
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'font-size': '16px',
            'font-weight': '500',
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
})



// call TPDirect.card.getPrime when user submit form to get tappay prime
let paymentBtn = document.querySelector(".booking-btn.payment")
paymentBtn.addEventListener('click', onSubmit)

function onSubmit(event) {
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    let tappayStatus = TPDirect.card.getTappayFieldsStatus()
    let contactData = getContact()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert("信用卡資料有誤，請重新確認。")
        return
    }

    if(contactData){
    // Get prime
        TPDirect.card.getPrime((result) => {
            if (result.status !== 0) {
                alert('get prime error ' + result.msg)
                return
            }
            // alert('get prime 成功，prime: ' + result.card.prime)
            // send prime to your server, to pay with Pay by Prime API .
            organizeOrderData(result.card.prime, contactData).then((orderData) => {
                let token = localStorage.getItem("token")
                fetch('/api/orders',{
                    method: 'POST',
                    headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify(orderData)
                })
                .then(response => response.json())
                .then(data => {
                    if(data["data"]){
                        window.location.href = `/thankyou?number=${data["data"]["number"]}`
                    }
                })

            })
        })
    }

}

function getContact(){

    let contactName = document.getElementById("contact-name")
    let contactEmail = document.getElementById("contact-email")
    let contactPhone = document.getElementById("contact-phone-number")
    let re = /^09[0-8][0-9]{7}$/

    if(!contactName.value || !contactEmail.value || !contactPhone.value){
        alert('請填寫完整的聯絡資訊。')
    }

    else if(!contactEmail.value.includes("@")){
        alert('Email 格式有誤，請重新輸入。')
    }

    else if(!re.test(contactPhone.value)){
        alert('電話號碼格式有誤，請重新輸入。')
    }

    else{
        let contactData = {
            "name": contactName.value,
            "email": contactEmail.value,
            "phone": contactPhone.value
        }
        return contactData
    }
}


async function organizeOrderData(primeNumber, contactData){
    //呼叫 api booking 取得 booking data
    let data = await getBooking();
    let bookingData = data["data"]
    let orderData = {
        "prime": primeNumber, //string
        "order": {
            "price": bookingData["price"],
            "trip": {
                "attraction": bookingData["attraction"],
                "date": bookingData["date"],
                "time": bookingData["time"]
            },
            "contact": contactData
        }
    }
    return orderData
}


async function getBooking(){
    let token = localStorage.getItem("token");
    let response = await fetch('/api/booking',{
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
    })
    let data = await response.json()
    return data
}

