<template>
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
  </template>
  
  <script>
  export default {
    data() {
      return {
        requests: [],
        showRequests: false
      };
    },
    methods: {
      async fetchPendingRequests() {
        try {
            let response = await fetch("http://127.0.0.1:5000/pending-requests");
            let data = await response.json();
            this.requests = data.requests;
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
            // Remove approved request from the list
            this.requests = this.requests.filter(request => request.id !== requestId);
          } else {
            console.error("Error approving request:", data.message);
          }
        } catch (error) {
          console.error("Error approving request:", error);
        }
      }
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
  </style>
  