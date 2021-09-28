import React, {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";
import EventService from "../components/API/EventService";
import {useParams} from "react-router-dom";
import Loader from "../components/UI/loader/Loader";
import MeetingForm from "../components/Meeting/MeetingForm";
import EventInfo from "../components/Event/EventInfo";

const CreateMeeting = () => {
    const params = useParams()
    const [timeslots, setTimeslots] = useState([])

    const [fetchTimeslots, isLoading, error] = useFetching(async () => {
        const slots = await EventService.getEventTimeslots(params.id)
        setTimeslots(slots)
    })

    const [fetchEvent, isEventLoading, eventError] = useFetching(async () => {
        const event = await EventService.getById(params.id)
        setEvent(event)
    })

    const [event, setEvent] = useState({
        title: "",
        description: "",
        start_time: "",
        end_time: ""
    })

    useEffect(() => {
        fetchTimeslots()
        fetchEvent()
    }, [])

    if (error || eventError) {
        return (
            <div>
                <h1 style={
                    {
                        display: 'flex',
                        justifyContent: 'center',
                        marginTop: 50
                    }
                }>Something went wrong</h1>
            </div>)
    }

    return (
        <div>
            {isLoading || isEventLoading
                ? <div style={
                    {
                        display: 'flex',
                        justifyContent: 'center',
                        marginTop: 50
                    }}>
                    <Loader/>
                </div>
                :
                <div>
                    <EventInfo event={event}/>
                    <MeetingForm event={event} timeslots={timeslots}/>
                </div>
            }
        </div>
    );
};

export default CreateMeeting;