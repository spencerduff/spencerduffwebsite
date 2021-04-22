
function displayDoneModal() {
  modal = document.getElementById("doneRequestModal");
  modal.style.display = "block";
}

function closeDoneModal() {
  modal = document.getElementById("doneRequestModal");
  modal.style.display = "none";
}

function displaySuccessModal() {
  modal = document.getElementById("contactModal");
  modal.style.display = "block";
}

function closeSuccessModal() {
  modal = document.getElementById("contactModal");
  modal.style.display = "none";
}

function displayBadRequestModal() {
  modal = document.getElementById("badRequestModal");
  modal.style.display = "block";
}

function closeBadRequestModal() {
  modal = document.getElementById("badRequestModal");
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function sendEmail() {
  var email = document.getElementById("emailField").value;
  var subject = document.getElementById("subjectField").value;
  var message = document.getElementById("messageField").value;
  var captcha = document.getElementById("captchaCheck").value;

  var body = {"email": email, "subject": subject, "message": message, "captcha": captcha};

  var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        displayDoneModal();
      } else if (this.readyState == 4 && this.status == 403){
        displayBadRequestModal();
      }
    };
    xhttp.open("POST", "https://xsa3ob1age.execute-api.us-west-2.amazonaws.com/Prod/postEmail", true);
    xhttp.send(JSON.stringify(body));
}