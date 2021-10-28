<template>
  <nc-container>
     <nc-layout horizontal>
       <nc-layout-aside>

         <nc-button @click="openForm">Register timeoff</nc-button>

         <nc-form class="user-form" v-if="this.showForm == 1">

          <div class="form-group">
            <label for="Name">Person number</label>
            <input class="form-control" type="number" id="PersonNumberID" placeholder="Enter person number" v-model="timeoffRequestForm.personNumber" />
          </div>

          <div class="form-group">
            <label for="Name">Employment number</label>
            <input class="form-control" type="number" id="EmploymentNumberID" placeholder="Enter employment number" v-model="timeoffRequestForm.employmentNumber" />
          </div>

          <div class="form-group">
            <label for="Name">Leave type code</label>
            <input class="form-control" type="text" id="LeaveTypeCodeID" placeholder="Enter leave type code" v-model="timeoffRequestForm.leaveTypeCode" />
          </div>

          <div class="form-group">
            <label for="Name">Leave year</label>
            <input class="form-control" type="text" id="LeaveYearID" placeholder="Enter leave year" v-model="timeoffRequestForm.leaveYear" />
          </div>

          <div class="form-group">
            <label for="Name">Start date</label>
            <input class="form-control" type="text" id="StartDateID" placeholder="Enter start date" v-model="timeoffRequestForm.startDate" />
          </div>

          <div class="form-group">
            <label for="Name">End date</label>
            <input class="form-control" type="text" id="EndDateID" placeholder="Enter end date" v-model="timeoffRequestForm.endDate" />
          </div>

          <div class="form-group">
            <label for="Name">Code leave reason</label>
            <input class="form-control" type="text" id="CodeLeaveReasonID" placeholder="Enter code leave reason" v-model="timeoffRequestForm.codeLeaveReason" />
          </div>
          
          <nc-button variant="primary" @click="requestTimeoff">Request timeoff</nc-button>
        </nc-form>
       </nc-layout-aside>
      <nc-layout-content>
        <nc-table class="data-table">
          <thead>
            <nc-table-row>
              <th>#</th>
              <th>Name</th>
              <th>Team</th>
              <th>Reason</th>
              <th>Date</th>
              <th>Status</th>
            </nc-table-row>
          </thead>
          <tbody>
            <nc-table-row v-for="request in requests" v-bind:key="request.id + '_' + request.name">
              <td>{{ request.id }}</td>
              <td>{{ request.name }}</td>
              <td>{{ request.team }}</td>
              <td>{{ request.reason }}</td>
              <td>{{ request.dateOfRequest }}</td>
              <td>{{ request.status }}</td>
            </nc-table-row>
          </tbody>
        </nc-table>
      </nc-layout-content>
    </nc-layout>
  </nc-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { ApiService, LeavePeriod } from '../services/api'

export default Vue.extend({
  name: 'Home',
  components: {

  },
  data: function () {
    return {
      showForm: 0,
      timeoffRequestForm: {
        personNumber: 0 as number,
        employmentNumber: 0 as number,
        leaveTypeCode: "" as string,
        leaveYear: "" as string,
        startDate: "" as string,
        endDate: "" as string,
        codeLeaveReason: "" as string
      } as LeavePeriod,
      requests: [
        { 
          id: 1,
          name: "Filip Havel", 
          team: "ATS", 
          reason: "doctor", 
          dateOfRequest: "26.20.2021", 
          status: "pending"
        },
        { 
          id: 2,
          name: "Filip Havel", 
          team: "ATS", 
          reason: "holiday", 
          dateOfRequest: "12.7.2021", 
          status: "denied"
        },
        { 
          id: 3,
          name: "Filip Havel", 
          team: "ATS", 
          reason: "funeral", 
          dateOfRequest: "2.5.2021", 
          status: "approved"
        }
      ]
      
      }
  }, 
  methods: {
    async requestTimeoff(){
      const api = new ApiService()
      const request = await api.testPOST()
      console.log(request)
    },
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
  padding: 1em 1em 0 1em;
  color: black;
}

.user-form {
  padding: 1em;
}
</style>