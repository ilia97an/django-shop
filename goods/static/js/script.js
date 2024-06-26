var currentImage = document.getElementById("current-image");

function thumbClick(thumb) {
  currentImage.src = thumb.src;
}

const rate = (rating, product_id) => {
  fetch(`/goods/rate/${product_id}/${rating}/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(rest => {
    //window.location.reload();
    // you may want to update the rating here
    // to simplify stuff, I just reload the page
  })
}
