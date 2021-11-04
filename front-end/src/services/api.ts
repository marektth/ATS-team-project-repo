import axios from "axios"

// Leave period data format 

export interface LeavePeriod {
	startDate:Date,
	endDate:Date,
	codeLeaveReason:string
    reason?:string
}

// API endpoint 1. -> get last five timeoff records for specific person (API returns array of TimeoffRecord data)

export interface TimeoffRecord {
    id: number,
    dateOfRequest:string, // timestamp when request was created
    startDate:string,
    endDate:string,
    codeLeaveReason:string,
    leaveReason:string,
    status:string // pending | accepted | declined
}

// API endpoint 2. -> get team

export interface TeamMember { // team member object attributes
    employeeNumber:string,
    name:string,
    position:string
}

export interface Team { // team object attributescodeL    name:string,
    members: TeamMember[]
}



export class ApiService {
    private employeeNumber:string = "123457"
    private requestTimeoffURL:string = "https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/test/submit"
    private codeLeaveURL:string = "https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/test/load"

    async requestTimeoffPOST(request:TimeoffRecord){
        try {
           // console.log(request)
            const testJSON = {
                "Person_Number": this.employeeNumber,
                "dateOfRequest": request.dateOfRequest,
                "startDate": request.startDate,
                "endDate" : request.endDate,
                "codeLeaveReason" : request.codeLeaveReason,
                "leaveReason": request.leaveReason,
                "status": "pending"
            }
            
            return await axios.post(this.requestTimeoffURL, testJSON);
        } catch (err){
            return err;
        }
    }


    async requestsTimeoffGET() : Promise<any>{
        try {
            const response = await axios.get(this.codeLeaveURL)
            //console.log(response.data)
            return response.data;
        } catch(err){
            return err;
        }
    }
}

