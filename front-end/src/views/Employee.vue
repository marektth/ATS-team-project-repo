<template>
  <nc-container>
     <nc-layout horizontal>
       <nc-layout-aside>

         <nc-button id="OpenFormButton" @click="openForm">Register timeoff</nc-button>

         <nc-form class="user-form" v-if="this.showForm == 1">

          <!-- <div class="form-group">
            <label for="Name">Start date</label>
            <nc-datepicker v-model="timeoffRequestForm.startDate" disable-past-days/>
          </div> -->

          <div class="form-group">
            <label for="Name">Date of time off</label>
            <nc-datepicker v-model="timeoffRequestForm.endDate" disable-past-days/>
          </div>

          <div class="form-group">
            <label for="Name">Code leave reason</label>
            <input class="form-control" type="text" id="CodeLeaveReasonID" placeholder="Enter code leave reason" v-model="timeoffRequestForm.codeLeaveReason" />
          </div>

          <div class="form-group">
            <label for="Name">Reason</label>
            <input class="form-control" type="text" id="ReasonID" placeholder="Enter reason" v-model="timeoffRequestForm.leaveReason" />
          </div>
          
          <nc-button id="FormSubmitButton"  @click.prevent="requestTimeoff">Request timeoff</nc-button>
        </nc-form>
       </nc-layout-aside>
      <nc-layout-content>

        <nc-table class="data-table" v-if="this.requests.length > 0">
          <thead>
            <nc-table-row>
              <th scope="col">#</th>
              <th scope="col">Request ID</th>
              <th scope="col">Employee ID</th>
              <th scope="col">Date Of Absence</th>
              <th scope="col">Absence Type Code</th>
              <th scope="col">Leave Reason</th>
              <th scope="col">Status</th>
              <th scope="col">Action</th>
            </nc-table-row>
          </thead>
          <tbody v-for="(request,idx) in requests" v-bind:key="String(request.EmployeeID) + '_'+ String(idx)">
            <nc-table-row>
              <td>{{ idx + 1 }}</td>
              <td>{{ request.id }}</td>
              <td>{{ request.EmployeeID }}</td>
              <td>{{ request.DateOfAbsence }}</td>
              <td>{{ request.AbsenceTypeCode }}</td>
              <td>{{ request.LeaveReason }}</td>
              <td>{{ request.Status }}</td>
              <td><a @click.prevent="deleteTimeoff(request.id)">Delete</a></td>
            </nc-table-row>
          </tbody>
        </nc-table>
        <h1 v-else>No data</h1>
      </nc-layout-content>
    </nc-layout>
  </nc-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { ApiService, EmployeeTimeoff, TimeoffRequest } from '../services/api'

export default Vue.extend({
  name: 'Home',
  components: {

  },
  data: function () {
    return {
      employeeID: 192,
      showForm: 0,
      timeoffRequestForm: {
        endDate: new Date(),
        codeLeaveReason: "" as string,
        leaveReason: "" as string,
      } as TimeoffRequest,
      requests: [] as EmployeeTimeoff[]
      }
  }, 
  async created(){
    this.getEmployeeData()
  },
  methods: {

    async getEmployeeData() {
      
      const api = new ApiService(this.employeeID)
      //const response = await api.requestTimeoffDELETE(10)
      const response:EmployeeTimeoff[] = await api.employeeTimeoffRequestsGET()
      console.log(response)
      if(this.requests.length > 0){
        this.requests = []
      }

      if (response.length > 0){
        response.forEach(request => {
          this.requests.push(request)
        });
      }
    },
    async requestTimeoff(){
      // request time off from form
      const api = new ApiService(this.employeeID)
      const response = await api.requestTimeoffPOST(this.timeoffRequestForm)
      console.log(response)
      this.getEmployeeData()
      this.clearFormInputs()
    },
    async deleteTimeoff(id:number){
      const confirmation = prompt(`If you want to delete your request enter: DELETE ${id}`);
      if(confirmation === `DELETE ${id}`){
        const api = new ApiService(this.employeeID)
        const response = await api.requestTimeoffDELETE(id)
        console.log(response)
        this.getEmployeeData()
      }
    },
    
    // helper functions

    loadDataToTable(res : any){
      // load to table
    },
    clearFormInputs(){
      // form clear
      this.timeoffRequestForm.endDate = new Date()
      this.timeoffRequestForm.codeLeaveReason = ""
      this.timeoffRequestForm.leaveReason = ""
      
    },
    
    // actions
    
    openForm(){
      if (this.showForm == 0) {
        this.showForm = 1
      } else {
        this.showForm = 0
      }
    }
  }
  
});
</script>

<style scoped>
.data-table {
  padding: 0 1em 0 1em;
  color: black;
}

.user-form {
  padding: 1em;
}
</style>