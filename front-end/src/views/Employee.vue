<template>
  <nc-container>
     <nc-layout horizontal>
       <nc-layout-aside>

         <nc-button @click="openForm">Register timeoff</nc-button>

         <nc-form class="user-form" v-if="this.showForm == 1">

          <div class="form-group">
            <label for="Name">Start date</label>
            <nc-datepicker v-model="timeoffRequestForm.startDate" />
          </div>

          <div class="form-group">
            <label for="Name">End date</label>
            <nc-datepicker v-model="timeoffRequestForm.endDate" />
          </div>

          <div class="form-group">
            <label for="Name">Code leave reason</label>
            <input class="form-control" type="text" id="CodeLeaveReasonID" placeholder="Enter code leave reason" v-model="timeoffRequestForm.codeLeaveReason" />
          </div>

          <div class="form-group">
            <label for="Name">Reason</label>
            <input class="form-control" type="text" id="ReasonID" placeholder="Enter reason" v-model="timeoffRequestForm.reason" />
          </div>
          
          <nc-button variant="primary" @click="requestTimeoff">Request timeoff</nc-button>
        </nc-form>
       </nc-layout-aside>
      <nc-layout-content>
        <nc-table class="data-table">
          <thead>
            <nc-table-row>
              <th scope="col">#</th>
              <th scope="col">Start Date</th>
              <th scope="col">End Date</th>
              <th scope="col">Code leave reason</th>
              <th scope="col">Reason</th>
              <th scope="col">Status</th>
            </nc-table-row>
          </thead>
          <tbody>
            <nc-table-row v-for="request in requests" v-bind:key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.startDate }}</td>
              <td>{{ request.endDate }}</td>
              <td>{{ request.codeLeaveReason }}</td>
              <td>{{ request.reason }}</td>
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
        startDate: new Date(),
        endDate: new Date(),
        codeLeaveReason: "" as string,
        reason: "" as string,
      } as LeavePeriod,
      requests: [] as Object[]
      }
  }, 
  methods: {
    toFullDate(date:Date) : string {
      return date.toLocaleString().split(",")[0]
    },
    async requestTimeoff(){

      const api = new ApiService()

      const request = {
        id: this.requests.length + 1,
        startDate: this.toFullDate(this.timeoffRequestForm.startDate),
        endDate: this.toFullDate(this.timeoffRequestForm.endDate),
        codeLeaveReason: this.timeoffRequestForm.reason,
        reason: String(this.timeoffRequestForm.codeLeaveReason),
        status: "pending"
      }

      this.requests.push(request)

      // const response = await api.requestTimeoffPOST(request.startDate, request.endDate, request.reason)

      // console.log(response)
      // const request = await api.codeLeaveGET()
      // console.log(request)
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