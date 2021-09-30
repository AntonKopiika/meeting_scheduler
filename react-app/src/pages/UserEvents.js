import React, {useEffect, useState} from 'react';
import {useParams} from "react-router-dom";
import {useFetching} from "../hooks/useFetching";
import EventService from "../components/API/EventService";
import Loader from "../components/UI/loader/Loader";
import EventList from "../components/Event/EventList";

const UserEvents = () => {
    const params = useParams()
    const [events, setEvents] = useState({})
    const [fetchEventsByUserId, isEventsLoading, eventsError] = useFetching(async () => {
        const data = await EventService.getByUserId(params.id)
        setEvents(data)
    })
    useEffect(() => {
        fetchEventsByUserId()
    }, [])
    const deleteEvent = (event) => {
        setEvents(events.filter(e => e.id !== event.id))
    }
    return (
        <div>
            {isEventsLoading
                ? <Loader/>
                :<EventList events={events} remove={deleteEvent} title={`Events of user with id=${params.id}`}/>
            }
        </div>
    );
};

export default UserEvents;