import React, {useContext} from 'react';
import {Link, useHistory} from "react-router-dom";
import MyButton from "../button/MyButton";
import {AuthContext} from "../../context";

const Navbar = () => {
    const {isAuth, setIsAuth, userId} = useContext(AuthContext)
    const history = useHistory();
    const logout = () => {
        setIsAuth(false)
        localStorage.removeItem('auth')
        sessionStorage.removeItem('user_id')
        sessionStorage.removeItem('is_outlook_auth')
        sessionStorage.removeItem('token')
        return history.push('/login')
    }

    const loginRedirect = () => {
        return history.push('/login')
    }

    const registerRedirect = () => {
        return history.push('/register')
    }


    return (
        <div className="navbar">
            {isAuth
                ?
                <MyButton
                    onClick={logout}
                >
                    Logout
                </MyButton>
                :
                <div>
                    <MyButton
                        onClick={loginRedirect}
                    >
                        Login
                    </MyButton>
                    <MyButton
                        onClick={registerRedirect}
                    >
                        Register
                    </MyButton>
                </div>

            }
            <div className="navbar__links">
                {isAuth
                    ?
                    <div>
                        <Link
                            className="navbar__item"
                            to="/about"
                        >
                            About
                        </Link>
                        <Link
                            className="navbar__item"
                            to="/meetings"
                        >
                            Meetings
                        </Link>
                        <Link
                            className="navbar__item"
                            to={`/user/${userId}`}
                        >
                            Events
                        </Link>
                        <a
                            className="navbar__item"
                            href="http://127.0.0.1:5000/auth_login"
                        >
                            Sign in Outlook
                        </a>
                    </div>
                    :
                    null
                    }
            </div>
        </div>
    );
};

export default Navbar;