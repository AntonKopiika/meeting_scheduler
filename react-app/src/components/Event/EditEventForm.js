import React, {useState} from 'react';
import MyInput from "../UI/input/MyInput";
import MyButton from "../UI/button/MyButton";

const EditEventForm = ({editedEvent, setEditedEvent, update}) => {
    const [formState, setFormState] = useState({
        formValid: true,
        formErrors: {
            title: '',
            start_time: '',
            end_time: '',
            duration: ''
        },
        titleValid: true,
        startTimeValid: true,
        endTimeValid: true,
        durationValid: true
    })
    const validateField = (value, fieldName) => {
        let fieldValidationErrors = {...formState.formErrors}
        let titleValid = formState.titleValid
        let startTimeValid = formState.startTimeValid
        let endTimeValid = formState.endTimeValid
        let durationValid = formState.durationValid
        const datePattern = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/
        switch (fieldName) {
            case "title":
                titleValid = value.length > 0
                fieldValidationErrors.title = titleValid ? '' : 'input your title, please'
                break
            case "start_time":
                startTimeValid = !!value.match(datePattern)
                fieldValidationErrors.start_time = startTimeValid ? '' : 'wrong date format'
                break
            case "end_time":
                endTimeValid = !!value.match(datePattern)
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
            formValid: formState.titleValid && formState.startTimeValid && formState.endTimeValid && formState.durationValid
        });
    }
    const editEvent = (e) => {
        e.preventDefault()
        setEditedEvent({
            ...editedEvent,
            duration: parseInt(editedEvent.duration),
            start_date: editedEvent.start_time.slice(0, 10),
            end_date: editedEvent.end_time.slice(0, 10)
        })
        update(editedEvent)
    }
    return (
        <form>
            <h1 style={{textAlign: 'center'}}>Edit event</h1>
            <MyInput
                value={editedEvent.title}
                onChange={e => {
                    setEditedEvent({...editedEvent, title: e.target.value})
                    validateField(e.target.value, e.target.name)
                }}
                type="text"
                placeholder="title"
                name="title"
                id="title"
            />
            <div>{
                formState.formErrors["title"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["title"]}</h5>
                    : null
            }</div>
            <MyInput
                value={editedEvent.start_time}
                onChange={e => {
                    setEditedEvent({...editedEvent, start_time: e.target.value})
                    validateField(e.target.value, e.target.name)
                }}
                type="text"
                placeholder="start time"
                name="start_time"
            />
            <div>{
                formState.formErrors["start_time"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["start_time"]}</h5>
                    : null
            }</div>
            <MyInput
                value={editedEvent.end_time}
                onChange={e => {
                    setEditedEvent({...editedEvent, end_time: e.target.value})
                    validateField(e.target.value, e.target.name)
                }}
                type="text"
                placeholder="end time"
                name="end_time"
            />
            <div>{
                formState.formErrors["end_time"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["end_time"]}</h5>
                    : null
            }</div>
            <MyInput
                value={editedEvent.description}
                onChange={e => setEditedEvent({...editedEvent, description: e.target.value})}
                type="text"
                placeholder="description"
            />

            <MyInput
                value={editedEvent.duration}
                onChange={e => {
                    setEditedEvent({...editedEvent, duration: e.target.value})
                    validateField(e.target.value, e.target.name)
                }}
                type="text"
                placeholder="duration"
                name="duration"
            />
            <div>{
                formState.formErrors["duration"].length > 0
                    ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["duration"]}</h5>
                    : null
            }</div>

            <MyInput
                value={editedEvent.event_type}
                onChange={e => setEditedEvent({...editedEvent, event_type: e.target.value})}
                type="text"
                placeholder="event type"
            />
            <input
                type="checkbox"
                id="isWorkingDays"
                checked={editedEvent.working_days}
                onChange={e => {
                    setEditedEvent({...editedEvent, working_days: e.target.checked})
                }}
            />
            <label htmlFor="isWorkingDays">Working days only</label>
            <br/>
            <MyButton style={{marginTop: '10px'}} onClick={editEvent} disabled={!formState.formValid}>Edit</MyButton>
        </form>
    );
};

export default EditEventForm;