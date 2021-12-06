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
import { ApiService, TimeoffRequest } from '../services/api'

export default Vue.extend({
  name: 'Home',
  components: {

  },
  data: function () {
    return {
      employeeID: 38,
      showForm: 0,
      timeoffRequestForm: {
        endDate: new Date(),
        codeLeaveReason: "" as string,
        leaveReason: "" as string,
      } as TimeoffRequest,
      requests: [] as any[],
      headers: [] as any[]
      }
  }, 
  async created(){
    // const api = new ApiService(this.employeeID)
    // const response = await api.requestTimeoffDELETE(13)
    // const response = await api.employeeTimeoffRequestsGET()
    // console.log(response)
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
      this.timeoffRequestForm.endDate = new Date()
      this.timeoffRequestForm.codeLeaveReason = ""
      this.timeoffRequestForm.leaveReason = ""
    },
    async requestTimeoff(){
      // request time off from form
      const api = new ApiService(this.employeeID)
      const response = await api.requestTimeoffPOST(this.timeoffRequestForm)
      console.log(response)
    },
    async deleteTimeoff(id:number, data:TimeoffRequest){
      const api = new ApiService(this.employeeID)
      const response = await api.requestTimeoffDELETE(id)
      console.log(response)
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