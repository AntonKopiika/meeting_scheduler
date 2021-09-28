import React from 'react';

const EventInfo = ({event}) => {
    return (
        <div>
            <h1 style={{textAlign: 'center', marginTop: '10px'}}>{event.title}</h1>
            <div>
                <h4>Duration: {event.start_time}-{event.end_time}</h4>
                <h4>Description: {event.description}</h4>
            </div>
        </div>
    );
};

export default EventInfo;