document.addEventListener('DOMContentLoaded', function() {
    var slides = document.querySelectorAll('.slide');
    var currentIndex = 0;
    var autoplayInterval;

    function showSlide(index) {
        slides.forEach(function(slide) {
            slide.style.display = 'none';
        });
        slides[index].style.display = 'block';
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
    }

    function startAutoplay() {
        autoplayInterval = setInterval(nextSlide, 2000); // Change slide every 2 seconds
    }

    function stopAutoplay() {
        clearInterval(autoplayInterval);
    }

    // Show the first slide initially
    showSlide(currentIndex);

    // Event listeners for navigation buttons
    document.getElementById('prevBtn').addEventListener('click', function() {
        prevSlide();
    });

    document.getElementById('nextBtn').addEventListener('click', function() {
        nextSlide();
    });

    document.getElementById('autoplayBtn').addEventListener('click', function() {
        startAutoplay();
    });

    document.getElementById('stopAutoplayBtn').addEventListener('click', function() {
        stopAutoplay();
    });
});

