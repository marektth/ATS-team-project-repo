import axios from "axios"
import _ from 'underscore';
import { KEY } from "@/utils/key_enum";

// Leave period data format 

export interface TimeoffRequest {
	endDate:Date,
	codeLeaveReason:string
    leaveReason:string
}

export class ApiService {
    private employeeNumber:number;
    private header = {
        "x-api-key": KEY.AWS
    }
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


    dateConvert(date:Date) : string {
        return  ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + ((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + date.getFullYear()
    }

    // GET

    // GET all time off requests -> employee 
    async employeeTimeoffRequestsGET() {
        try {
            const response:any = await axios.get(
                `https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/leaveRequest/load?personID=${this.employeeNumber}`,
                { headers: this.header }
            )
            if(response.data.length === 0){
                return "No data"
            } else {
                return response.data
            }
           
        } catch(err){
            console.log(err)
            return "No data";
        }
    }


    // GET all time off requests from team -> managaer
    async managerTimeoffRequestsGET() {
        try {
            const response:any = await axios.get(
                `https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/leaveRequest/load_team_absence?managerID=${this.employeeNumber}`,
                { headers: this.header }
            )
            if(response.data.length === 0){
                return "No data"
            } else {
                return response.data
            }
           
        } catch(err){
            console.log(err)
            return "No data";
        }
    }


    // POST


    // POST time off request -> employee
    async requestTimeoffPOST(request:TimeoffRequest){
        try {
            console.log(this.dateConvert(request.endDate))
            const timeoffData = {
                "EmployeeID": this.employeeNumber,
                "DateOfAbsence" : this.dateConvert(request.endDate),
                "AbsenceTypeCode" : request.codeLeaveReason,
                "LeaveReason": request.leaveReason, 
                "Status": "Pending"
}
           // console.log(request)
            
            return await axios.post("https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/leaveRequest/submit", timeoffData, { headers: this.header });
        } catch (err){
            return err;
        }
    }


    // DELETE

    // DELETE specific time off request
    async requestTimeoffDELETE(requestID:number){
        return await axios.delete("https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/leaveRequest/delete",{
            headers: this.header,
            data: {
                "id": requestID
            }
          })
    }
}

