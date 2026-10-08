import api from './axios';
export const courses=()=>api.get('/courses/'); export const course=(id)=>api.get(`/courses/${id}/`); export const enroll=(id)=>api.post(`/courses/${id}/enroll/`); export const enrolled=()=>api.get('/enrollments/'); export const completeLesson=(id)=>api.post(`/lessons/${id}/complete/`);
