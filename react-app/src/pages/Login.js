import React, {useContext, useState} from 'react';
import MyInput from "../components/UI/input/MyInput";
import MyButton from "../components/UI/button/MyButton";
import {AuthContext} from "../components/context";
import UserService from "../components/API/UserService";

const Login = () => {
    const {setIsAuth, setUserId} = useContext(AuthContext)
    const [credentials, setCredentials] = useState(
        {
            username: "",
            password: ""
        })
    const [formState, setFormState] = useState({
        formValid: false,
        formErrors: {username: '', password: ''},
        usernameValid: false,
        passwordValid: false
    })

    const validateField = (value, fieldName) => {
        let fieldValidationErrors = {...formState.formErrors};
        let usernameValid = formState.usernameValid;
        let passwordValid = formState.passwordValid;
        switch (fieldName) {
            case "username":
                usernameValid = value.length > 0
                fieldValidationErrors.username = usernameValid ? '' : 'input your username, please'
                break
            case "password":
                passwordValid = value.length > 0
                fieldValidationErrors.password = passwordValid ? '' : 'input your password, please'
                break
            default:
                break;
        }
        setFormState({
            ...formState,
            formErrors: fieldValidationErrors,
            usernameValid: usernameValid,
            passwordValid: passwordValid,
            formValid: formState.usernameValid && formState.passwordValid
        });
    }


    const login = async (event) => {
        event.preventDefault()
        const data = await UserService.login(credentials)
        if (!data.error) {
            sessionStorage.setItem('token', `${data.access_token}`)
            setUserId(data.id)
            setIsAuth(true)
            localStorage.setItem('auth', data.id)
            sessionStorage.setItem('user_id', `${data.id}`)
            if (data.accounts) {
                sessionStorage.setItem("is_outlook_auth", 'true')
            }
        } else {
            alert("Wrong username or password")
        }
        setCredentials(
            {
                username: "",
                password: ""
            })
    }
    return (
        <div>
            <h1 style={{textAlign: 'center'}}>Login</h1>
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
                <div style={{textAlign: 'center'}}>
                    <MyButton disabled={!formState.formValid} onClick={login}>Login</MyButton>
                </div>
            </form>
        </div>
    );
};

export default Login;