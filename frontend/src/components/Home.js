import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './Navbar';
import ImageSlider from './ImageSlider';
import ProductsGrid from './ProductsGrid';
import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/css/./Home.css'; 

const Home = ({ isAuthenticated }) => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        // Fetch products from API
        axios.get('http://127.0.0.1:8000/product/products/')
            .then(response => setProducts(response.data))
            .catch(error => console.error('Error fetching products:', error));
    }, []);

    const handleLogout = (navigate) => {
        localStorage.removeItem('access_token');
        navigate('/login');  // Redirect to login after logout
    };

    return (
        <div>
            <Navbar 
                isAuthenticated={isAuthenticated} 
                onLogout={(navigate) => handleLogout(navigate)} 
            />
            <ImageSlider />
            <ProductsGrid products={products} />
        </div>
    );
};

export default Home;
