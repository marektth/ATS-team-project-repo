<template>
  <nc-container>
   <nc-layout horizontal>
      <nc-button @click.prevent="triggerARS">Decide</nc-button>

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
   </nc-layout>
  </nc-container>
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
      //const response = await api.requestTimeoffDELETE(10)
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

</style>
