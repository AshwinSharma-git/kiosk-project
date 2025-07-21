document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.tour-section');
    const prevBtn = document.querySelector('.prev-section');
    const nextBtn = document.querySelector('.next-section');
    const dotsContainer = document.querySelector('.navigation-dots');
    
    let currentSection = 0;

    // Create navigation dots
    sections.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => goToSection(index));
        dotsContainer.appendChild(dot);
    });

    // Initialize first section
    sections[0].classList.add('active');
    updateNavigation();

    // Navigation functions
    function goToSection(index) {
        if (index < 0 || index >= sections.length) return;
        
        sections[currentSection].classList.remove('active');
        dotsContainer.children[currentSection].classList.remove('active');
        
        currentSection = index;
        
        sections[currentSection].classList.add('active');
        dotsContainer.children[currentSection].classList.add('active');
        
        updateNavigation();
    }

    function updateNavigation() {
        prevBtn.disabled = currentSection === 0;
        nextBtn.disabled = currentSection === sections.length - 1;
    }

    // Event listeners
    prevBtn.addEventListener('click', () => {
        goToSection(currentSection - 1);
    });

    nextBtn.addEventListener('click', () => {
        goToSection(currentSection + 1);
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            goToSection(currentSection - 1);
        } else if (e.key === 'ArrowRight') {
            goToSection(currentSection + 1);
        }
    });

    // Lazy load videos
    const videos = document.querySelectorAll('.tour-video');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target;
                if (!video.hasAttribute('data-loaded')) {
                    const source = video.querySelector('source');
                    source.src = source.dataset.src;
                    video.load();
                    video.setAttribute('data-loaded', 'true');
                }
            }
        });
    }, {
        threshold: 0.1
    });

    videos.forEach(video => {
        observer.observe(video);
    });

    // Add smooth scroll animation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
