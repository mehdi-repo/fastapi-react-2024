import React from 'react';
import { useNavigate } from 'react-router-dom';
import Carousel from 'react-bootstrap/Carousel';

const ProductsGrid = ({ products }) => {
    const navigate = useNavigate();

    const handleCardClick = (productId) => {
        navigate(`/product/${productId}`);
    };

    return (
        <div className="container mt-4">
            <div className="row">
                {products && products.length > 0 ? (
                    products.map(product => (
                        <div className="col-md-3 mb-4" key={product.id}>
                            <div
                                className="card"
                                style={{ width: '18rem', cursor: 'pointer' }}
                                onClick={() => handleCardClick(product.id)}
                            >
                                <Carousel>
                                    {product.image_urls && product.image_urls.length > 0 ? (
                                        product.image_urls.map((imageUrl, index) => (
                                            <Carousel.Item key={index}>
                                                <img
                                                    src={`http://127.0.0.1:8000${imageUrl}`}
                                                    className="d-block w-100"
                                                    alt={`Product ${product.name} Image ${index + 1}`}
                                                    style={{ height: '15rem', objectFit: 'cover' }}
                                                />
                                            </Carousel.Item>
                                        ))
                                    ) : (
                                        <Carousel.Item>
                                            <img
                                                src="https://via.placeholder.com/150"  // Placeholder image
                                                className="d-block w-100"
                                                alt="Placeholder"
                                                style={{ height: '15rem', objectFit: 'cover' }}
                                            />
                                        </Carousel.Item>
                                    )}
                                </Carousel>
                                <div className="card-body">
                                    <h5 className="card-title">{product.name}</h5>
                                    <p className="card-text">${product.price ? product.price.toFixed(2) : 'N/A'}</p>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="col-12">
                        <p>No products available.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ProductsGrid;
