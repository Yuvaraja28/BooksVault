function addToCart(name, price, image, book_status, rental_start_date, rental_end_date) {
    let cart = localStorage.getItem('cart');
    cart = cart ? JSON.parse(cart) : [];

    const item = {
        name: name,
        price: price,
        image: image,
        quantity: 1,
        book_status: book_status,
        rental_start_date: rental_start_date,
        rental_end_date: rental_end_date,
        quantity: book_status === 'rental' ? 1 : 1 // Set quantity to 1 for rental books
    };

    const existingItemIndex = cart.findIndex(cartItem =>
        cartItem.name === name &&
        cartItem.book_status === book_status &&
        cartItem.rental_start_date === rental_start_date &&
        cartItem.rental_end_date === rental_end_date
    );

    if (existingItemIndex > -1) {
      if (book_status !== 'rental') {
        cart[existingItemIndex].quantity++;
      }
    } else {
        cart.push(item);
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    openModal('Book added to cart!', 'Cart');
}

updateCartCount();
