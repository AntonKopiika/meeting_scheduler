import axios from "axios";
import {useRef} from "react";


export default class EventService {

    static async getAll() {
        const token = localStorage.getItem('token')
        const response = await axios.get('/event', {headers: {"Authorization": `Bearer ${token}`}})
        return response.data
    }

    static async getById(id) {
        const response = await axios.get('/event/' + id)
        return response.data
    }

    static async getByUserId(userId) {
        const token = localStorage.getItem('token')
        const response = await axios.get('/user/events/' + userId, {headers: {"Authorization": `Bearer ${token}`}})
        return response.data
    }

    static async getEventTimeslots(eventId) {
        const response = await axios.get('/timeslot/' + eventId)
        return response.data
    }

    static async postEvent(event) {
        const token = localStorage.getItem('token')
        const response = await axios.post('/event', event, {headers: {"Authorization": `Bearer ${token}`}})
        return response.data
    }

    static async putEvent(event) {
        const token = localStorage.getItem('token')
        const response = await axios.put(`/event/${event.id}`, event, {headers: {"Authorization": `Bearer ${token}`}})
        return response.data
    }

    static async deleteEvent(eventId) {
        const token = localStorage.getItem('token')
        const response = await axios.delete('/event/' + eventId, {headers: {"Authorization": `Bearer ${token}`}})
        return response.data
    }
}