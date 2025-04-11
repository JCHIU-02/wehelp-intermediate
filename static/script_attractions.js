renderData()

let webTitle = document.getElementById("nav-headline")
webTitle.addEventListener('click', function(){
    window.location.href = '/';
})

let radioBtns = document.querySelectorAll("input[name=time]")
radioBtns.forEach(button => {
    button.addEventListener('change', function(){
        let price = document.getElementById("price")
        if(this.id == "afternoon" && this.checked){
            price.textContent = "新台幣 2500 元"
        }
        if(this.id == "morning" && this.checked){
            price.textContent = "新台幣 2000 元"
        }
    })  
});

async function fetchOneAttraction(){
    let pathnameArr = window.location.pathname.split("/")
    let attractionId = pathnameArr.at(-1)
    let response = await fetch(`/api/attraction/${attractionId}`)
    let data = await response.json(); 
    return data["data"]
}

async function renderData(){

  let data = await fetchOneAttraction()

  let attractionName = document.getElementById("attraction-name")
  let category = document.getElementById("attraction-cat")
  let mrt = document.getElementById("attraction-mrt")
  let description = document.getElementById("attraction-desc")
  let address = document.getElementById("attraction-add")
  let transport = document.getElementById("attraction-transport")

  attractionName.textContent = data["name"]
  category.textContent = data["category"]
  mrt.textContent = data["mrt"]
  description.textContent = data["description"]
  address.textContent = data["address"]
  transport.textContent = data["transport"]
}

function createImgContainer(){
  let imgContainer = document.createElement("div")
  let slidesContainer = document.getElementById("slides-container")
  slidesContainer.appendChild(imgContainer)
  imgContainer.classList.add("img-container")
  return imgContainer
}


function createBullet(){
  let bullet = document.createElement("div")
  bullet.classList.add("bullet")
  bullet.classList.add("bullet-blur")
  bullet.classList.add("bullet-focus")
  let bulletContainer = document.getElementById("bullet-container")
  bulletContainer.appendChild(bullet)
}

async function fetchImgs(){
  data = await fetchOneAttraction()
  return data["images"]
}

async function preloadImgs(){
  let images = await fetchImgs()
  let preloadImages = []
  images.forEach(image => {
    let imgTag = new Image()
    imgTag.src = image
    preloadImages.push(imgTag)
  })
  return preloadImages  
}

async function renderImgs(){
  let imgTags = await preloadImgs()
  imgTags.forEach(imgTag => {
    imgTag.classList.add("slide-img")
    createImgContainer().appendChild(imgTag)
    createBullet()
  })
}

let slideIndex = 1;
renderImgs().then(() => {
  showDivs(slideIndex);
  setupSlideBtn()
})


function setupSlideBtn(){
  let leftBtn = document.getElementById("slide-btn-left")
  let rightBtn = document.getElementById("slide-btn-right")
  leftBtn.addEventListener('click', function(){plusDivs(-1)})
  rightBtn.addEventListener('click', function(){plusDivs(1)})
}


function plusDivs(n) {
  showDivs(slideIndex += n);
  let imgDivs = document.querySelectorAll(".img-container");
  imgDivs[slideIndex-1].classList.add("fade")
}


function showDivs(n) {
  let imgDivs = document.querySelectorAll(".img-container");
  let dots = document.querySelectorAll(".bullet");
  if (n > imgDivs.length) {slideIndex = 1}
  if (n < 1) {slideIndex = imgDivs.length}
  imgDivs.forEach(imgDiv => {
    imgDiv.style.display = "none"
    });
  dots.forEach(dot =>{
    dot.className = dot.className.replace("bullet-focus", "");
  })
  imgDivs[slideIndex-1].style.display = "block";
  dots[slideIndex-1].classList.add("bullet-focus"); 
}


//createBooking

let startBooking = document.getElementById("booking-btn")
startBooking.onclick = function(e){

    e.preventDefault()

    //check sign in or not
    let token = localStorage.getItem("token");
    fetch("/api/user/auth", {
        method:"GET",
        headers:{"Authorization": `Bearer ${token}`}
    })
    .then(response => response.json())
    .then(data => {
    
        //sign in
        if(data["data"]){
          createBooking()
        }

        //not sign in
        else{
          showLoginBox()
        }
    })
}


function createBooking(){

    let date = document.querySelector(".date-picker").value
    let time = document.querySelector("input[name=time]:checked").value
    let price = document.getElementById("price").textContent.slice(4,8)
    let id = window.location.pathname.split('/')[2]

    let bookingData = {
        "attractionId": Number(id),
        "date": date,
        "time": time,
        "price": Number(price)
    }

    let token = localStorage.getItem("token");
    fetch('/api/booking',{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(bookingData)
    })
    .then(response => response.json())
    .then(data => {
        if(data.ok){
            window.location.href = "/booking"
            renderBookingPage()
        }
    })
  }

function showLoginBox(){
  let modal = document.getElementById("modal");
  modal.style.display = "block"

  setTimeout(function(){
    let loginBox = document.querySelector(".login-box")
    loginBox.classList.add("show")
  }, 50)

}

//date-picker start from today & default today
let today = new Date();
let year = today.getFullYear();
let month = String(today.getMonth() + 1).padStart(2, '0');
let day = String(today.getDate() + 1).padStart(2, '0');
let formattedTomorrow = `${year}-${month}-${day}`;
document.querySelector(".date-picker").setAttribute('min', formattedTomorrow);
document.querySelector(".date-picker").value = formattedTomorrow;

