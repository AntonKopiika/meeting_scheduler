import React from 'react';
import MyButton from "../UI/button/MyButton";

const EventItem = (props) => {
    const copyEventLink = async () => {
        if (!navigator.clipboard) {
            // Clipboard API not available
            return
        }
        const text = `http://127.0.0.1:3000/events/${props.event.id}`
        try {
            await navigator.clipboard.writeText(text)
            document.getElementById(`copyButton${props.event.id}`).childNodes[0].nodeValue = "Copied";
        } catch (err) {
            console.error('Failed to copy!', err)
        }
    }

    return (
        <div className="block">
            <div className="block__content">
                <strong>{props.event.title}</strong>
                <div>
                    <h5>Time: {props.event.start_time}-{props.event.end_time}</h5>
                    <h5>Description: {props.event.description}</h5>
                </div>
            </div>
            <div className="block__btns">
                <MyButton
                    style={{display: 'inline-block'}}
                    id={`copyButton${props.event.id}`}
                    onClick={() => copyEventLink()}
                >
                    Copy link
                </MyButton>
                <form
                    action={`http://127.0.0.1:3000/events/${props.event.id}`}
                    style={{display: 'inline-block'}}
                >
                    <MyButton type="submit">View create page</MyButton>
                </form>
                <MyButton
                    style={{display: 'inline-block'}}
                    onClick={() => props.editModal(props.event)}
                >
                    Edit
                </MyButton>
                <MyButton
                    style={{display: 'inline-block'}}
                    onClick={() => props.remove(props.event)}
                >
                    Remove
                </MyButton>
            </div>
        </div>
    )
        ;
};

export default EventItem;