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
    private employeeTimeoffRequestURL:string = "https://gm837p1e3k.execute-api.eu-central-1.amazonaws.com/leaveRequestTF/load?personID="
    private managerTimeoffRequestsURL:string = "https://gm837p1e3k.execute-api.eu-central-1.amazonaws.com/leaveRequestTF/load_team_absence?managerID=";
    
    // POST URL
    private requestTimeoffURL:string = "https://gm837p1e3k.execute-api.eu-central-1.amazonaws.com/leaveRequestTF/submit"
    private triggerARSURL:string = "https://q2j2nwie52.execute-api.eu-central-1.amazonaws.com/leaveRequest/invoke_decision"
    
    // DELETE URL
    private requestTimeoffDeleteURL:string = "https://gm837p1e3k.execute-api.eu-central-1.amazonaws.com/leaveRequestTF/delete"

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
            absenceData: response.data[0].AbsenceData as EmployeeTimeoff[],
            employeeData: response.data[0].EmployeeData[0]
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

