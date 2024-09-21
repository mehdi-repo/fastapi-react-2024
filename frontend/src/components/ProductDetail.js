import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const ProductDetail = () => {
    const { productId } = useParams();
    const navigate = useNavigate();
    const [product, setProduct] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userId, setUserId] = useState(null);
    const [quantity, setQuantity] = useState(1); // Default quantity
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        // Check if the user is authenticated
        const token = localStorage.getItem('access_token');
        if (token) {
            setIsAuthenticated(true);
            const decodedToken = JSON.parse(atob(token.split('.')[1])); // Decode JWT token
            setUserId(decodedToken.user_id); // Extract user ID from token
        } else {
            setIsAuthenticated(false);
        }

        // Fetch product details
        axios.get(`http://127.0.0.1:8000/product/products/${productId}`)
            .then(response => setProduct(response.data))
            .catch(error => console.error('Error fetching product:', error));
    }, [productId]);

    const handleBuy = () => {
        if (!isAuthenticated || !userId) {
            navigate('/login');
            return;
        }

        const token = localStorage.getItem('access_token');

        const orderData = {
            user_id: userId,
            items: [{
                product_id: product.id,
                quantity: quantity // Use selected quantity
            }]
        };

        axios.post(`http://127.0.0.1:8000/order/orders/?token=${token}`, orderData, {
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        })
        .then(response => {
            setSuccessMessage('Purchase successful!');
            setErrorMessage('');  // Clear any previous errors
        })
        .catch(error => {
            console.error('Error placing order:', error);
            setErrorMessage('Failed to place the order.');
            setSuccessMessage('');  // Clear any previous successes
        });
    };

    if (!product) return <div>Loading...</div>;

    return (
        <div>
            <Navbar />
            <div className="container mt-4">
                {successMessage && <div className="alert alert-info">{successMessage}</div>}
                {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
                <div className="row">
                    <div className="col-md-6">
                        <img
                            src={`http://127.0.0.1:8000${product.image_urls[0]}`}
                            className="img-fluid"
                            alt={product.name}
                            style={{ maxHeight: '400px', objectFit: 'cover' }}
                        />
                    </div>
                    <div className="col-md-6 d-flex flex-column justify-content-between">
                        <div>
                            <h2>{product.name}</h2>
                            <p>{product.description}</p>
                        </div>
                        <div>
                            <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
                            <div className="form-group">
                                <label htmlFor="quantity">Quantity</label>
                                <input
                                    type="number"
                                    id="quantity"
                                    className="form-control"
                                    value={quantity}
                                    onChange={(e) => setQuantity(Number(e.target.value))}
                                    min="1" // Ensure quantity is at least 1
                                />
                            </div>
                            <button className="btn btn-primary mt-3" onClick={handleBuy}>
                                Buy
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductDetail;
