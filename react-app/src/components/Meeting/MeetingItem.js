import React from 'react';
import MyButton from "../UI/button/MyButton";

const MeetingItem = (props) => {
    return (
        <div className="block">
            <div className="block__content">
                <strong>{props.meeting.additional_info}</strong>
                <div>
                    <h5>Attendee: {props.meeting.attendee_name}</h5>
                    <h5>Time: {props.meeting.start_time}</h5>
                    <h5>Description: {props.meeting.additional_info}</h5>
                </div>
            </div>
            <div className="block__btns">
                <MyButton onClick={()=>props.remove(props.meeting)}>
                    Remove
                </MyButton>
            </div>
        </div>
    );
};

export default MeetingItem;