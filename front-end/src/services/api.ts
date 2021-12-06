import axios from "axios"
import _ from 'underscore';
import { KEY } from "@/utils/key_enum";

// INTERFACES

export interface TimeoffRequest {
	endDate:Date,
	codeLeaveReason:string
    leaveReason:string
}

export interface EmployeeTimeoff {
    id:number
    EmployeeID:string
    DateOfAbsence:string
    AbsenceTypeCode:string
    Rating:Object
    LeaveReason:string
    Status:string
}

export class ApiService {
    private employeeNumber:number;
    private header = {
        "x-api-key": KEY.AWS
    }

    // URL'S
    // ---------------------------------------

    // GET URL 
    private employeeTimeoffRequestURL:string = "https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/leaveRequest/load?personID="
    private managerTimeoffRequestsURL:string = "https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/leaveRequest/load_team_absence?managerID=";
    
    // POST URL
    private requestTimeoffURL:string = "https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/leaveRequest/submit"
    
    // DELETE URL
    private requestTimeoffDeleteURL:string = "https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/leaveRequest/delete"

    // UPDATE URL

    constructor(employeeNumber: number) {
        this.employeeNumber = employeeNumber
    }

    // HELPER FUNCTIONS
    // ---------------------------------------

    dateConvert(date:Date) : string {
        return  ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + ((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + date.getFullYear()
    }


    // REQUESTS
    // ---------------------------------------

    // GET

    // GET all time off requests -> employee 
    async employeeTimeoffRequestsGET() {
        try {
            const response:any = await axios.get(
                this.employeeTimeoffRequestURL + String(this.employeeNumber),
                { headers: this.header }
            )
            if(response.data.length === 0){
                return "No data"
            } else {
                return response.data
            }
           
        } catch(err){
            console.error(err)
            return "No data";
        }
    }


    // GET all time off requests from team -> managaer
    async managerTimeoffRequestsGET() {
        try {
            const response:any = await axios.get(
                this.managerTimeoffRequestsURL + String(this.employeeNumber),
                { headers: this.header }
            )
            if(response.data.length === 0){
                return "No data"
            } else {
                return response.data
            }
           
        } catch(err){
            console.error(err)
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
          
            return await axios.post(this.requestTimeoffURL, timeoffData, { headers: this.header });
        } catch (err){
            console.error(err)
            return err;
        }
    }


    // DELETE

    // DELETE specific time off request
    async requestTimeoffDELETE(requestID:number){
        try {
            return await axios.delete(this.requestTimeoffDeleteURL,{
                headers: this.header,
                data: {
                    "id": requestID
                }
            })
        } catch (err) {
            console.error(err)
        }
    }
}

