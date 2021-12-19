<template>
    <b-container id="EmployeeContainer">
      <b-row>
        <b-col cols="3">
          <b-card>
            <h5 class="card-title">Card title</h5>
            <form>
              <div class="mb-3">
                <label for="date-from" class="form-label">Date from:</label>
                <input type="date" class="form-control" id="date-from" v-model="timeoffRequestForm.startDate" required>
              </div>
              <div class="mb-3">
                <label for="date-to" class="form-label">Date to:</label>
                <input type="date" class="form-control" id="date-to" v-model="timeoffRequestForm.endDate" required>
              </div>
              <div class="mb-3">
                <label for="code-leave-reason-id">Code Leave reason:</label>
                <select id="code-leave-reason-id" class="form-select" v-model="timeoffRequestForm.codeLeaveReason" required>
                  <option value="TIM">TIM</option>
                  <option value="SPE">SPE</option>
                  <option value="PAR">PAR</option>
                </select>
              </div>

              <div class="mb-3">
                <label for="leave-reason" class="form-label">Leave reason:</label>
                <input type="text" placeholder="Enter leave reason..." class="form-control" id="leave-reason" v-model="this.timeoffRequestForm.leaveReason">
              </div>

              <button id="FormSubmitButton"  @click.prevent="requestTimeoff" class="btn btn-primary">Request timeoff</button>
            </form>
          </b-card>
        </b-col>

        <b-col cols="9">
          <b-card>
            <table class="table table-striped" v-if="this.requests.length > 0">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Request ID</th>
                  <th scope="col">Employee ID</th>
                  <th scope="col">Absence From</th>
                  <th scope="col">Absence To</th>
                  <th scope="col">Absence Type Code</th>
                  <th scope="col">Leave Reason</th>
                  <th scope="col">Reject reason</th>
                  <th scope="col">Status</th>
                  <th scope="col">Action</th>
                </tr>
              </thead>
                <tbody>
                <tr v-for="(request,idx) in requests" v-bind:key="String(request.EmployeeID) + '_'+ String(idx)">
                  <td scope="row">{{ idx + 1 }}</td>
                  <td>{{ request.id }}</td>
                  <td>{{ request.EmployeeID }}</td>
                  <td>{{ request.AbsenceFrom }}</td>
                  <td>{{ request.AbsenceTo }}</td>
                  <td>{{ request.AbsenceTypeCode }}</td>
                  <td>{{ request.LeaveReason }}</td>
                  <td>{{ request.StatusResolution }}</td>
                  <td>{{ request.Status }}</td>
                  <td><a @click.prevent="deleteTimeoff(request.id)"><b-icon icon="trash"></b-icon></a></td>
                </tr>
              </tbody>
            </table>
            <h1 v-else>No data</h1>

          </b-card>
        </b-col>
      </b-row>
    </b-container>
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
      employeeID: 69,
      leaveBalance: 0,
      showForm: 0,
      timeoffRequestForm: {
        startDate: new Date(),
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
      const response = await api.employeeTimeoffRequestsGET()
      console.log(response)
      if(this.requests.length > 0){
        this.requests = []
      }

      if (response.absenceData.length > 0){
        response.absenceData.forEach((request:any) => {
          this.requests.push(request)
        });
      }

      this.leaveBalance = response.leaveBalance
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
      this.timeoffRequestForm.startDate = new Date()
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

  color: black;
}

.user-form {
  padding: 1em;
}

.time-tabs {
  padding-bottom: 0 !important;
  margin-bottom: 0 !important;
}

#EmployeeContainer {
  margin-top: 2%;
}
</style>