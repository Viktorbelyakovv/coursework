export function setToken (state, data) { 
    state.token = data 
} 
export function unsetToken (state) { 
    state.token = '' 
} 
export function setUsername (state, data) { 
    state.username = data 
} 
export function unsetUsername (state) { 
    state.username = '' 
} 
export function setAuth (state, data) {
    state.auth = data 
} 
export function unsetAuth (state) { 
    state.auth = '' 
}
export function setLang (state, data) {
    state.lang = data 
} 
export function unsetLang (state) { 
    state.lang = 'ru' 
}
export function setRows (state, data) {
    state.rows = data 
} 
export function unsetRows (state) { 
    state.rows = 10 
}
export function setAutoUpdate (state, data) {
    state.autoUpdate = data 
} 
export function unsetAutoUpdate (state) { 
    state.autoUpdate = 10
}