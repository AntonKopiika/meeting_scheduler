import React from 'react';

const ErrorMessage = ({formState}) => {
    return (
        <div>{
            formState.formErrors["title"].length > 0
                ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["title"]}</h5>
                : null
        }</div>
    );
};

export default ErrorMessage;