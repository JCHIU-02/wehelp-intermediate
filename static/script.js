//fetch mrt list
function fetchMRTList(){
    fetch('/api/mrts')
    .then(response => response.json())
    .then(data => {
        mrtData = data["data"] 
        mrtData.forEach(mrtName => {
            createMRTContainer().textContent = mrtName  
        });
        })
    .catch(error => {
        console.error('發生錯誤:', error);
        });
}
    
function createMRTContainer(){
    let mrtList = document.getElementById('mrt-list')
    let mrtItem = document.createElement("li")
    mrtList.appendChild(mrtItem)
    mrtItem.classList.add('mrt-list-item')
    return mrtItem
}

fetchMRTList();


//fetch attractions without keyword

function attractionLoader(){
    
    let page = 0

    function loadAttractions(){
        return fetch(`/api/attractions?page=${page}`)
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

    loadAttractions().then(nextPage => {
            page = nextPage
            let observer = new IntersectionObserver((entries) => {
                //load more...
                if(entries[0].isIntersecting)
                loadAttractions().then(nextPageValue => {
                    if(nextPageValue !== null){
                        page = nextPageValue;
                    }
                    else{
                        observer.disconnect();
                    }
                });
                }
            );
            let target = document.getElementById("footer")
            observer.observe(target);
        
    });
}

attractionLoader();








    let mrtList = document.getElementById('mrt-list');
    let leftBtn = document.querySelector('.list-bar-leftBtn');
    let rightBtn = document.querySelector('.list-bar-rightBtn');
    let leftBtn_icon = document.getElementById('leftBtn-icon');
    let rightBtn_icon = document.getElementById('rightBtn-icon');
    let slogan_input = document.querySelector('#slogan-form input');

    // mrt_list 捲動
    document.addEventListener('DOMContentLoaded', function() {
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
    });

    //mrt-list icon hover
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

    //input default value
    slogan_input.addEventListener('focus', function(){
      slogan_input.value = ''
    })

    slogan_input.addEventListener('blur', function(){
      slogan_input.value = '輸入景點名稱查詢'
    })