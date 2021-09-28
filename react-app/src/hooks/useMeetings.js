import {useMemo} from "react";

export const useSortedMeetings = (meetings, sort) =>{
    const sortedMeetings = useMemo(() => {
        if (sort) {
            return [...meetings].sort((a, b) => a[sort].localeCompare(b[sort]))
        }
        return meetings
    }, [sort, meetings])

    return sortedMeetings
}

export const useMeetings = (meetings, sort, query) => {
    const sortedMeetings = useSortedMeetings(meetings, sort)
    const searchedAndSortedMeetings = useMemo(() => {
        return sortedMeetings.filter(meeting => meeting.additional_info.toLowerCase().includes(query.toLowerCase()))
    }, [sortedMeetings, query])
    return searchedAndSortedMeetings
}