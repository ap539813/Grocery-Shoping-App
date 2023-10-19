<template>
    <div>
      <nav class="navbar">
          <div class="navbar-left">
              <span id="admin-username">{{ adminUsername }}'s Dashboard</span>
          </div>
          <div class="navbar-right">
              <button style="text-decoration:none" @click="navigateToSummary">Summary</button>
              <button style="text-decoration:none" @click="logout">Logout</button>
          </div>
      </nav>
    </div>
    <div>
      <button @click="showRequests = !showRequests">Toggle Pending Requests</button>
      
      <div v-if="showRequests">
        <table>
          <thead>
            <tr>
              <th>Username</th>
              <th>Category</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id">
              <td>{{ request.username }}</td>
              <td>{{ request.category }}</td>
              <td><button @click="approveRequest(request.id)">Approve</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

      <div>
        <div id="categories-container">
            <div v-for="category in categories" :key="category.id" class="category-div" :id="category.id">
                <h2>{{ category.name }}</h2>
                <button class="edit-btn" @click="showEditCategoryPopup(category)">Edit</button>
                <button class="delete-btn" @click="deleteCategory(category.id)">Delete</button>
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
        requests: [],
        showRequests: false,
        adminUsername: '',
          categories: [],
          isCreateCategoryVisible: false,
          isEditCategoryVisible: false,
          newCategoryName: '',
          editingCategory: {
              id: null,
              name: ''
          },
      };
    },
    methods: {
      async fetchPendingRequests() {
        try {
            let response = await fetch("http://127.0.0.1:5000/pending-requests");
            let data = await response.json();
            this.requests = data.requests;
            this.categories = data.categories;
            this.adminUsername = data.admin;
        } catch (error) {
            console.error("Error fetching pending requests:", error);
        }
        },
      async approveRequest(requestId) {
        try {
          let response = await fetch(`http://127.0.0.1:5000/approve-request/${requestId}`, {
            method: "POST"
          });
          let data = await response.json();
          if (data.status === "success") {
            this.requests = this.requests.filter(request => request.id !== requestId);
          } else {
            console.error("Error approving request:", data.message);
          }
        } catch (error) {
          console.error("Error approving request:", error);
        }
      },
      async fetchUserAndCategories(){
        try {
              let response = await fetch("http://127.0.0.1:5000/categories", {
                  method: 'GET',
                  credentials: 'include'
              });
              let data = await response.json();
              console.log(data)
              this.categories = data.categories;
              this.managerUsername = data.manager;
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
      async saveCategory() {
          try {
              const response = await fetch('http://127.0.0.1:5000/save_category', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json;charset=UTF-8'
                  },
                  body: JSON.stringify({
                      'category_name': this.newCategoryName
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

    },
    mounted() {
      this.fetchPendingRequests();
    }
  };
  </script>
  
  <style scoped>
  /* You can add your table styling here */
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
  }
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

        #admin-username {
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
  </style>
  