import About from "../../pages/About";
import Login from "../../pages/Login";
import Events from "../../pages/Events";
import Meetings from "../../pages/Meetings";
import CreateMeeting from "../../pages/CreateMeeting";
import Register from "../../pages/Register";
import Error from "../../pages/Error";

export const publicRoutes=[
    {path: '/login', component: Login, exact: true},
    {path: '/events/:id', component: CreateMeeting, exact: true},
    {path: '/register', component: Register, exact: true},
    {path: '/error', component: Error, exact: true}
]

export const privateRoutes=[
    {path: '/events/:id', component: CreateMeeting, exact: true},
    {path: '/about', component: About, exact: true},
    {path: '/users/:id', component: Events, exact: true},
    {path: '/meetings', component: Meetings, exact: true},
    {path: '/error', component: Error, exact: true}
]