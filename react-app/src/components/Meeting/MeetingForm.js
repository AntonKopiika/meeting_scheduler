import React, {useState} from 'react';
import MyInput from "../UI/input/MyInput";
import MyButton from "../UI/button/MyButton";
import MeetingService from "../API/MeetingService";
import {useHistory} from "react-router-dom";

const MeetingForm = ({event, timeslots}) => {
    const history= useHistory()
    const [meeting, setMeeting] = useState({
        attendee_name: "",
        attendee_email: "",
        additional_info: "",
        start_time: "",
        link: ""
    })

    const [formState, setFormState] = useState({
        formValid: false,
        formErrors: {
            attendee_name: '',
            attendee_email: ''
        },
        attendeeNameValid: false,
        attendeeEmailValid: false,
    })

    const validateField = (value, fieldName) => {
        let fieldValidationErrors = {...formState.formErrors}
        let attendeeNameValid = formState.attendeeNameValid
        let attendeeEmailValid = formState.attendeeEmailValid
        switch (fieldName) {
            case "attendee_name":
                attendeeNameValid = value.length > 0
                fieldValidationErrors.attendee_name = attendeeNameValid ? '' : 'input your name, please'
                break
            case "attendee_email":
                attendeeEmailValid = !!value.match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i)
                fieldValidationErrors.attendee_email = attendeeEmailValid ? '' : 'wrong email format'
                break
            default:
                break;
        }
        setFormState({
            ...formState,
            formErrors: fieldValidationErrors,
            attendeeNameValid: attendeeNameValid,
            attendeeEmailValid: attendeeEmailValid,
            formValid: formState.attendeeNameValid && formState.attendeeEmailValid
        });
    }

    const setOptgroup = (day) => {
        const row = [];
        timeslots[day].forEach((time) => {
            row.push(<option value={time}>{time}</option>);
        })
        return row;
    };

    const addNewMeeting = async (e) => {
        e.preventDefault()
        if (meeting.start_time === "") {
            alert("Please fill the time field")
        } else {
            let end_time = new Date(meeting.start_time)
            end_time.setMinutes(end_time.getMinutes() + event.duration + 180)

            const data = {
                host: event.host,
                event: event.id,
                start_time: meeting.start_time,
                end_time: end_time.toISOString().slice(0, 19),
                attendee_name: meeting.attendee_name,
                attendee_email: meeting.attendee_email,
                link: meeting.link,
                additional_info: meeting.additional_info
            }

            const resp = await MeetingService.postMeeting(data)
            if (resp.status === 201) {
                setMeeting(
                    {
                        attendee_name: "",
                        attendee_email: "",
                        additional_info: "",
                        start_time: "",
                        link: ""
                    }
                )
                alert("Meeting successfully created!")
                history.push('/about')
            } else {
                alert("Something went wrong while creating meeting. Please check input fields!")
            }
        }
    }
    if (!Object.keys(timeslots).length) {
        return (
            <h1 style={{textAlign: "center"}}>
                There are no free timeslots
            </h1>
        )
    }
    return (
        <form>
            <div style={{alignItem: 'center', marginTop: '10px'}}>
                <label htmlFor="time">Choose a start time:</label>
                <select
                    name="time"
                    id="time"
                    value={meeting.start_time}
                    onChange={event => setMeeting({...meeting, start_time: event.target.value})}
                    required={true}
                >
                    <option disabled value=""></option>
                    {Object.keys(timeslots).map((day) =>
                        <optgroup label={day}>
                            {setOptgroup(day)}
                        </optgroup>
                    )}
                </select>
            </div>
            <MyInput
                value={meeting.attendee_name}
                onChange={
                    e => {
                        setMeeting({...meeting, attendee_name: e.target.value})
                        validateField(e.target.value, e.target.name)
                    }
                }
                type="text"
                placeholder="name"
                name="attendee_name"
            />
            <div>{
                formState.formErrors["attendee_name"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["attendee_name"]}</h5>
                    : null
            }</div>
            <MyInput
                value={meeting.attendee_email}
                onChange={
                    e => {
                    setMeeting({...meeting, attendee_email: e.target.value})
                    validateField(e.target.value, e.target.name)
                    }
                }
                type="text"
                placeholder="email"
                name="attendee_email"
            />
            <div>{
                formState.formErrors["attendee_email"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["attendee_email"]}</h5>
                    : null
            }</div>
            <MyInput
                value={meeting.additional_info}
                onChange={e => setMeeting({...meeting, additional_info: e.target.value})}
                type="text"
                placeholder="description"
            />
            <MyInput
                value={meeting.link}
                onChange={e => setMeeting({...meeting, link: e.target.value})}
                type="text"
                placeholder="link"
            />
            <MyButton
                onClick={addNewMeeting}
                disabled={!formState.formValid}
            >
                Create meeting
            </MyButton>
        </form>
    );
};

export default MeetingForm;