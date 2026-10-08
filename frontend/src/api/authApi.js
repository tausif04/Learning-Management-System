import api from './axios';
export const login=async(data)=>{const r=await api.post('/auth/token/',data); localStorage.setItem('access',r.data.access);localStorage.setItem('refresh',r.data.refresh);return r.data};
export const signup=(data)=>api.post('/auth/signup/',data);
export const profile=()=>api.get('/profile/'); export const updateProfile=(data)=>api.patch('/profile/',data);
