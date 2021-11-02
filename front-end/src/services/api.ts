import axios from "axios"

// Leave period data format 

export interface LeavePeriod {
	personNumber:number,
	employmentNumber:number,
	leaveTypeCode:string,
	leaveYear:string,
	startDate:Date,
	endDate:Date,
	codeLeaveReason?:string
    reason?:string
}

export class ApiService {
    private employeeNumber:string = "123456"
    private requestTimeoffURL:string = "https://ulniobyl6l.execute-api.eu-central-1.amazonaws.com/skuska/submit"
    private codeLeaveURL:string = "https://ulniobyl6l.execute-api.eu-central-1.amazonaws.com/skuska/load"

    async requestTimeoffPOST(startDate:string, endDate:string, reason:string){
        try {

            const testJSON = {
                "Person_Number": this.employeeNumber,
                "startDate": startDate,
                "endDate" : endDate,
                "leaveReason" : reason
            }
            
            const req = await axios.post(this.requestTimeoffURL, testJSON)
            return req;
        } catch (err){
            return err;
        }
    }

    async codeLeaveGET(){
        try {
            const req = await axios.get(this.codeLeaveURL)
            return req;
        } catch(err){
            return err;
        }
    }
}

