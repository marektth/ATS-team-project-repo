import axios from "axios"
import _ from 'underscore';
// Leave period data format 

export interface LeavePeriod {
	startDate:Date,
	endDate:Date,
	codeLeaveReason:string
    reason?:string
}

// API endpoint 1. -> get last five timeoff records for specific person (API returns array of TimeoffRecord data)

export interface TimeoffRecord {
    id:number,
    dateOfRequest:string, // timestamp when request was created
    startDate:string,
    endDate:string,
    codeLeaveReason:string,
    leaveReason:string,
    status:string // pending | accepted | declined
}

// API endpoint 2. -> get team

export interface TeamMember { // team member object attributes
    employeeNumber:number,
    name:string,
    position:string
}

export interface Team { // team object attributescodeL    name:string,
    members: TeamMember[]
}



export class ApiService {
    private employeeNumber:number;

    //URLs

    // GET URL 

    // POST URL

    // DELETE URL

    // UPDATE URL

    //private requestTimeoffURL:string;
    //private codeLeaveURL:string;

    constructor(employeeNumber: number) {
        this.employeeNumber = employeeNumber
    }

    // GET

    // GET all time off requests -> manager 
    async requestsTimeoffGET() {
        try {
            const response = await axios.get("URL")
            console.log(response.data)
            return response.data;
        } catch(err){
            return err;
        }
    }


    // GET time off requests for specific employee -> employee
    async employeeTimeoffGET(employeeID:number){

    }


    // POST


    // POST time off request -> employee
    async requestTimeoffPOST(request:TimeoffRecord){
        try {
           // console.log(request)
            const timeoffData = {
                "Employee ID": this.employeeNumber,
                "Vacation Date" : request.endDate,
                "Code Leave Reason" : request.codeLeaveReason,
                "Leave Reason": request.leaveReason,
                "Status": "Pending"
            }
            
            return await axios.post("URL", timeoffData);
        } catch (err){
            return err;
        }
    }


    // DELETE

    // DELETE specific time off request
    async requestTimeoffDELETE(requestID:number){

    }


    // UPDATE

    // UPDATE specific time off request (start date, end date, code leave reason, reason) -> employee
    async requestTimeoffUPDATE(requestID:number, obj:Object){

    }

    // UPDATE specific time off request (status) -> manager
    async requestTimeoffStatusUPDATE(id:number, status:string){

    }
}

