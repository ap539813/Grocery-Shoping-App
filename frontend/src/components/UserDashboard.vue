<template>
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-left">
        <span id="manager-username">{{ username }}'s Dashboard</span>
      </div>
      <div class="navbar-right">
        <button @click="goToCart">Cart</button>
        <button @click="logout">Logout</button>
      </div>
    </nav>
  
    <div class="container">
      <div v-for="category in categories" :key="category.name" class="category-block">
        <h2>{{ category.name }}</h2>
        <div class="category-block-inner">
          <div v-for="product in category.products" :key="product.id" class="product-block">
            <div class="product-info">
              <span>{{ product.name }}</span>
              <span class="product-price">{{ product.rate }}/{{ product.unit }}</span>
            </div>
            <div class="product-actions">
              <button v-if="product.quantity > 0" class="buy-btn" @click="showBuyPopup(product.rate, product.id)">Buy</button>
              <button v-if="product.quantity > 0" class="cart-btn" @click="showCartPopup(product.rate, product.id)">Add to Cart</button>
              <label v-else class="out-of-stock">Out of Stock</label>
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Buy Product Popup -->
    <div v-if="buyPopupVisible" class="popup">
      <div class="popup-content">
        <span class="close-btn" @click="closeBuyPopup">&times;</span>
        <h3>Buying Product</h3>
        <div class="popup-input">
          <label for="product-quantity">Quantity:</label>
          <input type="number" id="product-quantity" v-model.number="buyQuantity" @change="updateTotalPrice">
        </div>
        <div class="popup-price">
          Total Price: &#8377;<span id="total-price">{{ totalPrice }}</span>
        </div>
        <button @click="finalizePurchase">Buy</button>
      </div>
    </div>
  
    <!-- Add to Cart Popup -->
    <div v-if="cartPopupVisible" class="popup">
      <div class="popup-content">
        <span class="close-btn" @click="closeCartPopup">&times;</span>
        <h3>Adding to Cart</h3>
        <div class="popup-input">
          <label for="cart-product-quantity">Quantity:</label>
          <input type="number" id="cart-product-quantity" v-model.number="cartQuantity" @change="updateCartTotalPrice">
        </div>
        <div class="popup-price">
          Total Price: &#8377;<span id="cart-total-price">{{ cartTotalPrice }}</span>
        </div>
        <button @click="addToCartFinalizePurchase">Add to Cart</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: 'User', // Replace with dynamic data
        categories: [], // Populate with data from your API
        buyPopupVisible: false,
        cartPopupVisible: false,
        selectedProduct: null,
        buyQuantity: 1,
        cartQuantity: 1,
        totalPrice: 0,
        cartTotalPrice: 0
      };
    },
    methods: {
        async fetchUserAndCategories(){
        try {
            let response = await fetch(`http://127.0.0.1:5000/categories_user?username=${this.$route.query.username}`, {
                method: 'GET',
                credentials: 'include'
            });
            console.log(response.status);
            if (response.status === 401 || response.status === 404) {
                this.$router.push({ name: 'LoginUser' })
            }

            let data = await response.json();
            console.log(data)
            
            if (data.categories && data.user) { // Added check to make sure data is present
                this.categories = data.categories;
                this.username = data.user;
            } else {
                console.error("Unexpected response data:", data);
            }

        } catch (error) {
            console.error("Error fetching pending requests:", error);
        }
    },
      goToCart() {
        this.$router.push({ name: 'cart' });
      },
      async logout() {
        // this.$router.push({ name: 'Home' });
        await fetch(`http://127.0.0.1:5000/logout?username=${this.$route.query.username}`, {
                method: 'GET',
                credentials: 'include'
            });
            this.$router.push({ name: 'Home' });
            return;
      },
      showBuyPopup(product) {
        this.selectedProduct = product;
        this.totalPrice = product.rate;
        this.buyPopupVisible = true;
      },
      closeBuyPopup() {
        this.buyPopupVisible = false;
      },
      updateTotalPrice() {
        this.totalPrice = (this.selectedProduct.rate * this.buyQuantity).toFixed(2);
      },
      finalizePurchase() {
        // Replace with your API call using Axios or fetch
      },
      showCartPopup(product) {
        this.selectedProduct = product;
        this.cartTotalPrice = product.rate;
        this.cartPopupVisible = true;
      },
      closeCartPopup() {
        this.cartPopupVisible = false;
      },
      updateCartTotalPrice() {
        this.cartTotalPrice = (this.selectedProduct.rate * this.cartQuantity).toFixed(2);
      },
      addToCartFinalizePurchase() {
        // Replace with your API call using Axios or fetch
      }
    },
    mounted() {
      this.fetchUserAndCategories();
    }
  };
  </script>
  
  <style scoped>
        .container {
            width: 80%;
            margin: 20px auto;
            font-family: Arial, sans-serif;
        }

        .category-block {
            background-color: #e6f7ff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
        }

        .category-block-inner {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }

        .product-block {
            background-color: #fffae6;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            width: 25%
        }

        .product-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .product-price {
            margin-left: 10px;
            color: #444;
            font-weight: bold;
        }

        .product-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }

        .buy-btn, .cart-btn {
            padding: 5px 15px;
            cursor: pointer;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }

        .buy-btn {
            background-color: #4CAF50;
            color: white;
        }

        .cart-btn {
            background-color: #FFC107;
            color: white;
        }

        .popup {
            display: none;
            position: fixed; 
            top: 0; 
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            z-index: 1000;
        }

        .popup-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            width: 300px;
            border-radius: 5px;
        }

        .close-btn {
            cursor: pointer;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }

        .popup-input, .popup-price {
            margin: 20px 0;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #333;
            color: white;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
            position: fixed; 
            top: 0; 
            left: 0;  
            width: 100%; 
            z-index: 1000;
            box-sizing: border-box; 
            padding-right: 15px;
        }

        .navbar-left, .navbar-right {
            display: flex;
            align-items: center;
        }

        #manager-username {
            margin-right: 20px;
            font-weight: bold;
        }

        .navbar button {
            margin-left: 10px;
            padding: 5px 15px;
            background-color: #555;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .navbar button:hover {
            background-color: #777;
        }

        body {
            padding-top: 60px;
        }

  </style>
  