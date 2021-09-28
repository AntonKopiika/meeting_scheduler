import React from 'react';
import MeetingItem from "./MeetingItem";

const MeetingList = ({meetings, title, remove}) => {
    if (!meetings.length){
        return (
            <h1 style={{textAlign: "center"}}>
                Meeting list is empty
            </h1>
        )
    }
    return (
        <div>
            <h1 style={{textAlign: "center"}}>
                {title}
            </h1>
            {meetings.map(meeting =>
                <MeetingItem key={meeting.id} remove={remove} meeting={meeting}/>
            )}
        </div>
    );
};

export default MeetingList;