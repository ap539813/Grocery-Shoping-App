<template>
  <div>
    <!-- Bootstrap Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="navbar-brand">
        <span id="admin-username">{{ adminUsername }}'s Dashboard</span>
      </div>
      <div class="ml-auto">
        <button class="btn btn-outline-primary" @click="logout">Logout</button>
      </div>
    </nav>

    <div class="container mt-5">
      <button class="btn btn-primary mb-3 position-relative" @click="showRequests = !showRequests">
        Pending Requests
        <span class="badge-number">{{ numberOfPendingRequests }}</span>
      </button>
      <div v-if="showRequests">
        <!-- Bootstrap Table -->
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Username</th>
              <th>Category</th>
              <th>Action</th>
              <th>Approve Request</th>
              <th>Decline Request</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id">
              <td>{{ request.username }}</td>
              <td>{{ request.category }}</td>
              <td>{{ request.action }}</td>
              <td><button class="btn btn-success" @click="approveRequest(request.id)">Approve</button></td>
              <td><button class="btn btn-danger" @click="declineRequest(request.id)">Decline</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div id="categories-container" class="container mt-3">
      <div v-for="category in categories" :key="category.id" class="category-div" :id="category.id">
        <h2>{{ category.name }}</h2>
        <button class="btn btn-warning edit-btn" @click="showEditCategoryPopup(category.id)">Edit</button>
        <button class="btn btn-danger delete-btn" @click="deleteCategory(category.id)">Delete</button>
      </div>

      <button id="openBtn" class="btn btn-primary" @click="showCreateCategoryPopup()">Create Category</button>
    </div>

    <!-- Create Category Modal -->
  <div v-if="isCreateCategoryVisible" id="create-category-overlay">
    <div id="create-category-popup">
      <button class="close-btn" @click="isCreateCategoryVisible = false">&times;</button>
      <input type="text" v-model="newCategoryName" placeholder="Create a category">
      <button id="saveBtn" class="btn btn-primary" @click="saveCategory">Save</button>
    </div>
  </div>

  <!-- Edit Category Modal -->
  <div v-if="isEditCategoryVisible" id="edit-category-overlay">
    <div id="edit-category-popup">
      <button class="close-btn" @click="isEditCategoryVisible = false">&times;</button>
      <input type="hidden" v-model="categoryId" id="editing-category-id-hidden" name="category_name">
      <input type="text" id="new-category-name" placeholder="Edit category name">
      <button id="updateBtn" class="btn btn-primary" @click="updateCategory">Update</button>
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
          numberOfPendingRequests: 0,
          categoryId: null,
      };
    },
    methods: {
      async fetchPendingRequests() {
        try {
            let response = await fetch(`http://127.0.0.1:5000/pending-requests?username=${this.$route.query.username}`, {
                method: 'GET',
                credentials: 'include'
            });
            console.log(response.status);
            if (response.status === 401 || response.status === 404) {
                this.$router.push({ name: 'LoginAdmin' })
            }
            let data = await response.json();
            this.requests = data.requests;
            this.categories = data.categories;
            this.adminUsername = data.admin;
            this.numberOfPendingRequests = this.requests.length;
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
            window.location.reload();
          } else {
            console.error("Error approving request:", data.message);
          }
        } catch (error) {
          console.error("Error approving request:", error);
        }
      },
      async declineRequest(requestId) {
        try {
          let response = await fetch(`http://127.0.0.1:5000/decline-request/${requestId}`, {
            method: "POST"
          });
          let data = await response.json();
          if (data.status === "success") {
            this.requests = this.requests.filter(request => request.id !== requestId);
            window.location.reload();
          } else {
            console.error("Error declining request:", data.message);
          }
        } catch (error) {
          console.error("Error declining request:", error);
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
                    alert(data.message);
                    window.location.reload();
                    
                } else {
                    alert(data.message);
                    console.log(this.editingCategory.id);
                }
            })
            .catch(error => {
                console.error("There was an error saving the product:", error);
            });
            this.hideEditCategoryPopup();
        },
        async logout() {
        await fetch(`http://127.0.0.1:5000/logout?username=${this.$route.query.username}`, {
                method: 'GET',
                credentials: 'include'
            });
            this.$router.push({ name: 'Home' });
            return;
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
      .badge-number {
        position: absolute;
        top: -10px; /* Adjust these values as needed */
        right: -10px;
        width: 20px; /* Badge size */
        height: 20px;
        background-color: red;
        color: white;
        border-radius: 50%; /* Circular shape */
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 12px; /* Font size of the number */
      }

            #create-category-overlay, #edit-category-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1;
      }

  /* Popup Styles */
        #create-category-popup, #edit-category-popup {
          position: relative;
          top: 50%;
          left: 50%;
          width: 300px;
          padding: 20px;
          transform: translate(-50%, -50%);
          background-color: #fff;
          text-align: center;
          border-radius: 10px;
          /* Increased padding at bottom */
        }

        /* Close Button Styles */
        .close-btn {
          position: absolute;
          top: 10px;
          right: 10px;
          border: none;
          background-color: transparent;
          cursor: pointer;
          font-size: 20px;
        }

        /* Input and Button Spacing */
        input[type="text"] {
          margin-bottom: 15px; /* Add margin to create space */
        }

        #categories-container {
            display: flex;
            align-items: left;
            justify-content: center;
            flex-wrap: wrap;
        }

        .category-div {
            width: 300px; 
            height: 160px; 
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

        /* #edit-category-overlay {
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
        } */

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
  