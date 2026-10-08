import {Navigate,Route,Routes} from 'react-router'
import {AuthProvider} from './context/AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage';import RegisterPage from './pages/RegisterPage';import DashboardPage from './pages/DashboardPage';import CoursesPage from './pages/CoursesPage';import CourseDetailsPage from './pages/CourseDetailsPage';import ProfilePage from './pages/ProfilePage'
export default function App(){return <AuthProvider><Routes><Route path="/login" element={<LoginPage/>}/><Route path="/register" element={<RegisterPage/>}/><Route element={<Layout/>}><Route path="/" element={<Navigate to="/dashboard" replace/>}/><Route path="/dashboard" element={<ProtectedRoute><DashboardPage/></ProtectedRoute>}/><Route path="/courses" element={<ProtectedRoute><CoursesPage/></ProtectedRoute>}/><Route path="/courses/:id" element={<ProtectedRoute><CourseDetailsPage/></ProtectedRoute>}/><Route path="/profile" element={<ProtectedRoute><ProfilePage/></ProtectedRoute>}/><Route path="*" element={<Navigate to="/dashboard" replace/>}/></Route></Routes></AuthProvider>}
