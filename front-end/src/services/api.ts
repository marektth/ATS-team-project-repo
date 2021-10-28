import axios from "axios"

// Leave period data format 

export interface LeavePeriod {
	personNumber:number,
	employmentNumber:number,
	leaveTypeCode:string,
	leaveYear:string,
	startDate:string,
	endDate:string,
	codeLeaveReason?:string
}

export class ApiService {
    private requestURL:string = "https://io7jc9gyn5.execute-api.eu-central-1.amazonaws.com/test/"

    async testPOST(){
        try {
            const testJSON = {
                "Person_Number": 69,
                "name": "Ludovit",
                "surname": "Chocholacek",
                "age": "34"
            }
            
            const req = await axios.post(this.requestURL, testJSON)
            return req;
        } catch (err){
            return err;
        }
    }
}

