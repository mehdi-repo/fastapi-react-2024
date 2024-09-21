import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ element }) => {
    const token = localStorage.getItem('access_token');
    return token ? element : <Navigate to="/login" />;
};

export default PrivateRoute;
