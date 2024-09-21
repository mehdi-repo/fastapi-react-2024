import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import RegisterForm from './components/RegisterForm';
import LoginForm from './components/LoginForm';
import Home from './components/Home';
import ProductDetail from './components/ProductDetail'; 
import Orders from './components/Orders';

import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
    // Retrieve the access token within the component for real-time checks
    const isAuthenticated = !!localStorage.getItem('access_token');

    return (
        <Router>
            <Routes>
                {/* Public Routes */}
                <Route path="/" element={<Home />} />
                <Route path="/register" element={<RegisterForm />} />
                <Route path="/login" element={<LoginForm />} />
                <Route path="/product/:productId" element={<ProductDetail />} /> 
                <Route path='/orders' element={<Orders/> }/>

            </Routes>
        </Router>
    );
}

export default App;
