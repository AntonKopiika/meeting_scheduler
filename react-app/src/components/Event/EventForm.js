import React, {useState} from 'react';
import MyInput from "../UI/input/MyInput";
import MyButton from "../UI/button/MyButton";
import {useParams} from "react-router-dom";

const EventForm = ({create}) => {
    const params = useParams()
    const [event, setEvent] = useState({
        host: parseInt(params.id),
        title: "",
        description: "",
        start_time: "",
        end_time: "",
        duration: "",
        working_days: false,
        event_type: ""
    })

    const [formState, setFormState] = useState({
        formValid: false,
        formErrors: {
            title: '',
            start_time: '',
            end_time: '',
            duration: ''
        },
        titleValid: false,
        startTimeValid: false,
        endTimeValid: false,
        durationValid: false
    })

    const validateField = (value, fieldName) => {
        let fieldValidationErrors = {...formState.formErrors}
        let titleValid = formState.titleValid
        let startTimeValid = formState.startTimeValid
        let endTimeValid = formState.endTimeValid
        let durationValid = formState.durationValid
        const datePattern = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/
        switch (fieldName) {
            case "title":
                titleValid = value.length > 0
                fieldValidationErrors.title = titleValid ? '' : 'input your title, please'
                break
            case "start_time":
                startTimeValid = value.match(datePattern)
                fieldValidationErrors.start_time = startTimeValid ? '' : 'wrong date format'
                break
            case "end_time":
                endTimeValid = value.match(datePattern)
                fieldValidationErrors.end_time = endTimeValid ? '' : 'wrong date format'
                break
            case "duration":
                durationValid = !isNaN(value)
                fieldValidationErrors.duration = durationValid ? '' : 'wrong data format'
                break
            default:
                break;
        }
        setFormState({
            ...formState,
            formErrors: fieldValidationErrors,
            titleValid: titleValid,
            startTimeValid: startTimeValid,
            endTimeValid: endTimeValid,
            durationValid: durationValid,
            formValid: titleValid && startTimeValid && endTimeValid && durationValid
        });
    }
    const addNewEvent = (e) => {
        e.preventDefault()
        const newEvent = {
            ...event,
            duration: parseInt(event.duration),
            start_date: event.start_time.slice(0, 10),
            end_date: event.end_time.slice(0, 10)
        }
        create(newEvent)
        setEvent({
            title: "",
            description: "",
            start_time: "",
            end_time: "",
            duration: "",
            working_days: false,
            event_type: ""
        })
    }
    return (
        <form>
            <h1 style={{textAlign: 'center'}}>New event</h1>
            <MyInput
                value={event.title}
                onChange={e => {
                    setEvent({...event, title: e.target.value})
                    validateField(e.target.value, e.target.name)
                }}
                type="text"
                name="title"
                placeholder="title"
            />
            <div>{
                formState.formErrors["title"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["title"]}</h5>
                    : null
            }</div>
            <MyInput
                value={event.start_time}
                onChange={e => {
                    setEvent({...event, start_time: e.target.value})
                    validateField(e.target.value, e.target.name)
                }}
                type="text"
                name="start_time"
                placeholder="start time"
            />
            <div>{
                formState.formErrors["start_time"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["start_time"]}</h5>
                    : null
            }</div>
            <MyInput
                value={event.end_time}
                onChange={e => {
                    setEvent({...event, end_time: e.target.value})
                    validateField(e.target.value, e.target.name)
                }}
                type="text"
                name="end_time"
                placeholder="end time"
            />
            <div>{
                formState.formErrors["end_time"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["end_time"]}</h5>
                    : null
            }</div>
            <MyInput
                value={event.description}
                onChange={e => setEvent({...event, description: e.target.value})}
                type="text"
                placeholder="description"
            />

            <MyInput
                value={event.duration}
                onChange={e => {
                    setEvent({...event, duration: e.target.value})
                    validateField(e.target.value, e.target.name)
                }}
                type="text"
                name="duration"
                placeholder="duration"
            />
            <div>{
                formState.formErrors["duration"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["duration"]}</h5>
                    : null
            }</div>

            <MyInput
                value={event.event_type}
                onChange={e => setEvent({...event, event_type: e.target.value})}
                type="text"
                placeholder="event type"
            />
            <input
                type="checkbox"
                id="isWorkingDays"
                checked={event.working_days}
                onChange={e => {
                    setEvent({...event, working_days: e.target.checked})
                }}

            />
            <label htmlFor="isWorkingDays">Working days only</label>
            <br/>
            <MyButton
                style={{marginTop: '10px'}}
                onClick={addNewEvent}
                disabled={!formState.formValid}
            >Create event</MyButton>
        </form>
    );
};

export default EventForm;