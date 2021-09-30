import axios from "axios";

export default class UserService {

    static async getAll() {
        const token = localStorage.getItem('token')
        const response = await axios.get('/user', {headers: {"Authorization": `Bearer ${token}`}})
        return response.data
    }

    static async register(data) {
        const response = await axios.post('/user', data)
        return response
    }

    static async login(credentials) {
        const response = await axios.post('/api/login',
            credentials)
        return response.data
    }
}