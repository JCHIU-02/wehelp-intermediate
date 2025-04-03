function hideUserStatus(){
    let userStatus = document.querySelectorAll(".user-status")
    userStatus.forEach(status => {
        status.hidden = true
    })
}


//check user_status
token = document.cookie.split("=")[1]
console.log(token)
fetch("/api/user/auth", {
    method:"GET",
    headers:{"Authorization": `Bearer ${token}`}
})
.then(response => response.json())
.then(data => {

    let loginBtn = document.getElementById("nav-login-btn")
    let logoutBtn = document.getElementById("nav-logout-btn")
    
    if(data["data"]){
        loginBtn.hidden = true
        logoutBtn.hidden = false
    }
    else{
        loginBtn.hidden = false
        logoutBtn.hidden = true 
    }
})


 //logout
let logoutBtn = document.getElementById("nav-logout-btn")
logoutBtn.addEventListener('click', function(){
    document.cookie = "token= ; max-age=0; path=/;"
    window.location.reload()
})


//show login box
let loginBtn = document.getElementById("nav-login-btn")
loginBtn.addEventListener('click', function(){
    let modal = document.getElementById("modal");
    modal.style.display = "block"

    setTimeout(function(){
        let loginBox = document.querySelector(".login-box")
        loginBox.classList.add("show")
        showSigninForm()
    }, 50)
})

//html btn onclick
function showSignupForm(){
    let loginForm = document.querySelector(".login-form")
    loginForm.hidden = true
    let signUpBox = document.querySelector(".signup-form")
    signUpBox.hidden = false  
}

//html btn onclick
function showSigninForm(){
    let loginForm = document.querySelector(".login-form")
    loginForm.hidden = false
    let signUpBox = document.querySelector(".signup-form")
    signUpBox.hidden = true
}

//signup
let signUpForm = document.querySelector(".signup-form")
signUpForm.addEventListener('submit', function(e){

    e.preventDefault()
    
    let nameInput = document.querySelector(".signup-input.name").value
    let emailInput = document.querySelector(".signup-input.email").value
    let passwordInput = document.querySelector(".signup-input.password").value

    let userData = {
        "name": nameInput,
        "email": emailInput,
        "password": passwordInput
    }

    if(!emailInput.includes("@")){
        let invalidEmailFormat = document.querySelector(".signup.user-status.error")
        invalidEmailFormat.hidden = false
        invalidEmailFormat.textContent = "Email 格式錯誤"
    }

    else{
        fetch("/api/user", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(userStatus => {
            if(userStatus.ok){
                hideUserStatus() 
                let successMessage = document.querySelector(".signup.user-status.ok")
                successMessage.hidden = false
                successMessage.textContent = "註冊成功，請登入系統"
            }
            else if(userStatus.error){
                hideUserStatus()
                let duplicateEmail = document.querySelector(".signup.user-status.error")
                duplicateEmail.hidden = false
                duplicateEmail.textContent = userStatus["message"]
                }
            })
    } 
})

//login
let SignInForm = document.querySelector(".login-form")
SignInForm.addEventListener('submit', function(e){

    e.preventDefault()

    let emailInput = document.querySelector(".login-input.email").value
    let passwordInput = document.querySelector(".login-input.password").value

    let userData = {
        "email": emailInput,
        "password": passwordInput
    }

    fetch("/api/user/auth", {
        method:"PUT",
        headers:{'Content-Type': 'application/json'},
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(userStatus => {
        if(userStatus.ok){
            window.location.reload();
            
        }
        else if(userStatus.error){
            let wrongDataMsg = document.querySelector(".login.user-status.error")
            wrongDataMsg.hidden = false
            wrongDataMsg.textContent = userStatus["message"]
        }
    })

})

//clear input
let loginBoxInput = document.querySelectorAll(".login-box input")
loginBoxInput.forEach(input => {
    input.addEventListener('focus', function(){
        input.value = ''
    })
})


//hide modal
window.onclick = function(event) {
  if (event.target == modal) {
    let loginBox = document.querySelector(".login-box")
    loginBox.classList.remove("show")
    modal.style.display = "none";
  }
}


//toggle password
function togglePassword(eyeElement, input){
    eyeElement.addEventListener("click", function(e){
        if(e.target.classList.contains('fa-eye')){
          e.target.classList.remove('fa-eye');
          e.target.classList.add('fa-eye-slash');
          input.type = "password"
        }else{
          e.target.classList.remove('fa-eye-slash');
          e.target.classList.add('fa-eye')
          input.type = "text"
        }
      });
}

let loginEye = document.getElementById("login-eye-closed")
let loginInput = document.querySelector(".login-input.password")
let signupEye = document.getElementById("signup-eye-closed")
let signupInput = document.querySelector(".signup-input.password")

togglePassword(loginEye, loginInput)
togglePassword(signupEye, signupInput)