import { writable } from 'svelte/store';
import { UnoState } from './uno-types';

export const createUnoStateStore = () => {
    const { subscribe, set, update } = writable<UnoState | undefined>(undefined)

    const eventSource = new EventSource(`/api/listen`)

    eventSource.onmessage = e => {
        update(_ => {
            const json = JSON.parse(e.data)
            return UnoState.parse(json)
        })
    }

    return {
        subscribe,
        reset: () => set(undefined),
        close: () => eventSource.close(),
    }
}
