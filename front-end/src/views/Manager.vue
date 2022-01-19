<template>
  <b-container id="ManagerContainer">
   <b-row>
     <b-col cols="1">
      <button class="btn btn-success" @click.prevent="triggerARS">Decide</button>
     </b-col>

     <b-col>
      <b-card id="table_card" v-for="(team, team_index) in teams" v-bind:key="String(team.OUID) + '_' + String(team_index)" >
        <h5 class="card-title">{{ team.OUName }} (Team ID: {{team.OUID}})</h5>
        <table class="table table-striped" v-if="team.Data.length > 0" aria-hidden="true">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Request ID</th>
              <th scope="col">Employee ID</th>
              <th scope="col">Name</th>
              <th scope="col">Job Name</th>
              <th scope="col">Requested At</th>
              <th scope="col">Absence Date</th>
              <th scope="col">ATC</th>
              <th scope="col">Leave Reason</th>
              <th scope="col">Reject Reason</th>
              <th scope="col">Overlapping Days</th>
              <th scope="col">Status</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
            <tbody>
            <tr v-for="(employee, idx) in team.Data" v-bind:key="String(employee.EmployeeID) + '_'+ String(idx)">
              <td>{{ idx + 1 }}</td>
              <td>{{ employee.id }}</td>
              <td>{{ employee.EmployeeID }}</td>
              <td>{{ employee.EmployeeName }}</td>
              <td>{{ employee.JobName }}</td>
              <td>{{ epochToDate(employee.AbsenceRequestedAt) }}</td>
              <td>{{ String(employee.AbsenceFrom) }} <br>-<br> {{ String(employee.AbsenceTo) }}</td>
              <td>{{ employee.AbsenceTypeCode }}</td>
              <td>{{ employee.LeaveReason }}</td>
              <td>{{ employee.StatusResolution }}</td>
              <td>{{ overLappingDays(employee.OverlappingDays) }}</td>
              <td>{{ employee.Status }}</td>
              <td v-if="(employee.Status != 'Rejected') && (employee.Status != 'Cancelled')">
                <a @click="openModal(employee.id)" ref="btnToggle"><b-icon icon="x-octagon"></b-icon></a>

                <b-modal
                  v-bind:id="`modal-prevent-closing-${employee.id}`"
                  title="DELETE request"
                  @show="resetModal"
                  @hidden="resetModal"
                  @ok="deleteTimeoff(employee.id)"
                >
                  <form ref="form" @submit.stop.prevent="handleSubmit">
                    <p>If you want to delete your request enter: <strong>DELETE {{employee.id}}</strong></p>
                      <b-form-input
                        id="name-input"
                        v-model="confirmation"
                        required
                      ></b-form-input>
                  </form>
                </b-modal>         
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
import { ApiService } from '../services/api'

export default Vue.extend({
  name: 'Manager',
  components: {

  },
  data: function () {
    return {
      confirmation: "" as string,
      managerID: 7,
      teams: [] as any[]
      }
  }, 
  async created(){
    this.getEmployeeData()
  },
  methods: {
    async triggerARS(){
      const api = new ApiService(this.managerID)
      alert(await api.triggerARSPOST())
      this.getEmployeeData()
    },
    async getEmployeeData() {
      
      const api = new ApiService(this.managerID)
      const response:any[] = await api.managerTimeoffRequestsGET()
      console.log(response)
      if(this.teams.length > 0){
        this.teams = []
      }

      if (response.length > 0){
        response.forEach(team => {
          if(team.Data != null){
            this.teams.push(team)
          }
        });
      }
      let el = document.getElementById("user-info")
      if(el != null){
        el.innerHTML = `Manager ${this.managerID}`;
      }
    },
     async deleteTimeoff(id:number){
      if(this.confirmation === `DELETE ${id}`){
        const api = new ApiService(this.managerID)
        const response = await api.requestTimeoffDELETE(id)
        console.log(response)
        this.getEmployeeData()
      }
    },
    
    openModal(id:number){
      this.$root.$emit('bv::toggle::modal', `modal-prevent-closing-${id}`, '#btnToggle')
    },
    resetModal(){
      this.confirmation = ""
    },
    addZeroToTime(number:number){
      if(number <= 9){
        return '0' + String(number)
      } else {
        return String(number)
      }
    },
    epochToDate(date:number){
      let convertedDate = new Date(date*1000)
      let day = this.addZeroToTime(convertedDate.getDate())
      let month = this.addZeroToTime(convertedDate.getMonth() + 1)
      let year = String(convertedDate.getFullYear())
      let hour = this.addZeroToTime(convertedDate.getHours())
      let minute = this.addZeroToTime(convertedDate.getHours())
      let second = this.addZeroToTime(convertedDate.getSeconds())

      return `${day}/${month}/${year}\n${hour}:${minute}:${second}`
    },
    overLappingDays(dates:Array<any>){
      let days = ""
      let len = dates.length
      if(len == 0) {
        return "-"
      }
      dates.forEach(date => {
        let convertedDate = new Date(date*1000)
        let day = this.addZeroToTime(convertedDate.getDate())
        let month = this.addZeroToTime(convertedDate.getMonth() + 1)
        let year = String(convertedDate.getFullYear())
        if(len > 1){
          days += `${day}/${month}/${year}, `
          len--
        } else {
          days += `${day}/${month}/${year}`
        }
      })

      return days
    }
  }
  
});
</script>

<style scoped>
.data-table {
  padding: 0 1em 0 1em;
  color: black;
}
b-button {
  text-align: left;
}

#ManagerContainer {
  margin-top: 2%;
}

#table_card {
  margin-bottom: 1em !important;
}

</style>
