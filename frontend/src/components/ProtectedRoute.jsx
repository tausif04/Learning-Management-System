import {Navigate,useLocation} from 'react-router'
import {useAuth} from '../context/AuthContext'
export default function ProtectedRoute({children}){const{user,loading}=useAuth();const loc=useLocation();if(loading)return <div className="min-h-screen grid place-items-center text-slate-500">Loading your learning space…</div>;return user?children:<Navigate to="/login" replace state={{from:loc.pathname}}/>}
