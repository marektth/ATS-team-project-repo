import axios from "axios"

export class apiService {
    private requestAllURL:string = "https://jsonplaceholder.typicode.com/todos"

    async requestAllPeople(){
        try {
            const response = await axios.get(this.requestAllURL);
            return response;
        } catch (error) {
            return error;
        }
    }
}

