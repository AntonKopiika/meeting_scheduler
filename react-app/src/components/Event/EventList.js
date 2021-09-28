import React from 'react';
import EventItem from "./EventItem";

const EventList = ({events, title, remove, editModal}) => {
    if (!events.length){
        return (
            <h1 style={{textAlign: "center"}}>
                Event list is empty
            </h1>
        )
    }
    return (
        <div>
            <h1 style={{textAlign: "center"}}>
                {title}
            </h1>
            {events.map(e =>
                <EventItem key={e.id} remove={remove} event={e} editModal={editModal}/>
            )}
        </div>
    );
};

export default EventList;