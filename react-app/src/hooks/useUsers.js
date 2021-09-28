import {useMemo} from "react";

export const useSortedUsers = (users, sort) =>{
    const sortedUsers = useMemo(() => {
        if (sort) {
            return [...users].sort((a, b) => a[sort].localeCompare(b[sort]))
        }
        return users
    }, [sort, users])

    return sortedUsers
}

export const useUsers = (users, sort, query) => {
    const sortedUsers = useSortedUsers(users, sort)
    const searchedAndSortedUsers = useMemo(() => {
        return sortedUsers.filter(user => user.username.toLowerCase().includes(query.toLowerCase()))
    }, [sortedUsers, query])
    return searchedAndSortedUsers
}