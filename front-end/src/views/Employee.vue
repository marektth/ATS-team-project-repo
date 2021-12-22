<template>
    <b-container id="EmployeeContainer">
      <b-row>
        <b-col cols="3">
    
          <div class="card widget-user">
              <div class="card-body">
                  <img src="https://bootdey.com/img/Content/avatar/avatar2.png" class="img-fluid d-block rounded-circle avatar-md" alt="user">
                  <div class="wid-u-info">
                      <h5 class="mt-3 mb-1">{{employeeInfo.EmployeeName}}</h5>
                      <p class="text-muted mb-0">Employee ID: {{employeeInfo.EmployeeID}}</p>
                      <p class="text-muted mb-0">Leave balance: {{employeeInfo.LeaveBalance}}</p>
                      <div class="user-position">
                          <span class="text-success">Employee</span>
                      </div>
                  </div>
              </div>
          </div>

          <b-card>
            <h5 class="card-title">Request timeoff form</h5>
            <form>
              <div class="mb-3">
                <label for="date-from" class="form-label">Date from:</label>
                <b-form-datepicker id="date-from" :min="date.min" v-model="timeoffRequestForm.startDate" required />
              </div>
              <div class="mb-3">
                <label for="date-to" class="form-label">Date to:</label>
                <b-form-datepicker id="date-to" :min="date.min" v-model="timeoffRequestForm.endDate" required />
              </div>
              <div class="mb-3">
                <label for="code-leave-reason-id">Code Leave reason:</label>
                <select id="code-leave-reason-id" class="form-select" v-model="timeoffRequestForm.codeLeaveReason" required>
                  <option value="" selected>Select code leave reason...</option>
                  <option value="TIM">TIM</option>
                  <option value="SPE">SPE</option>
                  <option value="PAR">PAR</option>
                </select>
              </div>

              <div class="mb-3">
                <label for="leave-reason" class="form-label">Leave reason:</label>
                <input type="text" placeholder="Enter leave reason..." class="form-control" id="leave-reason" v-model="timeoffRequestForm.leaveReason">
              </div>

              <button id="FormSubmitButton"  @click.prevent="requestTimeoff" class="btn btn-success btn-sm">Request timeoff</button>
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
                  <td v-if="(request.Status != 'Rejected') && (request.Status != 'Cancelled')">
                    <a @click="openModal(request.id)" ref="btnToggle"><b-icon icon="x-octagon"></b-icon></a>

                    <b-modal
                      v-bind:id="`modal-prevent-closing-${request.id}`"
                      title="Submit Your Name"
                      @show="resetModal"
                      @hidden="resetModal"
                      @ok="deleteTimeoff(request.id)"
                    >
                      <form ref="form" @submit.stop.prevent="handleSubmit">
                        <p>If you want to delete your request enter: <b>DELETE {{request.id}}</b></p>
                          <b-form-input
                            id="name-input"
                            v-model="confirmation"
                            required
                          ></b-form-input>
                      </form>
                    </b-modal>                    
                    <!-- <b-modal id="bv-modal-example" hide-footer>
                      <div class="d-block text-center">
                        <h3>If you want to delete your request enter: DELETE {{request.id}}</h3>
                      </div>
                      <b-button @click="$bvModal.hide('bv-modal-example')">Close Me</b-button>
                      <b-button @click.prevent="deleteTimeoff(request.id)">delete</b-button>
                    </b-modal> -->

                  </td>
                  <td v-else>-</td>
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
      confirmation: "" as string,
      date: {
        min: new Date()
      },
      employeeInfo: {
        EmployeeID: 69,
        EmployeeName: "",
        EmploymentNumber: 0,
        LeaveBalance: 0,
        OUID: 7
      },
      showForm: 0,
      timeoffRequestForm: {
        startDate: "" as string,
        endDate: "" as string,
        codeLeaveReason: "" as string,
        leaveReason: "" as string,
      } as TimeoffRequest,
      requests: [] as EmployeeTimeoff[]
      }
  }, 
  async created(){
    this.getEmployeeData()
    this.setDate()
  },
  methods: {

    async getEmployeeData() {
      
      const api = new ApiService(this.employeeInfo.EmployeeID)

      const response = await api.employeeTimeoffRequestsGET()

      if(this.requests.length > 0){
        this.requests = []
      }

      if (response.absenceData.length > 0){
        response.absenceData.forEach((request:any) => {
          this.requests.push(request)
        });
      }

      this.employeeInfo.LeaveBalance = response.employeeData.LeaveBalanceDisplay
      this.employeeInfo.EmployeeName = response.employeeData.EmployeeName
      this.employeeInfo.EmploymentNumber = response.employeeData.EmploymentNumber
      this.employeeInfo.OUID = response.employeeData.OUID

      let el = document.getElementById("user-info")
      if(el != null){
        el.innerHTML = `${this.employeeInfo.EmployeeName}`;
      }

      this.setDate()
    },
    async requestTimeoff(){
      // request time off from form
      const api = new ApiService(this.employeeInfo.EmployeeID)
      const response = await api.requestTimeoffPOST(this.timeoffRequestForm)
      console.log(response)
      this.getEmployeeData()
      this.clearFormInputs()
    },
    async deleteTimeoff(id:number){
      //const confirmation = prompt(`If you want to delete your request enter: DELETE ${id}`);
      if(this.confirmation === `DELETE ${id}`){
        const api = new ApiService(this.employeeInfo.EmployeeID)
        const response = await api.requestTimeoffDELETE(id)
        console.log(response)
        this.getEmployeeData()
        this.$nextTick(() => {
          this.$bvModal.hide('modal-prevent-closing')
        })
      }
    },
    
    // helper functions

    setDate(){
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      const minDate = new Date(today)
      minDate.setDate(minDate.getDate() + 1)
      this.date.min = minDate
    },
    clearFormInputs(){
      // form clear
      this.timeoffRequestForm.startDate = ""
      this.timeoffRequestForm.endDate = ""
      this.timeoffRequestForm.codeLeaveReason = ""
      this.timeoffRequestForm.leaveReason = ""
      
    },
    openModal(id:number){
      this.$root.$emit('bv::toggle::modal', `modal-prevent-closing-${id}`, '#btnToggle')
    },
    resetModal(){
      this.confirmation = ""
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

.user-position {
    position: absolute;
    top: 0;
    border-left: 1px solid #dee2e6;
    bottom: 0;
    width: 44px;
    font-size: 16px;
    text-align: center;
    right: 0;
    left: auto;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    -webkit-box-orient: horizontal;
    -webkit-box-direction: normal;
    -ms-flex-direction: row;
    flex-direction: row
}

.user-position span {
    -webkit-transform: rotate(90deg);
    transform: rotate(90deg)
}

.avatar-md {
    height: 3.5rem;
    width: 3.5rem;
}
</style>