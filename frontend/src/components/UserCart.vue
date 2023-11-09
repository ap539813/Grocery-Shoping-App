<template>
    <div>
      <!-- Navigation Bar -->
      <nav class="navbar">
        <div class="navbar-left">
          <span id="manager-username">{{ username }}'s Dashboard</span>
        </div>
        <div class="navbar-right">
          <button @click="goToHomepage()">Home</button>
          <button @click="logout()">Logout</button>
        </div>
      </nav>
  
      <div id="cart-container">
        <input type="hidden" id="hidden-user-id" :value="userId">
        <div class="cart-item" v-for="item in items" :key="item.id">
          <span>{{ item.category }} - {{ item.product_name }}</span>
          <span>{{ item.quantity }} {{ item.unit }}</span>
          <span>Rate: &#8377;{{ item.rate }} / {{ item.unit }}</span>
          <span class="item-total" :data-item-total="item.rate * item.quantity">Total: &#8377;{{ item.rate * item.quantity }}</span>
          <button class="remove-button" @click="removeItem(item.id)">Remove</button>
        </div>
      </div>
  
      <div class="grand-total-section">
        <span class="grand-total-display">Grand Total: &#8377;{{ grandTotal }}</span>
        <button class="buy-all-button" @click="buyAll">Buy All</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: 'User', 
        userId: '', 
        items: [],
        grandTotal: 0,
        dashboardUrl: '',
        logoutUrl: '',
      };
    },
    mounted() {
      this.getDataAndcalculateGrandTotal();
    },
    methods: {
      async getDataAndcalculateGrandTotal() {
        try {
          let response = await fetch(`http://127.0.0.1:5000/cart?username=${this.$route.query.username}`, {
                method: 'GET',
                credentials: 'include'
            });
            console.log(response.status);
            if (response.status === 401 || response.status === 404) {
                this.$router.push({ name: 'LoginUser' })
            }

            let data = await response.json();
            console.log(data);
            
            if (data.items && data.user) {
                this.items = data.items;
                this.username = data.user;
            } else {
                console.error("Unexpected response data:", data);
            }

        } catch (error) {
            console.error("Error fetching pending requests:", error);
        }


        this.grandTotal = this.items.reduce((total, item) => total + (item.rate * item.quantity), 0);
      },
      buyAll() {
        fetch('http://127.0.0.1:5000/buy_all', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: this.userId
          })
        })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          location.reload();
        })
        .catch(error => {
          alert(error);
        });
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
      goToHomepage(){
            this.$router.push({ name: 'UserDashboard', query: { username: this.username } });
      },
      removeItem(itemId) {
        fetch('http://127.0.0.1:5000/remove_item', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            item_id: itemId
          })
        })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          location.reload();
        })
        .catch(error => {
            alert(error);
        });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Your CSS styles here */
  </style>
  