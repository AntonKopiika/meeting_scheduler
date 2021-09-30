import React, {useEffect, useState} from "react";
import './styles/App.css'
import {BrowserRouter} from "react-router-dom";
import Navbar from "./components/UI/navbar/Navbar";
import AppRouter from "./components/AppRouter";
import {AuthContext} from "./components/context";

function App() {
    const [isAuth, setIsAuth] = useState(false)
    const [isLoading, setIsLoading] = useState(true)
    const [userId, setUserId] = useState(0)
    const [isOutlookAuth, setIsOutlookAuth] = useState(false)

    useEffect(() => {
        if (localStorage.getItem('auth')){
            setIsAuth(true)
            setUserId(parseInt(localStorage.getItem('auth')))
        }
        if (sessionStorage.getItem('is_outlook_auth')){
            setIsOutlookAuth(true)
        }
        if (sessionStorage.getItem('user_id')){
            setUserId(parseInt(sessionStorage.getItem('user_id')))
        }
        setIsLoading(false)

    }, [])
    return (
        <AuthContext.Provider value={{
            isAuth,
            setIsAuth,
            isLoading,
            userId,
            setUserId,
            isOutlookAuth,
            setIsOutlookAuth
        }}>
            <BrowserRouter>
                <Navbar/>
                <AppRouter/>
            </BrowserRouter>
        </AuthContext.Provider>
    );
}

export default App;
