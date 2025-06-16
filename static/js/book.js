$(document).ready(function() {

  $('.color-choose input').on('click', function() {
      var headphonesColor = $(this).attr('data-image');

      $('.active').removeClass('active');
      $('.left-column img[data-image = ' + headphonesColor + ']').addClass('active');
      $(this).addClass('active');
  });

  $('.cart-btn').on('click', function(event) {
    event.preventDefault();
    const name = $(this).data('name');
    const price = $(this).data('price');
    const image = $(this).data('image');
    const book_status = $(this).data('book_status');
    const rental_start_date = $('#rental_start_date').val();
    const rental_end_date = $('#rental_end_date').val();

    addToCart(name, price, image, book_status, rental_start_date, rental_end_date);
    updateCartCount();
  });

});
