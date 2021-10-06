// Функция записи токена в хранилище данных 
export function setToken (context, data) { 
    context.commit('setToken', data) 
} 
// Функция записи имени пользователя в хранилище данных 
export function setUsername (context, data) { 
    context.commit('setUsername', data) 
} 
// Функция установки признака авторизации в хранилище данных 
export function setAuth (context) { 
    context.commit('setAuth', true) 
} 
// Функция переключения языка интерфейса в хранилище данных 
export function setLang (context, data) { 
    context.commit('setLang', data) 
}
// Функция установки количества строк пагинации по умолчанию
export function setRows (context, data) { 
    context.commit('setRows', data) 
} 
// Функция установки времени автоматического обновления данных
export function setAutoUpdate (context, data) { 
    context.commit('setAutoUpdate', data) 
} 
// Функция сброса всех полей хранилища данных 
export function unsetStorage (context) { 
    context.commit('unsetToken') 
    context.commit('unsetUsername') 
    context.commit('unsetAuth') 
    context.commit('unsetLang') 
    context.commit('unsetRows') 
    context.commit('unsetAutoUpdate') 
}
