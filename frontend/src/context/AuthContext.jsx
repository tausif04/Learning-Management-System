import {createContext,useContext,useEffect,useState} from 'react'
import {api,saveTokens,clearAuth} from '../lib/api'
const AuthContext=createContext(null)
export function AuthProvider({children}){
 const [user,setUser]=useState(()=>{try{return JSON.parse(localStorage.getItem('user'))}catch{return null}}),[loading,setLoading]=useState(true)
 useEffect(()=>{if(localStorage.getItem('access'))api.profile().then(u=>{setUser(u);localStorage.setItem('user',JSON.stringify(u))}).catch(()=>{}).finally(()=>setLoading(false));else setLoading(false)},[])
 const login=async body=>{const t=await api.login(body);saveTokens(t);const u=await api.profile();setUser(u);localStorage.setItem('user',JSON.stringify(u));return u}
 const signup=async body=>api.signup(body)
 const update=async body=>{const u=await api.updateProfile(body);setUser(u);localStorage.setItem('user',JSON.stringify(u));return u}
 const logout=()=>{clearAuth();setUser(null)}
 return <AuthContext.Provider value={{user,loading,login,signup,update,logout}}>{children}</AuthContext.Provider>
}
export const useAuth=()=>useContext(AuthContext)
