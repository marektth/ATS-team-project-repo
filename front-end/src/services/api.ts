import axios from "axios"
import { KEY } from "@/utils/key_enum";

// INTERFACES

export interface TimeoffRequest {
    startDate:string
	endDate:string
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
    private employeeTimeoffRequestURL:string = "https://q2j2nwie52.execute-api.eu-central-1.amazonaws.com/leaveRequest/load?personID="
    private managerTimeoffRequestsURL:string = "https://q2j2nwie52.execute-api.eu-central-1.amazonaws.com/leaveRequest/load_team_absence?managerID=";
    
    // POST URL
    private requestTimeoffURL:string = "https://q2j2nwie52.execute-api.eu-central-1.amazonaws.com/leaveRequest/submit"
    private triggerARSURL:string = "https://q2j2nwie52.execute-api.eu-central-1.amazonaws.com/leaveRequest/invoke_decision"
    
    // DELETE URL
    private requestTimeoffDeleteURL:string = "https://q2j2nwie52.execute-api.eu-central-1.amazonaws.com/leaveRequest/delete"

    // UPDATE URL

    constructor(employeeNumber: number) {
        this.employeeNumber = employeeNumber
    }

    // HELPER FUNCTIONS
    // ---------------------------------------

    dateConvert(date:string) : string {
        let tmp = date.split('-')
        return `${tmp[2]}/${tmp[1]}/${tmp[0]}`
    }
    // REQUESTS
    // ---------------------------------------

    // GET

    // GET all time off requests -> employee 
    async employeeTimeoffRequestsGET() {
     
        const response:any = await axios.get(
            this.employeeTimeoffRequestURL + String(this.employeeNumber),
            { headers: this.header }
        )
        console.log(response)
        return {
            absenceData: response.data.AbsenceData as EmployeeTimeoff[],
            employeeData: response.data.EmployeeData[0]
        } // môže byť viac LeaveBalance? Nie je lepší object?
            
           
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
            const timeoffData = {
                "EmployeeID": this.employeeNumber,
                "AbsenceFrom": this.dateConvert(request.startDate),
                "AbsenceTo" : this.dateConvert(request.endDate),
                "AbsenceTypeCode" : request.codeLeaveReason,
                "LeaveReason": request.leaveReason, 
                "Status": "Pending"
            }
            console.log(timeoffData)
          
            return await axios.post(this.requestTimeoffURL, timeoffData, { headers: this.header });
        } catch (err:any){
            console.error(err.response)
            return err.response;
        }
    }


    // POST trigger ARS

    async triggerARSPOST() {
        try {
            const response = await axios.post(this.triggerARSURL, { "alg-trigger": "true" }, { headers: this.header });
            return String(response.data)
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

