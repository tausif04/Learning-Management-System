const BASE=(import.meta.env.VITE_API_URL||'http://127.0.0.1:8000/api').replace(/\/$/,'')
let refreshing=null
const getAccess=()=>localStorage.getItem('access')
const saveTokens=(d)=>{if(d.access)localStorage.setItem('access',d.access);if(d.refresh)localStorage.setItem('refresh',d.refresh)}
const clearAuth=()=>{localStorage.removeItem('access');localStorage.removeItem('refresh');localStorage.removeItem('user')}
async function request(path,options={},retry=true){
  const headers={'Content-Type':'application/json',...(options.headers||{})}; const token=getAccess(); if(token)headers.Authorization=`Bearer ${token}`
  const res=await fetch(`${BASE}${path}`,{...options,headers});
  if(res.status===401&&retry&&localStorage.getItem('refresh')){
    try{await refreshToken();return request(path,options,false)}catch{clearAuth();window.location.href='/login'}
  }
  const text=await res.text(); let data=null; try{data=text?JSON.parse(text):null}catch{data=text}
  if(!res.ok)throw Object.assign(new Error(data?.detail||'Request failed'),{status:res.status,data})
  return data
}
async function refreshToken(){
  if(!refreshing)refreshing=fetch(`${BASE}/token/refresh/`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh:localStorage.getItem('refresh')})}).then(async r=>{if(!r.ok)throw Error('Refresh failed');const d=await r.json();saveTokens(d);return d}).finally(()=>{refreshing=null})
  return refreshing
}
export const api={
  login:(body)=>request('/token/',{method:'POST',body:JSON.stringify(body)},false),
  signup:(body)=>request('/user/auth/',{method:'POST',body:JSON.stringify(body)},false),
  profile:()=>request('/user/profile/'),
  updateProfile:(body)=>request('/user/profile/',{method:'PATCH',body:JSON.stringify(body)}),
  categories:()=>request('/categories/'),
  courses:()=>request('/courses/'),
  course:(id)=>request(`/courses/${id}/`),
  lessons:(course)=>request(`/lessons/${course?`?course=${course}`:''}`),
  enrollments:()=>request('/enrollments/'),
  enroll:(course)=>request('/enrollments/enroll/',{method:'POST',body:JSON.stringify({course})}),
  complete:(id)=>request(`/lessons/${id}/complete/`,{method:'POST'}),
  uncomplete:(id)=>request(`/lessons/${id}/complete/`,{method:'DELETE'}),
  questions:(course)=>request(`/questions/${course?`?course=${course}`:''}`),
  ask:(body)=>request('/questions/',{method:'POST',body:JSON.stringify(body)}),
}
export {saveTokens,clearAuth,getAccess}
