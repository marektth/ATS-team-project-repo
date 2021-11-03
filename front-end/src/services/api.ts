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
    dateOfRequest:string, // timestamp when request was created
    startDate:string,
    endDate:string,
    codeLeaveReason:string,
    reason?:string,
    status:string // pending | accepted | declined
}

// API endpoint 2. -> get team

export interface TeamMember { // team member object attributes
    employeeNumber:string,
    name:string,
    position:string
}

export interface Team { // team object attributes
    name:string,
    members: TeamMember[]
}



export class ApiService {
    private employeeNumber:string = "123457"
    private requestTimeoffURL:string = "https://ulniobyl6l.execute-api.eu-central-1.amazonaws.com/skuska/submit"
    private codeLeaveURL:string = "https://ulniobyl6l.execute-api.eu-central-1.amazonaws.com/skuska/load"

    async requestTimeoffPOST(startDate:string, endDate:string, codeLeaveReason:string){
        try {
            console.log(codeLeaveReason)
            const testJSON = {
                "Person_Number": this.employeeNumber,
                "startDate": startDate,
                "endDate" : endDate,
                "leaveReason" : codeLeaveReason
            }
            
            return await axios.post(this.requestTimeoffURL, testJSON);
        } catch (err){
            return err;
        }
    }

    async codeLeaveGET(){
        try {
            return await axios.get(this.codeLeaveURL);
        } catch(err){
            return err;
        }
    }
}

