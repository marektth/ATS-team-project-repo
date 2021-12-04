<template>
  <nc-container>
     <nc-layout horizontal>
       <nc-layout-aside>

         <nc-button id="OpenFormButton" @click="openForm">Register timeoff</nc-button>

         <nc-form class="user-form" v-if="this.showForm == 1">

          <div class="form-group">
            <label for="Name">Start date</label>
            <nc-datepicker v-model="timeoffRequestForm.startDate" disable-past-days/>
          </div>

          <div class="form-group">
            <label for="Name">End date</label>
            <nc-datepicker v-model="timeoffRequestForm.endDate" disable-past-days/>
          </div>

          <div class="form-group">
            <label for="Name">Code leave reason</label>
            <input class="form-control" type="text" id="CodeLeaveReasonID" placeholder="Enter code leave reason" v-model="timeoffRequestForm.codeLeaveReason" />
          </div>

          <div class="form-group">
            <label for="Name">Reason</label>
            <input class="form-control" type="text" id="ReasonID" placeholder="Enter reason" v-model="timeoffRequestForm.reason" />
          </div>
          
          <nc-button id="FormSubmitButton" variant="primary" @click="requestTimeoff">Request timeoff</nc-button>
        </nc-form>
       </nc-layout-aside>
      <nc-layout-content>

        <nc-table class="data-table">
          <thead>
            <nc-table-row v-for="(idx,header) in headers" v-bind:key="header + '_' + idx">
              <th scope="col">header</th>
            </nc-table-row>
          </thead>
          <!-- <tbody v-for="request in requests" v-bind:key="request.id">
            <nc-table-row>
              <td>{{ request }}</td>
            </nc-table-row>
          </tbody> -->
        </nc-table>

      </nc-layout-content>
    </nc-layout>
  </nc-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { ApiService, LeavePeriod, TimeoffRecord } from '../services/api'

export default Vue.extend({
  name: 'Home',
  components: {

  },
  data: function () {
    return {
      employeeNumber: 123456,
      showForm: 0,
      timeoffRequestForm: {
        startDate: new Date(),
        endDate: new Date(),
        codeLeaveReason: "" as string,
        reason: "" as string,
      } as LeavePeriod,
      requests: [] as any[],
      headers: [] as any[]
      }
  }, 
  async created(){
    const api = new ApiService(this.employeeNumber)
    const response = await api.requestsTimeoffGET()
    this.loadDataToTable(response)
  },
  methods: {
    loadDataToTable(res : any){
      // load to table
    },
    toFullDate(date:Date) : string {
      // function to edit date to specific format
      return "";
    },
    clearFormInputs(){
      this.timeoffRequestForm.startDate = new Date()
      this.timeoffRequestForm.endDate = new Date()
      this.timeoffRequestForm.codeLeaveReason = ""
      this.timeoffRequestForm.reason = ""
    },
    async requestTimeoff(){
      
      const api = new ApiService(this.employeeNumber)
      const date = new Date()
      const request: TimeoffRecord = {
        id: this.requests.length + 1,
        dateOfRequest:this.toFullDate(date),
        startDate: this.toFullDate(this.timeoffRequestForm.startDate),
        endDate: this.toFullDate(this.timeoffRequestForm.endDate),
        codeLeaveReason: String(this.timeoffRequestForm.codeLeaveReason),
        leaveReason: String(this.timeoffRequestForm.reason),
        status: "pending"
      }

      //const responsePOST = await api.requestTimeoffPOST(request)
      //console.log(responsePOST)
      this.requests = []
      //const responseGET = await api.requestsTimeoffGET()
      //this.loadDataToTable(responseGET)
      this.clearFormInputs()
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
  padding: 0 1em 0 1em;
  color: black;
}

.user-form {
  padding: 1em;
}
</style>