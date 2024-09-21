import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';

function LoginForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Create URLSearchParams object
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);
        // The OAuth2PasswordRequestForm expects application/x-www-form-urlencoded data, not JSON.
        try {
            const response = await axios.post('http://127.0.0.1:8000/user/login', params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });

            if (response.status === 200) {
                // Store token in localStorage or handle accordingly
                localStorage.setItem('access_token', response.data.access_token);
                navigate('/');
            }
        } catch (error) {
            setError('Error logging in: ' + (error.response?.data?.detail || error.message));
        }
    };

    return (
        <div>
            <Navbar />
            <div className="d-flex justify-content-center align-items-center min-vh-100">
                <div className="card">
                    <div className="card-body">
                        <h2 className="card-title text-center mb-4">Login</h2>
                        {error && <div className="alert alert-danger">{error}</div>}
                        <form onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label htmlFor="username" className="form-label">Username:</label>
                                <input
                                    type="text"
                                    id="username"
                                    className="form-control"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="mb-3">
                                <label htmlFor="password" className="form-label">Password:</label>
                                <input
                                    type="password"
                                    id="password"
                                    className="form-control"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                            <button type="submit" className="btn btn-primary w-100">Login</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoginForm;
