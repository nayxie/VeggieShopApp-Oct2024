(function($) {

  "use strict";

  var initPreloader = function() {
    $(document).ready(function($) {
    var Body = $('body');
        Body.addClass('preloader-site');
    });
    $(window).load(function() {
        $('.preloader-wrapper').fadeOut();
        $('body').removeClass('preloader-site');
    });
  }

	var initChocolat = function() {
		Chocolat(document.querySelectorAll('.image-link'), {
		  imageSize: 'contain',
		  loop: true,
		})
	}

  var initSwiper = function() {

    var swiper = new Swiper(".main-swiper", {
      speed: 500,
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    var category_swiper = new Swiper(".category-carousel", {
      slidesPerView: 6,
      spaceBetween: 30,
      speed: 500,
      navigation: {
        nextEl: ".category-carousel-next",
        prevEl: ".category-carousel-prev",
      },
      breakpoints: {
        0: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 3,
        },
        991: {
          slidesPerView: 4,
        },
        1500: {
          slidesPerView: 6,
        },
      }
    });

    var brand_swiper = new Swiper(".brand-carousel", {
      slidesPerView: 4,
      spaceBetween: 30,
      speed: 500,
      navigation: {
        nextEl: ".brand-carousel-next",
        prevEl: ".brand-carousel-prev",
      },
      breakpoints: {
        0: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 2,
        },
        991: {
          slidesPerView: 3,
        },
        1500: {
          slidesPerView: 4,
        },
      }
    });

    var products_swiper = new Swiper(".products-carousel", {
      slidesPerView: 5,
      spaceBetween: 30,
      speed: 500,
      navigation: {
        nextEl: ".products-carousel-next",
        prevEl: ".products-carousel-prev",
      },
      breakpoints: {
        0: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 3,
        },
        991: {
          slidesPerView: 4,
        },
        1500: {
          slidesPerView: 6,
        },
      }
    });
  }

  // cart object
  const Cart = {
    items: [],

    addItem: function(product) {
      const existingItemIndex = this.items.findIndex(item => item.productId === product.productId);
      if (existingItemIndex !== -1) {
        // Update quantity
        this.items[existingItemIndex].quantity += product.quantity;
      } else {
        // Add new item
        this.items.push(product);
      }
    },

    getTotalQuantity: function() {
      return this.items.reduce((sum, item) => sum + item.quantity, 0);
    },

    getTotalAmount: function() {
      return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },

    clear: function() {
      this.items = [];
    }
  };

  function updateCartBadge() {
    const totalQuantity = Cart.getTotalQuantity();
    document.querySelectorAll('.cart-badge').forEach(badge => {
      badge.textContent = totalQuantity.toString();
    });
  }



  function updateCartDropdown() {
    const cartList = document.querySelector('.cart-list');
    cartList.innerHTML = '';

    Cart.items.forEach(item => {
      const itemSubtotal = (item.price * item.quantity).toFixed(2);

      // Capitalize all initials in the item name
      const capitalizedItemName = item.name.replace(/\b\w/g, char => char.toUpperCase());

      // Display unit
      const unitDisplay = `${item.quantity} ${item.unit}`;

      const listItem = `
        <li class="list-group-item d-flex justify-content-between lh-sm">
          <div>
            <h6 class="my-0">${capitalizedItemName}</h6>
            <small class="text-body-secondary">${unitDisplay}</small>
          </div>
          <span class="text-body-secondary">$${itemSubtotal}</span>
        </li>
      `;
      cartList.insertAdjacentHTML('beforeend', listItem);
    });

    // Add Total item
    const totalAmount = Cart.getTotalAmount();
    const totalItem = `
      <li class="list-group-item d-flex justify-content-between">
        <span>Total </span>
        <strong>$${totalAmount.toFixed(2)}</strong>
      </li>
    `;
    cartList.insertAdjacentHTML('beforeend', totalItem);
  }


  // Event listener for Add to Cart buttons
  document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function(event) {
      event.preventDefault();

      // Get product details
      const productId = this.getAttribute('data-product-id');
      const quantityInput = document.querySelector(`#quantity-${productId}`);
      const quantity = parseInt(quantityInput.value);
      const productElement = this.closest('.product-item');
      const price = parseFloat(productElement.getAttribute('data-product-price'));
      const name = productElement.querySelector('h3').textContent.trim();

      // Get the unit from the <span class="qty"> element
      const unitElement = productElement.querySelector('.qty');
      let unit = unitElement ? unitElement.textContent.trim() : '';
      // Extract the unit (e.g., '1 kg' -> 'kg')
      unit = unit.replace(/^\d+\s*/, '').toLowerCase();

      // Create product object
      const product = {
        productId: productId,
        name: name,
        price: price,
        quantity: quantity,
        unit: unit
      };

      // Add item to cart
      Cart.addItem(product);

      // Update badge and dropdown
      updateCartBadge();
      updateCartDropdown();

      // reset quantity input to 1
      quantityInput.value = 1;

      // Send data to the backend using fetch
      fetch('/customer/add_to_cart/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(product),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Cart updated on server:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });

    });
  });

  // Initialize the product quantity handlers
  function initProductQty() {

    $('.quantity-right-plus').click(function(e){
        e.preventDefault();
        var $el_product = $(this).closest('.product-qty');
        var $quantityInput = $el_product.find('input[name="quantity"]');
        var quantity = parseInt($quantityInput.val());
        $quantityInput.val(quantity + 1);
    });

    $('.quantity-left-minus').click(function(e){
        e.preventDefault();
        var $el_product = $(this).closest('.product-qty');
        var $quantityInput = $el_product.find('input[name="quantity"]');
        var quantity = parseInt($quantityInput.val());

        if(quantity > 1){
          $quantityInput.val(quantity - 1);
        }
    });
  }

  // check-out form validation
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })


  // payment section 

  function showPaymentFields() {
    var creditFields = $('#creditCardFields');
    var debitFields = $('#debitCardFields');
    var accountFields = $('#accountFields');

    var creditRadio = $('#credit');
    var debitRadio = $('#debit');
    var accountRadio = $('#account');

    if (creditRadio.is(':checked')) {
      creditFields.show();
      debitFields.hide();
      accountFields.hide();

      // Set required attributes for credit card fields
      $('#cc-number').attr('required', 'required');
      $('#cc-type').attr('required', 'required');
      $('#cc-expiration').attr('required', 'required');

      // Remove required attributes from other fields
      $('#debit-card-number').removeAttr('required');
      $('#bank-option').removeAttr('required');
      $('#other-bank-name').removeAttr('required');

    } else if (debitRadio.is(':checked')) {
      creditFields.hide();
      debitFields.show();
      accountFields.hide();

      // Set required attributes for debit card fields
      $('#debit-card-number').attr('required', 'required');
      $('#bank-option').attr('required', 'required');

      // Remove required attributes from other fields
      $('#cc-number').removeAttr('required');
      $('#cc-type').removeAttr('required');
      $('#cc-expiration').removeAttr('required');

      // Initialize bank-option change handler
      handleBankOptionChange();

    } else if (accountRadio.is(':checked')) {
      creditFields.hide();
      debitFields.hide();
      accountFields.show();

      // Remove required attributes from all card fields
      $('#cc-number').removeAttr('required');
      $('#cc-type').removeAttr('required');
      $('#cc-expiration').removeAttr('required');
      $('#debit-card-number').removeAttr('required');
      $('#bank-option').removeAttr('required');
      $('#other-bank-name').removeAttr('required');
    }
  }

  function handleBankOptionChange() {
    if ($('#bank-option').val() === 'others') {
      $('#other-bank-name-field').show();
      $('#other-bank-name').attr('required', 'required');
    } else {
      $('#other-bank-name-field').hide();
      $('#other-bank-name').removeAttr('required');
    }
  }


// Cart Summary
  function updateCartSummary() {
    var deliveryOption = $('#deliveryOption').val();
    var deliveryFee = 0;
    var deliveryLabel = '';

    if (deliveryOption === 'delivery') {
      deliveryFee = 10;
      deliveryLabel = 'Delivery';
    } else if (deliveryOption === 'pickup') {
      deliveryFee = 0;
      deliveryLabel = 'Pick up';
    } else {
      // Default when no option is selected
      deliveryFee = 0;
      deliveryLabel = 'Pick up';
    }

    // Update the delivery label and fee in the cart summary
    $('#deliveryLabel').text(deliveryLabel);
    $('#deliveryFee').text('$' + deliveryFee.toFixed(2));

    // Get the subtotal from a data attribute
    var subtotal = parseFloat($('#subtotal').data('subtotal'));

    // Check if subtotal is a valid number
    if (isNaN(subtotal)) {
      subtotal = 0;
    }

    // Calculate the new total
    var totalWithDelivery = subtotal + deliveryFee;

    // Update the total amount displayed
    $('#totalWithDelivery').text('$' + totalWithDelivery.toFixed(2));
  }


  // init jarallax parallax
  var initJarallax = function() {
    jarallax(document.querySelectorAll(".jarallax"));

    jarallax(document.querySelectorAll(".jarallax-keep-img"), {
      keepImg: true,
    });
  }

  // document ready
  $(document).ready(function() {
    
    initPreloader();
    initSwiper();
    initProductQty();
    initJarallax();
    initChocolat();
    showPaymentFields();
    $('input[name="paymentMethod"]').on('change', showPaymentFields);
    // Bind change event to bank-option
    $('#bank-option').on('change', handleBankOptionChange);
    // Initialize the visibility of other-bank-name-field
    handleBankOptionChange();

    // Initialize the cart summary when the page loads
    updateCartSummary();

    // Listen for changes on the delivery option dropdown
    $('#deliveryOption').on('change', function() {
      updateCartSummary();
    });

  });

})(jQuery);