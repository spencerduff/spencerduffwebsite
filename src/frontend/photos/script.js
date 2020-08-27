var infScroll = new InfiniteScroll( '.container', {
  path: function() {
    return "path.html";
  },
  responseType: 'text',
  status: '.scroll-status',
  history: false,
});

var proxyElem = document.createElement('div');
var photoList = [];

for (var i = 0; i < 975; ++i) {
    photoList.push(i);
}

infScroll.on( 'load', function( response ) {
  var id = getRandomPhoto();
  var photo = { "url":'https://spencerduff.com/photos/' + id + '.jpg',
                "id": id }
  // convert HTML string into elements
  var itemHTML = getItemHTML(photo);
  // convert HTML string into elements
  proxyElem.innerHTML = itemHTML;
  // append item elements
  var items = proxyElem.querySelectorAll('.photo-item');
  var modals = proxyElem.querySelectorAll('.deleteModal');
  infScroll.appendItems( items );
  infScroll.appendItems( modals );
});

// load initial page
infScroll.loadNextPage();

var itemTemplateSrc = document.querySelector('#photo-item-template').innerHTML;

function getItemHTML( photo ) {
  return microTemplate( itemTemplateSrc, photo );
}

// micro templating, sort-of
function microTemplate( src, data ) {
  // replace {{tags}} in source
  return src.replace( /\{\{([\w\-_\.]+)\}\}/gi, function( match, key ) {
    // walk through objects to get value
    var value = data;
    key.split('.').forEach( function( part ) {
      value = value[ part ];
    });
    return value;
  });
}

function getRandomPhoto() {
    if (photoList.length == 0) {
        for (var i = 0; i < 975; ++i) {
            photoList.push(i);
        }
    }
    var index = getRandomInt(photoList.length);
    var res = photoList[index];
    photoList.splice(index, 1);
    return res;
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

var modal;

function displayModal(id) {
  modal = document.getElementById("deleteModal"+id);
  modal.style.display = "block";
}

function closeModal(id) {
  modal = document.getElementById("deleteModal"+id);
  modal.style.display = "none";
}

function displaySuccessModal() {
  modal = document.getElementById("successModal");
  modal.style.display = "block";
}

function closeSuccessModal() {
  modal = document.getElementById("successModal");
  modal.style.display = "none";
}

function displayBadPasswordModal() {
  modal = document.getElementById("badPasswordModal");
  modal.style.display = "block";
}

function closeBadPasswordModal() {
  modal = document.getElementById("badPasswordModal");
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function deletePhoto(id) {
  var password = document.getElementById("passwordText" + id).value;
  var body = {"password": password, "id": id};
  callAwsLambdaFunctionDeletePhoto(body);
  var modal = document.getElementById("deleteModal"+id);
  modal.style.display = "none";
}

function callAwsLambdaFunctionDeletePhoto(body) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      displaySuccessModal();
    } else if (this.readyState == 4 && this.status == 401){
      displayBadPasswordModal();
    }
  };
  xhttp.open("DELETE", "https://h8mb4pgqk4.execute-api.us-west-2.amazonaws.com/Prod/deletephoto", true);
  xhttp.send(JSON.stringify(body));
}