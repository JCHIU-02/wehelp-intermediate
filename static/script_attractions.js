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
    let attractionId = pathnameArr[pathnameArr.length - 1]
    let response = await fetch(`/api/attraction/${attractionId}`)
    let data = await response.json();
    return data["data"]
}

async function renderData(){
  let data = await fetchOneAttraction()
  // console.log(data)

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

renderData()


function createImgDiv(){
  let imgContainer = document.createElement("div")
  let img = document.createElement("img")
  let slidesContainer = document.getElementById("slides-container")
  slidesContainer.appendChild(imgContainer)
  imgContainer.appendChild(img)
  imgContainer.classList.add("img-container")
  img.classList.add("slide-img")
  return img
}


function createBullet(){
  let bullet = document.createElement("div")
  bullet.classList.add("bullet")
  bullet.classList.add("bullet-blur")
  bullet.classList.add("bullet-focus")
  let bulletContainer = document.getElementById("bullet-container")
  bulletContainer.appendChild(bullet)
}

async function renderImgs(){
  data = await fetchOneAttraction()
  data["images"].forEach(image => {
    let imgElement = createImgDiv()
    imgElement.src = image
    createBullet()
  })
}


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


let slideIndex = 1;
renderImgs().then(() => {
  showDivs(slideIndex);
  setupSlideBtn()
})
