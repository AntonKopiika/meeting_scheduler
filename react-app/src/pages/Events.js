import React, {useEffect, useState} from "react";
import '../styles/App.css';
import MyModal from "../components/UI/modal/MyModal";
import MyButton from "../components/UI/button/MyButton";
import Loader from "../components/UI/loader/Loader";
import {useFetching} from "../hooks/useFetching";
import EventService from "../components/API/EventService";
import EventFilter from "../components/Event/EventFilter";
import EventList from "../components/Event/EventList";
import {useEvents} from "../hooks/useEvents";
import EventForm from "../components/Event/EventForm";
import {useParams} from "react-router-dom";
import EditEventForm from "../components/Event/EditEventForm";


function Events() {
    const username = sessionStorage.getItem("username")
    const params = useParams()
    const [events, setEvents] = useState([])
    const [editedEvent, setEditedEvent] = useState({
        host: parseInt(params.id),
        title: "",
        description: "",
        start_time: "",
        end_time: "",
        duration: "",
        working_days: false,
        event_type: ""
    })
    useEffect(async () => {
        await fetchEvents()
    }, [])

    const [filter, setFilter] = useState({sort: '', query: ''})
    const [eventModal, setEventModal] = useState(false)
    const [editEventModal, setEditEventModal] = useState(false)
    const searchedAndSortedEvents = useEvents(events, filter.sort, filter.query)
    const [fetchEvents, isEventsLoading, eventError] = useFetching(async () => {
        const events = await EventService.getByUserId(params.id)
        setEvents(events)
    })

    const createEvent = async (event) => {
        await EventService.postEvent(event)
        setEventModal(false)
        await fetchEvents()
    }

    const editEvent = async (editedEvent) => {
        await EventService.putEvent(editedEvent)
        setEditEventModal(false)
        await fetchEvents()
    }

    const openEditEventModal = (event) => {
        setEditedEvent(event)
        setEditEventModal(true)
    }

    const deleteEvent = async (event) => {
        await EventService.deleteEvent(event.id)
        await fetchEvents()
    }

    return (
        <div className="App">
            <MyButton
                style={{marginTop: 30}}
                onClick={() => setEventModal(true)}
            >
                Create event
            </MyButton>
            <MyModal
                visible={editEventModal}
                setVisible={setEditEventModal}
            >
                <EditEventForm update={editEvent} editedEvent={editedEvent} setEditedEvent={setEditedEvent}/>
            </MyModal>
            <MyModal
                visible={eventModal}
                setVisible={setEventModal}
            >
                <EventForm create={createEvent}/>
            </MyModal>

            <hr style={{margin: '15px 0'}}/>
            <EventFilter filter={filter} setFilter={setFilter}/>
            {eventError
                ? <h1 style={
                    {
                        display: 'flex',
                        justifyContent: 'center',
                        marginTop: 50
                    }
                }>Something went wrong {`${eventError}`}</h1>
                : isEventsLoading
                    ? <div style={
                        {
                            display: 'flex',
                            justifyContent: 'center',
                            marginTop: 50
                        }
                    }>
                        <Loader/>
                    </div>
                    :
                    <EventList
                        editModal={openEditEventModal}
                        remove={deleteEvent}
                        events={searchedAndSortedEvents}
                        title={`Event list for ${username}`}
                    />
            }
        </div>
    );
}

export default Events;