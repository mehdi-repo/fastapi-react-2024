import React from 'react';
import Carousel from 'react-bootstrap/Carousel';
import img1 from './assets/img/1.jpg';
import img2 from './assets/img/2.jpg';
import img3 from './assets/img/3.jpg';
import './assets/css/ImageSlider.css'; // Ensure this path is correct

const ImageSlider = () => {
    return (
        <Carousel>
            <Carousel.Item>
                <img
                    className="d-block img-size" // Ensure img-size is defined in ImageSlider.css
                    src={img1}
                    alt="First slide"
                />
                <Carousel.Caption>
                    <h3>First Slide Title</h3>
                    <p><a href="https://example.com" className="text-white">Learn More</a></p>
                </Carousel.Caption>
            </Carousel.Item>
            <Carousel.Item>
                <img
                    className="d-block img-size"
                    src={img2}
                    alt="Second slide"
                />
                <Carousel.Caption>
                    <h3>Second Slide Title</h3>
                    <p><a href="https://example.com" className="text-white">Learn More</a></p>
                </Carousel.Caption>
            </Carousel.Item>
            <Carousel.Item>
                <img
                    className="d-block img-size"
                    src={img3}
                    alt="Third slide"
                />
                <Carousel.Caption>
                    <h3>Third Slide Title</h3>
                    <p><a href="https://example.com" className="text-white">Learn More</a></p>
                </Carousel.Caption>
            </Carousel.Item>
        </Carousel>
    );
};

export default ImageSlider;
