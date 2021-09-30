import React, {useState} from 'react';
import MyInput from "../components/UI/input/MyInput";
import MyButton from "../components/UI/button/MyButton";
import UserService from "../components/API/UserService";
import {useHistory} from "react-router-dom";

const Register = () => {
    const [credentials, setCredentials] = useState(
        {
            username: "",
            password: "",
            confirm_password: ""
        })

    const history = useHistory();

    const [formState, setFormState] = useState({
        formValid: false,
        formErrors: {
            username: '',
            password: '',
            confirm_password: ''
        },
        usernameValid: false,
        passwordValid: false,
        confirmPasswordValid: false
    })

    const validateField = (value, fieldName) => {
        let fieldValidationErrors = {...formState.formErrors}
        let usernameValid = formState.usernameValid
        let passwordValid = formState.passwordValid
        let confirmPasswordValid = formState.confirmPasswordValid
        switch (fieldName) {
            case "username":
                usernameValid = value.length > 0
                fieldValidationErrors.username = usernameValid ? '' : 'input your title, please'
                break
            case "password":
                passwordValid = value.length > 0
                fieldValidationErrors.password = passwordValid ? '' : 'input your password, please'
                break
            case "confirm_password":
                confirmPasswordValid = (value === credentials.password)
                fieldValidationErrors.confirm_password = confirmPasswordValid ? '' : "passwords doesn't match"
                break
            default:
                break;
        }
        setFormState({
            ...formState,
            formErrors: fieldValidationErrors,
            usernameValid: usernameValid,
            passwordValid: passwordValid,
            confirmPasswordValid: confirmPasswordValid,
            formValid: formState.usernameValid && formState.passwordValid && formState.confirmPasswordValid
        });
    }

    const register = async (event) => {
        event.preventDefault()
        const response = await UserService.register({
            username: credentials.username,
            password: credentials.password
        })

        if (response.status === 201) {
            alert("Register successful")
            return history.push('/login')
        } else {
            alert("Something went wrong")
        }

        setCredentials(
            {
                username: "",
                password: "",
                confirm_password: ""
            })
    }
    return (
        <div>
            <h1 style={{textAlign: 'center'}}>Register</h1>
            <form>
                <MyInput
                    value={credentials.username}
                    onChange={e => {
                        setCredentials({...credentials, username: e.target.value})
                        validateField(e.target.value, e.target.name)
                    }}
                    type="text"
                    placeholder="username"
                    name="username"
                />
                <div>{
                    formState.formErrors["username"].length > 0
                        ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["username"]}</h5>
                        : null
                }</div>

                <MyInput
                    value={credentials.password}
                    onChange={e => {
                        setCredentials({...credentials, password: e.target.value})
                        validateField(e.target.value, e.target.name)
                    }}
                    type="password"
                    placeholder="password"
                    name="password"
                />
                <div>{
                    formState.formErrors["password"].length > 0
                        ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["password"]}</h5>
                        : null
                }</div>
                <MyInput
                    value={credentials.confirm_password}
                    onChange={e => {
                        setCredentials({...credentials, confirm_password: e.target.value})
                        validateField(e.target.value, e.target.name)
                    }}
                    type="password"
                    placeholder="confirm password"
                    name="confirm_password"
                />
                <div>{
                    formState.formErrors["confirm_password"].length > 0
                        ? <h5 style={{color: 'red', textAlign: 'center'}}>{formState.formErrors["confirm_password"]}</h5>
                        : null
                }</div>
                <div style={{textAlign: 'center'}}>
                <MyButton
                    onClick={register}
                    disabled={!formState.formValid}
                >Register</MyButton>
                </div>
            </form>
        </div>
    );
};

export default Register;