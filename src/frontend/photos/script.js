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
  var photo = {"url":'https://spencerduff.com/photos/' + getRandomPhoto() + '.jpg'}
  // convert HTML string into elements
  var itemHTML = getItemHTML(photo);
  // convert HTML string into elements
  proxyElem.innerHTML = itemHTML;
  // append item elements
  var items = proxyElem.querySelectorAll('.photo-item');
  infScroll.appendItems( items );
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