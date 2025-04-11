let navBookingBtn = document.querySelector(".nav-items-btn")
navBookingBtn.onclick = function(){

    let token = localStorage.getItem("token");
        fetch("/api/user/auth", {
            method:"GET",
            headers:{"Authorization": `Bearer ${token}`}
        })
        .then(response => response.json())
        .then(data => {
        
            if(data["data"]){
                window.location.href = "/booking"
            }
            else{
                let modal = document.getElementById("modal");
                modal.style.display = "block"

                setTimeout(function(){
                    let loginBox = document.querySelector(".login-box")
                    loginBox.classList.add("show")
                    showSigninForm()
                }, 50)
            }
        })
    }




    

