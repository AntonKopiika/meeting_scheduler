import React, {useContext, useEffect, useState} from "react";
import '../styles/App.css';
import MeetingList from "../components/Meeting/MeetingList";
import MeetingFilter from "../components/Meeting/MeetingFilter";
import {useMeetings} from "../hooks/useMeetings";
import MeetingService from "../components/API/MeetingService";
import Loader from "../components/UI/loader/Loader";
import {useFetching} from "../hooks/useFetching";
import {AuthContext} from "../components/context";

function Meetings() {
    const {userId} = useContext(AuthContext)
    const [meetings, setMeetings] = useState(
        [])

    useEffect(async () => {
        await fetchMeetings()
    }, [])

    const [filter, setFilter] = useState({sort: '', query: ''})
    const searchedAndSortedMeetings = useMeetings(meetings, filter.sort, filter.query)
    const [fetchMeetings, isMeetingsLoading, meetingError] = useFetching(async () => {
        const meetings = await MeetingService.getByUserId(parseInt(userId))
        setMeetings(meetings)
    })

    const deleteMeeting = async (meeting) => {
        await MeetingService.deleteMeeting(meeting.id)
        await fetchMeetings()
    }

    return (
        <div className="App">
            <hr style={{margin: '15px 0'}}/>
            <MeetingFilter filter={filter} setFilter={setFilter}/>
            {meetingError &&
            <h1>Something went wrong</h1>
            }
            {isMeetingsLoading
                ? <div style={
                    {
                        display: 'flex',
                        justifyContent: 'center',
                        marginTop: 50
                    }}>
                    <Loader/>
                </div>
                : <MeetingList remove={deleteMeeting} meetings={searchedAndSortedMeetings} title="Meeting list"/>
            }
        </div>
    );
}
export default Meetings;