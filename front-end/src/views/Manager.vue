<template>
  <nc-container>
   <nc-layout horizontal> 
     <nc-table class="data-table">
          <thead>
            <nc-table-row>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Team</th>
              <th scope="col">Code leave reason</th>
              <th scope="col">Reason</th>
              <th scope="col">Date of request</th>
              <th scope="col">Start date</th>
              <th scope="col">End date</th>
              <th scope="col">Status</th>
            </nc-table-row>
          </thead>
          <tbody>
            <nc-table-row v-for="request in requests" v-bind:key="request.id + '_' + request.name">
              <td>{{ request.id }}</td>
              <td>{{ request.name }}</td>
              <td>{{ request.team }}</td>
              <td>{{ request.codeLeaveReason }}</td>
              <td>{{ request.reason }}</td>
              <td>{{ request.dateOfRequest }}</td>
              <td>{{ request.startDate }}</td>
              <td>{{ request.endDate }}</td>
              <td>{{ request.status }}</td>
            </nc-table-row>
          </tbody>
        </nc-table>
   </nc-layout>
  </nc-container>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'Manager',
  components: {

  },
  data: function () {
    return {
      requests: [
        { 
          id: 1,
          name: "Filip Havel", 
          team: "ATS", 
          codeLeaveReason: "BOW",
          reason: "Health", 
          dateOfRequest: "26.2.2021", 
          startDate: "27.2.2021",
          endDate: "28.2.2021",
          status: "for approval"
        },
        { 
          id: 2,
          name: "Filip Havel", 
          team: "ATS", 
          codeLeaveReason: "WET",
          reason: "", 
          dateOfRequest: "12.7.2021", 
          startDate: "17.7.2021",
          endDate: "28.7.2021",
          status: "denied"
        },
        { 
          id: 3,
          name: "Filip Havel", 
          team: "ATS", 
          codeLeaveReason: "BOW",
          reason: "Holiday",  
          dateOfRequest: "2.5.2021", 
          startDate: "26.5.2021",
          endDate: "26.5.2021",
          status: "approved"
        }
      ]
      
      }
  }, 
  methods: {
    
  }
  
});
</script>

<style scoped>
.data-table {
  padding: 0 1em 0 1em;
  color: black;
}

</style>
