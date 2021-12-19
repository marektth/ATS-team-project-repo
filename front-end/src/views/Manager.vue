<template>
  <b-container id="ManagerContainer">
   <b-row>
     <b-col cols="1">
      <button class="btn btn-success" @click.prevent="triggerARS">Decide</button>
     </b-col>
     <b-col>
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
import { ApiService, EmployeeTimeoff} from '../services/api'

export default Vue.extend({
  name: 'Manager',
  components: {

  },
  data: function () {
    return {
      managerID: 7,
      requests: [] as EmployeeTimeoff[]
      
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
      const response:EmployeeTimeoff[] = await api.managerTimeoffRequestsGET()
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
     async deleteTimeoff(id:number){
      const confirmation = prompt(`If you want to delete your request enter: DELETE ${id}`);
      if(confirmation === `DELETE ${id}`){
        const api = new ApiService(this.managerID)
        const response = await api.requestTimeoffDELETE(id)
        console.log(response)
        this.getEmployeeData()
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
b-button {
  text-align: left;
}

#ManagerContainer {
  margin-top: 2%;
}
</style>
