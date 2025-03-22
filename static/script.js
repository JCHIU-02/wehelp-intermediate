//fetch mrt list
function fetchMRTList(){
    return fetch('/api/mrts')
    .then(response => response.json())
    .then(data => {
        mrtData = data["data"] 
        mrtData.forEach(mrtName => {
            createMRTContainer().textContent = mrtName  
        });
        })
}

//create mrt list container
function createMRTContainer(){
    let mrtList = document.getElementById('mrt-list')
    let mrtItem = document.createElement("li")
    mrtList.appendChild(mrtItem)
    mrtItem.classList.add('mrt-list-item')
    return mrtItem
}

//search attractions by mrt station
fetchMRTList().then(() => {
    let mrt_list_item = document.querySelectorAll(".mrt-list-item")
    mrt_list_item.forEach(itemElement => {
        itemElement.addEventListener('click', function(){
            let mrtName = itemElement.textContent
            let input = document.getElementById('slogan-input')
            input.value = mrtName
            // 自動送出表單：建立 submit 事件 & 觸發 submit 事件
            let submitEvent = new Event('submit')
            let sloganForm = document.getElementById('slogan-form')
            sloganForm.dispatchEvent(submitEvent)
        })       
    });
})


//render attractions on index page 
function loadAttractions(page = 0, keyword = ''){
    return fetch(`/api/attractions?page=${page}&keyword=${keyword}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        let attractionData = data["data"]
        attractionData.forEach(attraction => {
            let container = createAttractionContainer()
            container.img.src = attraction["images"][0]
            container.name.textContent = attraction["name"]
            container.mrt.textContent = attraction["mrt"]
            container.category.textContent = attraction["category"]   
        });
        return data["nextPage"]       
    })
}


//render attractions without keyword (initial loading)
let globalObserver = null
let isLoading = false

loadAttractions().then(nextPage => {
    currentPage = nextPage
    globalObserver = new IntersectionObserver((entries) => {
        if(entries[0].isIntersecting && isLoading == false){
            isLoading = true
            loadAttractions(currentPage).then(nextPageValue => {
                isLoading = false
                if(nextPageValue !== null){
                    currentPage = nextPageValue;
                }
                else{
                    globalObserver.disconnect();
                }
            });
        }
    });
    let target = document.getElementById("footer")
    globalObserver.observe(target);
});


//render attractions with keyword
let form = document.getElementById("slogan-form");
form.addEventListener('submit', function(e) {
    e.preventDefault()

    if(globalObserver){
        globalObserver.disconnect();
    }

    let inputValue = document.getElementById("slogan-input").value
    if(inputValue !== "輸入景點名稱查詢"){

    const attractionsSection = document.getElementById("attractions-section");
    attractionsSection.replaceChildren();

    loadAttractions(0, inputValue).then(nextPage => {
        if(nextPage != null){
            page = nextPage
            globalObserver = new IntersectionObserver((entries) => {
                    if(entries[0].isIntersecting && isLoading == false){
                        isLoading = true
                        loadAttractions(page, inputValue).then(nextPageValue => {
                            if(nextPageValue !== null){
                                isLoading = false
                                page = nextPageValue;
                            }
                            else{
                                globalObserver.disconnect();
                            }
                        });
                    }   
                });
            let target = document.getElementById("footer")
            globalObserver.observe(target);
        }
    });
}   
})


function createAttractionContainer(){
    let attractionsSection = document.getElementById('attractions-section')
    let attractionCard = document.createElement("div")
    let attractionInfo = document.createElement("div")
    let attractionTag = document.createElement("div")
    attractionsSection.appendChild(attractionCard)
    attractionCard.appendChild(attractionInfo)
    attractionCard.appendChild(attractionTag)
    let infoImg = document.createElement("img")
    let infoName = document.createElement("p")
    attractionInfo.appendChild(infoImg)
    attractionInfo.appendChild(infoName)
    let tagMrt = document.createElement("p")
    let tagCat = document.createElement("p")
    attractionTag.appendChild(tagMrt)
    attractionTag.appendChild(tagCat)
    attractionCard.classList.add("attraction")
    attractionInfo.classList.add("attraction-info")
    attractionTag.classList.add("attraction-tag")
    infoImg.classList.add("attraction-info-img")
    infoName.classList.add("attraction-info-name")
    tagMrt.classList.add("attraction-tag-mrt")
    tagCat.classList.add("attraction-tag-cat")

    return{
        img: infoImg,
        name: infoName,
        mrt: tagMrt,
        category: tagCat
    }
}


function scrollMRTList(){
    let mrtList = document.getElementById('mrt-list');
    let leftBtn = document.querySelector('.list-bar-leftBtn');
    let rightBtn = document.querySelector('.list-bar-rightBtn');
    let scrollAmount = 200;

    leftBtn.addEventListener('click', function() {
        mrtList.scrollBy({
            left: -scrollAmount,
            behavior: 'smooth'
        });
    });
    rightBtn.addEventListener('click', function() {
        mrtList.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });
    });
}

scrollMRTList();

function changeBtnIcon(){
    let leftBtn = document.querySelector('.list-bar-leftBtn');
    let rightBtn = document.querySelector('.list-bar-rightBtn');
    let leftBtn_icon = document.getElementById('leftBtn-icon');
    let rightBtn_icon = document.getElementById('rightBtn-icon');

    leftBtn.addEventListener('mouseover', function(){
            leftBtn_icon.src = "/static/images/left-hovered.png"
        });
    leftBtn.addEventListener('mouseout', function(){
            leftBtn_icon.src = "/static/images/left-default.png"
        });
    rightBtn.addEventListener('mouseover', function(){
            rightBtn_icon.src = "/static/images/right-hovered.png"
        });
    rightBtn.addEventListener('mouseout', function(){
            rightBtn_icon.src = "/static/images/right-default.png"
        });
}

changeBtnIcon();


function clearInputValue(){
    let slogan_input = document.getElementById('slogan-input');
    slogan_input.addEventListener('focus', function(){
        if (slogan_input.value !== null) {
            slogan_input.value = '';
        }
    });

    slogan_input.addEventListener('blur', function(){
        if (slogan_input.value == '') {
            slogan_input.value = '輸入景點名稱查詢';
        }
    });
}

clearInputValue();