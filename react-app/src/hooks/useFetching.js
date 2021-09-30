import {useContext, useState} from "react";
import {useHistory} from "react-router-dom";
import {AuthContext} from "../components/context";

export const useFetching = (callback) => {
    const {setIsAuth} = useContext(AuthContext)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState("")
    const history = useHistory()
    const fetching = async () => {
        try {
            setIsLoading(true)
            await callback()
        } catch (e){
            switch (e.response.status){
                case 401:
                    setIsAuth(false)
                    localStorage.removeItem('auth')
                    sessionStorage.removeItem('user_id')
                    sessionStorage.removeItem('is_outlook_auth')
                    localStorage.removeItem('token')
                    history.push("/error")
                    break
                default:
                    setError(e.message)
                    break
            }
        } finally {
            setIsLoading(false)
        }
    }
    return [fetching, isLoading, error]
}