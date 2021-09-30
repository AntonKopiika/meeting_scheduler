import axios from "axios";

export default class MeetingService {

    static async getAll() {
        const token = localStorage.getItem('token')
        const response = await axios.get('/meeting', {headers: {"Authorization": `Bearer ${token}`}})
        return response.data.filter(meeting => meeting.event !== null)
    }

    static async getByUserId(userId) {
        const token = localStorage.getItem('token')
        const response = await axios.get('/meeting',
            {headers: {"Authorization": `Bearer ${token}`}})
        return response.data.filter(meeting => meeting.host === userId)
    }

    static async postMeeting(data) {
        const response = await axios.post('/meeting', data)
        return response
    }

    static async deleteMeeting(meetingId) {
        const token = localStorage.getItem('token')
        const response = await axios.delete('/meeting/' + meetingId,
            {headers: {"Authorization": `Bearer ${token}`}})
        return response
    }
}