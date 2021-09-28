import {useMemo} from "react";

export const useSortedEvents = (events, sort) =>{
    const sortedEvents = useMemo(() => {
        if (sort) {
            return [...events].sort((a, b) => a[sort].localeCompare(b[sort]))
        }
        return events
    }, [sort, events])

    return sortedEvents
}

export const useEvents = (events, sort, query) => {
    const sortedEvents = useSortedEvents(events, sort)
    const searchedAndSortedEvents = useMemo(() => {
        return sortedEvents.filter(e => e.title.toLowerCase().includes(query.toLowerCase()))
    }, [sortedEvents, query])
    return searchedAndSortedEvents
}