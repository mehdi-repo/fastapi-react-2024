import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Carousel, Card, Row, Col } from 'react-bootstrap';  // Import necessary components from Bootstrap
import Navbar from './Navbar';

const Orders = () => {
    const [orders, setOrders] = useState([]);
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [userId, setUserId] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    // Check if the user is authenticated and extract user ID from token
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                const decodedToken = JSON.parse(atob(token.split('.')[1])); // Decode JWT token
                setUserId(decodedToken.user_id); // Extract user ID
                setIsAuthenticated(true);
            } catch (error) {
                console.error('Error decoding token:', error);
                setIsAuthenticated(false);
                setError('Invalid token. Please log in again.');
            }
        } else {
            setIsAuthenticated(false);
        }
    }, []);

    // Fetch orders using the token as a query parameter
    useEffect(() => {
        const fetchOrders = async () => {
            if (!userId) return;

            const token = localStorage.getItem('access_token');  // Fetch the token again
            const endpoint = `http://127.0.0.1:8000/order/users/${userId}/order-details/?token=${token}`;

            try {
                const response = await axios.get(endpoint, {
                    headers: {
                        'Content-Type': 'application/json',
                        'accept': 'application/json',
                    }
                });
                setOrders(response.data);
                setSuccessMessage('Orders fetched successfully!');
                setError('');  // Clear any previous errors
            } catch (error) {
                setError('Failed to fetch orders.');
                setSuccessMessage('');  // Clear any previous successes
                console.error('Error fetching orders:', error);
            }
        };

        if (isAuthenticated && userId) {
            fetchOrders();
        } else if (!isAuthenticated) {
            setError('You must be logged in to view orders.');
        }
    }, [userId, isAuthenticated]);

    return (

        <div>
            <Navbar />



            <div className="container mt-4">

                <h2>My Orders</h2>
                {successMessage && <div className="alert alert-info">{successMessage}</div>}
                {error && <div className="alert alert-danger">{error}</div>}
                {orders.length === 0 ? (
                    <p>No orders found.</p>
                ) : (
                    <Row>
                        {orders.map(order => (
                            <Col key={order.order_id} md={3} className="mb-4">
                                <Card>
                                    <Card.Body>
                                        <Card.Title>Order ID: {order.order_id}</Card.Title>
                                        <Card.Subtitle className="mb-2 text-muted">
                                            Total Price: ${order.total_order_price.toFixed(2)}
                                        </Card.Subtitle>
                                        <Card.Text>
                                            <h6>Items:</h6>
                                            {order.items && order.items.length > 0 ? (
                                                order.items.map(item => (
                                                    <div key={item.product_name} className="mb-2">
                                                        {/* Display images in a Carousel */}
                                                        {item.images && item.images.length > 0 && (
                                                            <Carousel>
                                                                {item.images.map((image, index) => (
                                                                    <Carousel.Item key={index}>
                                                                        <img
                                                                            src={`http://127.0.0.1:8000${image}`}  // Correct image URL construction
                                                                            alt={`Image of ${item.product_name}`}
                                                                            className="d-block w-100"
                                                                            style={{ height: '150px', objectFit: 'cover' }}  // Set height and fit
                                                                        />
                                                                    </Carousel.Item>
                                                                ))}
                                                            </Carousel>
                                                        )}
                                                        <h6>Product Name: {item.product_name}</h6>
                                                        <p><strong>Description:</strong> {item.description || 'N/A'}</p>
                                                        <p><strong>Price per Unit:</strong> ${item.price_per_unit.toFixed(2)}</p>
                                                        <p><strong>Quantity:</strong> {item.quantity}</p>
                                                        <p><strong>Total Price for Item:</strong> ${item.total_price_for_item.toFixed(2)}</p>
                                                    </div>
                                                ))
                                            ) : (
                                                <p>No items found.</p>
                                            )}
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                        ))}
                    </Row>
                )}
            </div>
        </div>
    );
};

export default Orders;
