<template>
  <div>
      <!-- Navigation Bar -->
      <nav class="navbar">
          <div class="navbar-left">
              <span id="manager-username">{{ managerUsername }}'s Dashboard</span>
          </div>
          <div class="navbar-right">
              <button style="text-decoration:none" @click="navigateToSummary">Summary</button>
              <button style="text-decoration:none" @click="logout">Logout</button>
          </div>
      </nav>

      <div id="categories-container">
          <div v-for="category in categories" :key="category.id" class="category-div" :id="category.id">
              <h2>{{ category.name }}</h2>
              
              <div class="products-container">
                  <div v-for="product in category.products" :key="product.id" class="product-div" :id="'product-' + product.id">
                      <span>{{ product.name }}</span>
                      <button @click="showEditProductPopup(product.id, product.name, product.unit, product.rate, product.quantity)">Edit</button>
                      <button @click="deleteProduct(product.id)">Delete</button>
                  </div>
              </div>

              <button class="add-btn" @click="showAddProductPopup(category.id)">+</button>
              <br><br>
              <button class="edit-btn" @click="showEditCategoryPopup(category.id)">Edit</button>
              <button class="delete-btn" @click="deleteCategory(category.id)">Delete</button>
          </div>
      </div>

      <div v-if="isCreateProductVisible" id="add-product-overlay">
        <div id="add-product-popup">
        <h3>Add Product</h3>
        <form id="add-product-form">
            <input type="hidden" v-model="categoryId" id="category-id-hidden" name="category_name">
            <input type="text" id="product-name-input" name="product_name" placeholder="Product Name" required>
            <input type="text" id="unit-input" name="unit" placeholder="Unit" required>
            <input type="number" id="rate-input" name="rate" placeholder="Rate" required>
            <input type="number" id="quantity-input" name="quantity" placeholder="Quantity" required>
            <input type="date" id="mfd-input" name="mfd" placeholder="Manufacturing Date" required>
            <button type="button" @click="saveProduct()">Save</button>
        </form>
    </div>
    </div>

    <div v-if="isEditProductVisible" id="edit-product-overlay">
        <div id="edit-product-popup">
        <h3>Edit Product</h3>
        <form id="edit-product-form">
            <input type = "hidden" v-model="productId" id = "edit-product-id-hidden" name="product_id">
            <input type="text" v-model="productName" id="edit-product-name-input" name="product_name" placeholder="Product Name" required>
            <input type="text" v-model="productUnit" id="edit-unit-input" name="unit" placeholder="Unit" required>
            <input type="number" v-model="productRate" id="edit-rate-input" name="rate" placeholder="Rate" required>
            <input type="number" v-model="productQuantity" id="edit-quantity-input" name="quantity" placeholder="Quantity" required>
            <input type="date" v-model="productDate" id="edit-mfd-input" name="mfd" placeholder="Manufacturing Date" required>
            <button type="button" @click="editProduct()">Save</button>
        </form>
    </div>
    </div>

    <button id="openBtn" @click = "showCreateCategoryPopup()">Create Category</button>

    <!-- Create Category Modal -->
    <div v-if="isCreateCategoryVisible" id="create-category-overlay">
        <div id="create-category-popup">
            <input type="text" v-model="newCategoryName" placeholder="Create a category">
            <button id="saveBtn" @click="saveCategory">Save</button>
        </div>
    </div>

    <!-- Edit Category Modal -->
    <div v-if="isEditCategoryVisible" id="edit-category-overlay">
        <div id="edit-category-popup">
            <input type="hidden" v-model="categoryId" id="editing-category-id-hidden" name="category_name">
            <input type="text" id = "new-category-name" placeholder="Edit category name">
            <button id="updateBtn" @click="updateCategory">Update</button>
        </div>
    </div>

  </div>
</template>

<script>
export default {
  data() {
      return {
          managerUsername: '',
          categories: [],
          isCreateCategoryVisible: false,
          isEditCategoryVisible: false,
          newCategoryName: '',
          isCreateProductVisible: false,
          isEditProductVisible: false,
          editingCategory: {
              id: null,
              name: ''
          },
          categoryId: null,
          product: {
            product_id: '',
            category_id: '',
            product_name: '',
            unit: '',
            rate: '',
            quantity: '',
            mfd: ''
        },
        productId: '',
        productName: '',
        productUnit: '',
        productRate: '',
        productQuantity: '',
        productDate: ''
      };
  },
  methods: {
    // async fetchUserAndCategories(){
    //   try {
    //         let response = await fetch("http://127.0.0.1:5000/categories", {
    //             method: 'GET',
    //             credentials: 'include'
    //         });
    //         let data = await response.json();
    //         console.log(data)
    //         this.categories = data.categories;
    //         this.managerUsername = data.manager;
    //     } catch (error) {
    //         console.error("Error fetching pending requests:", error);
    //     }
    // },

    // async fetchUserAndCategories(){
    // try {
    //         let response = await fetch(`http://127.0.0.1:5000/categories?username=${this.$route.query.username}`, {
    //             method: 'GET',
    //             credentials: 'include'
    //         });
    //         let data = await response.json();
    //         console.log(data)
    //         this.categories = data.categories;
    //         this.managerUsername = data.manager;
    //     } catch (error) {
    //         console.error("Error fetching pending requests:", error);
    //     }
    // },

    async fetchUserAndCategories(){
        try {
            let response = await fetch(`http://127.0.0.1:5000/categories?username=${this.$route.query.username}`, {
                method: 'GET',
                credentials: 'include'
            });
            console.log(response.status);
            if (response.status === 401 || response.status === 404) { // If unauthorized
                this.$router.push({ name: 'LoginManager' })
            }

            let data = await response.json();
            console.log(data)
            
            if (data.categories && data.manager) { // Added check to make sure data is present
                this.categories = data.categories;
                this.managerUsername = data.manager;
            } else {
                console.error("Unexpected response data:", data);
            }

        } catch (error) {
            console.error("Error fetching pending requests:", error);
        }
    },

    showCreateCategoryPopup() {
        this.isCreateCategoryVisible = true;
    },
    hideCreateCategoryPopup() {
        this.isCreateCategoryVisible = false;
    },
    showEditCategoryPopup(categoryId) {
        this.categoryId = categoryId;
        this.isEditCategoryVisible = true;
    },
    hideEditCategoryPopup() {
        this.isEditCategoryVisible = false;
    },
    showAddProductPopup(categoryId) {
        this.categoryId = categoryId;
        this.isCreateProductVisible = true;
      },
      hideAddProductPopup() {
         this.isCreateProductVisible = false;
      },
        async saveCategory() {
            try {
                const response = await fetch('http://127.0.0.1:5000/create_category_request', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json;charset=UTF-8'
                    },
                    body: JSON.stringify({
                        'category': this.newCategoryName,
                        'username': this.managerUsername
                    })
                });
                
                const data = await response.json();
                
                if (data.status === "success") {
                    alert(data.message);
                    window.location.reload();
                } else {
                console.error("Error saving category:", data.message);
                }
            } catch (error) {
            console.error("Error saving category:", error);
            }
            this.hideCreateCategoryPopup();
        },
      saveProduct() {
            this.product.category_id = document.getElementById("category-id-hidden").value;
            this.product.product_name = document.getElementById("product-name-input").value;
            this.product.unit = document.getElementById("unit-input").value;
            this.product.rate = parseFloat(document.getElementById("rate-input").value);
            this.product.quantity = parseInt(document.getElementById("quantity-input").value);
            this.product.mfd = document.getElementById("mfd-input").value;
            
            fetch('http://127.0.0.1:5000/save_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.product)
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Product saved successfully!');
                    window.location.reload();
                    
                } else {
                    alert('Error saving product!');
                }
            })
            .catch(error => {
                console.error("There was an error saving the product:", error);
            });
            this.hideAddProductPopup();
        },

        updateCategory() {
            this.editingCategory.id = document.getElementById("editing-category-id-hidden").value;
            this.editingCategory.name = document.getElementById("new-category-name").value;
            console.log(JSON.stringify(this.editingCategory))
            fetch('http://127.0.0.1:5000/update_category', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.editingCategory)
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Product saved successfully!');
                    window.location.reload();
                    
                } else {
                    alert('Error saving product!');
                }
            })
            .catch(error => {
                console.error("There was an error saving the product:", error);
            });
            this.hideAddProductPopup();
        },
        editProduct() {
            this.product.product_id = document.getElementById("edit-product-id-hidden").value;
            this.product.product_name = document.getElementById("edit-product-name-input").value;
            this.product.unit = document.getElementById("edit-unit-input").value;
            this.product.rate = parseFloat(document.getElementById("edit-rate-input").value);
            this.product.quantity = parseInt(document.getElementById("edit-quantity-input").value);
            this.product.mfd = document.getElementById("edit-mfd-input").value;
            
            fetch('http://127.0.0.1:5000/edit_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.product)
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Product updated successfully!');
                    window.location.reload();
                    
                } else {
                    alert('Error updating product!');
                }
            })
            .catch(error => {
                console.error("There was an error updating the product:", error);
            });
            this.hideEditProductPopup();
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
      showEditProductPopup(productId, productName, productUnit, productRate, productQuantity, productDate) {
          this.isEditProductVisible = true;
          this.productId = productId;
          this.productName = productName;
          this.productUnit = productUnit;
          this.productRate = productRate;
          this.productQuantity = productQuantity;
          this.productDate = productDate;
      },
      hideEditProductPopup() {
          this.isEditProductVisible = true;
      },
      deleteProduct(productId) {
        fetch('http://127.0.0.1:5000/delete_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                        'product_id': productId
                    })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Product deleted successfully!');
                    window.location.reload();
                    
                } else {
                    alert('Error deleting product!');
                }
            })
            .catch(error => {
                console.error("There was an error deleting the product:", error);
            });
      },
      deleteCategory(categoryId) {
        fetch('http://127.0.0.1:5000/delete_category', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                        'category_id': categoryId
                    })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert('Category deleted successfully!');
                    window.location.reload();
                    
                } else {
                    alert('Error deleting category!');
                }
            })
            .catch(error => {
                console.error("There was an error deleting the category:", error);
            });
      },
    },
  mounted() {
      this.fetchUserAndCategories();
    }
};
</script>

<style>
#create-category-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1;
        }

        #create-category-popup {
            position: relative;
            top: 50%;
            left: 50%;
            width: 300px;
            padding: 20px;
            transform: translate(-50%, -50%);
            background-color: #fff;
            text-align: center;
            border-radius: 10px;
        }

        #categories-container {
            display: flex;
            align-items: left;
            justify-content: center;
            flex-wrap: wrap;
        }

        .category-div {
            width: 300px; 
            height: 300px; 
            margin: 60px auto; 
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1), 0px 6px 20px rgba(0, 0, 0, 0.13); 
            overflow-y: auto; 
            padding: 20px;
            border-radius: 8px; 
            background-color: #ffffff;
            text-align: center;
            vertical-align: top;
            position: relative;
        }

        #edit-category-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1;
        }

        #edit-category-popup {
            position: relative;
            top: 50%;
            left: 50%;
            width: 300px;
            padding: 20px;
            transform: translate(-50%, -50%);
            background-color: #fff;
            text-align: center;
            border-radius: 10px;
        }

        #add-product-overlay{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1;
        }

        #edit-product-overlay{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1;
        }

        #add-product-popup{
            position: relative;
            top: 50%;
            left: 50%;
            width: 300px;
            padding: 20px;
            transform: translate(-50%, -50%);
            background-color: #fff;
            text-align: center;
            border-radius: 10px;
        }

        #edit-product-popup{
            position: relative;
            top: 50%;
            left: 50%;
            width: 300px;
            padding: 20px;
            transform: translate(-50%, -50%);
            background-color: #fff;
            text-align: center;
            border-radius: 10px;
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

        #openBtn {
            position: fixed;  
            bottom: 20px;       
            right: 20px;      
            background-color: #008CBA; 
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 50px; 
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease-in-out;
            z-index: 1000;  
        }

        #openBtn:hover {
            background-color: #006c99;
        }

        .category-div button.add-btn {
            background-color: #008CBA; 
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            position: relative;
            margin-top: 10px;
        }

        .category-div button.add-btn:hover {
            cursor: pointer;
        }

        .category-div button.add-btn::before {
            content: '+';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-weight: bold;
        }

        .category-div button.edit-btn, .category-div button.delete-btn {
            width: 80px; 
            height: 35px; 
            line-height: 35px; 
            border: none;
            border-radius: 15px; 
            display: inline-block; 
            font-size: 14px;
            text-align: center;
            margin-top: 10px;
            position: absolute; 
            bottom: 10px;
        }

        .category-div button.edit-btn, .category-div button.delete-btn:hover {
            cursor: pointer;
        }

        .category-div button.edit-btn {
            background-color: #ffeb85; 
            left: 40px;
        }

        .category-div button.delete-btn {
            background-color: #ffb3b3; 
            right: 40px;
        }

        .products-container {
            height: 40%;
            overflow-y: auto; 
            padding: 10px; 
            border-radius: 5px; 
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .product-div {
            display: flex; 
            justify-content: space-between;
            align-items: center;
            padding: 10px; 
            border-bottom: 1px solid #e1e1e1;
        }

        .product-div:last-child {
            border-bottom: none;
        }

        .product-div span {
            flex: 1;
            font-size: 16px;
            text-align: left;
            margin-right: 10px;
        }

        .product-div button {
            margin: 0 5px;
            padding: 5px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }

        .product-div button:hover {
            opacity: 0.8;
            cursor: pointer;
        }

        .product-div button:nth-child(2) {
            background-color: #d1ffd1;
        }

        .product-div button:nth-child(3) {
            background-color: #ffc1c1;
        }
</style>
