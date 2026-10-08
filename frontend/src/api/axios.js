import axios from 'axios';
const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://127.0.0.1:8000/api'});
api.interceptors.request.use(c=>{const t=localStorage.getItem('access'); if(t)c.headers.Authorization=`Bearer ${t}`; return c});
api.interceptors.response.use(r=>r,async e=>{if(e.response?.status===401&&localStorage.getItem('refresh')){try{const r=await axios.post(`${api.defaults.baseURL}/auth/token/refresh/`,{refresh:localStorage.getItem('refresh')});localStorage.setItem('access',r.data.access);e.config.headers.Authorization=`Bearer ${r.data.access}`;return api(e.config)}catch{localStorage.clear();location.href='/login'}} return Promise.reject(e)});
export default api;
