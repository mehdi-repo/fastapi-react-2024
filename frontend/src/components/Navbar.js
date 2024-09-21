import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
    const token = localStorage.getItem('access_token');
    const isAuthenticated = !!token;
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate('/login'); // Redirect to login page after logout
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <Link className="navbar-brand" to="/">FastAPI-React</Link>
            <div className="collapse navbar-collapse">
                <ul className="navbar-nav mr-auto">
                    <li className="nav-item">
                        <Link className="nav-link" to="/">Home</Link>
                    </li>
                    {isAuthenticated && (
                        <li className="nav-item">
                            <Link className="nav-link" to="/orders">Orders</Link>
                        </li>
                    )}
                    {!isAuthenticated ? (
                        <>
                            <li className="nav-item">
                                <Link className="nav-link" to="/login">Login</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/register">Register</Link>
                            </li>
                        </>
                    ) : (
                        <li className="nav-item">
                            <button className="btn btn-link nav-link" onClick={handleLogout}>Logout</button>
                        </li>
                    )}
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;
