//fetch mrt list
async function fetchMRTList(){
    const response = await fetch('/api/mrts');
    const data = await response.json();
    return data["data"];
}

//create mrt list container
function createMRTContainer(){
    let mrtList = document.getElementById('mrt-list')
    let mrtItem = document.createElement("li")
    mrtList.appendChild(mrtItem)
    mrtItem.classList.add('mrt-list-item')
    return mrtItem
}

//render MRT list on the page
async function renderMRTList() {
    const mrtData = await fetchMRTList();
    mrtData.forEach(mrtName => {
        createMRTContainer().textContent = mrtName;
    });
}

//after rendering MRT list is complete: 1. addEventListner 2. list scroll
renderMRTList().then(() => {
    setupMRTItemListener();
    setupMRTListScroller();
    })

function setupMRTItemListener(){
    let mrt_list_item = document.querySelectorAll('.mrt-list-item')
    mrt_list_item.forEach(itemElement => {
        itemElement.addEventListener('click', function(){
            let mrtName = itemElement.textContent
            let input = document.getElementById('slogan-input')
            input.value = mrtName
            // trigger submit automatically
            let submitEvent = new Event('submit')
            let sloganForm = document.getElementById('slogan-form')
            sloganForm.dispatchEvent(submitEvent)
        })       
    });
}

function setupMRTListScroller(){
    let mrtList = document.getElementById('mrt-list');
    let leftBtn = document.querySelector('.list-bar-leftBtn');
    let rightBtn = document.querySelector('.list-bar-rightBtn');

    leftBtn.addEventListener('click', function() {
        mrtList.scrollBy({
            left: -850,
            behavior: 'smooth'
        });
    });
    rightBtn.addEventListener('click', function() {
        mrtList.scrollBy({
            left: 850,
            behavior: 'smooth'
        });
    });
}


//fetch attractions
async function fetchAttractions(page, keyword){
    const response = await fetch(`/api/attractions?page=${page}&keyword=${keyword}`);
    const data = await response.json();
    return data
}

//render attractions
async function renderAttractions(page = 0, keyword = '') {
    const attractionsData = await fetchAttractions(page, keyword);
    if(attractionsData){
        console.log(attractionsData["data"])
        attractionsData["data"].forEach(attraction => {
            let container = createAttractionContainer();
            container.img.src = attraction["images"][0];
            container.name.textContent = attraction["name"];
            container.mrt.textContent = attraction["mrt"];
            container.category.textContent = attraction["category"];
            container.aTag.href = `/attraction/${attraction["id"]}`
        });
        return attractionsData["nextPage"];
    }
}


let globalObserver = null
let isLoading = false
let currentPage

//addObserver
async function addObserver(nextPage, keyword){

    if(globalObserver){
        globalObserver.disconnect();
    }

    if(nextPage != null){
        currentPage = nextPage
        globalObserver = new IntersectionObserver((entries) => {
            if(entries[0].isIntersecting && isLoading == false){
                isLoading = true
                renderAttractions(currentPage, keyword).then(nextPageValue => {
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
    }
}

//load data without keyword
renderAttractions().then(nextPage => {
    addObserver(nextPage)
})

//load with keyword
let form = document.getElementById("slogan-form");
form.addEventListener('submit', function(e) {
    e.preventDefault()
    
    let inputValue = document.getElementById("slogan-input").value
    const attractionsSection = document.getElementById("attractions-section");
    attractionsSection.replaceChildren();

    renderAttractions(0, inputValue).then(nextPage => {
        addObserver(nextPage, inputValue)
    })

})


function createAttractionContainer(){
    let attractionsSection = document.getElementById('attractions-section')
    let attractionURL = document.createElement("a")
    let attractionCard = document.createElement("div")
    let attractionInfo = document.createElement("div")
    let attractionTag = document.createElement("div")
    attractionsSection.appendChild(attractionURL)
    attractionURL.appendChild(attractionCard)
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
        category: tagCat,
        aTag: attractionURL
    }
}


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