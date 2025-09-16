// Mobile Hamburger Menu Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const navMenu = document.getElementById('nav-menu');
    const body = document.body;

    // Toggle menu function
    function toggleMenu() {
        hamburgerMenu.classList.toggle('active');
        navMenu.classList.toggle('active');
        
        // Prevent body scroll when menu is open
        if (navMenu.classList.contains('active')) {
            body.style.overflow = 'hidden';
        } else {
            body.style.overflow = 'auto';
        }
    }

    // Close menu function
    function closeMenu() {
        hamburgerMenu.classList.remove('active');
        navMenu.classList.remove('active');
        body.style.overflow = 'auto';
    }

    // Event listeners
    if (hamburgerMenu) {
        hamburgerMenu.addEventListener('click', toggleMenu);
    }

    // Close menu when clicking on menu links
    const menuLinks = navMenu.querySelectorAll('a');
    menuLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Close menu when clicking outside of it
    document.addEventListener('click', function(event) {
        if (!hamburgerMenu.contains(event.target) && !navMenu.contains(event.target)) {
            closeMenu();
        }
    });

    // Close menu on window resize (if screen becomes larger)
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeMenu();
        }
    });

    // Close menu on escape key press
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeMenu();
        }
    });

    // Active navigation highlighting
    function setActiveNavItem() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('#nav-menu a');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const linkPath = new URL(link.href).pathname;
            
            if (linkPath === currentPath || 
                (currentPath === '/' && linkPath === '/about_me') ||
                (currentPath === '/tetris' && linkPath === '/tetris') ||
                (currentPath === '/resume' && linkPath === '/resume') ||
                (currentPath === '/contact' && linkPath === '/contact')) {
                link.classList.add('active');
            }
        });
    }

    // Set active nav item on page load
    setActiveNavItem();

    // Resume download functionality
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            // Create a new window for printing
            const printWindow = window.open('', '_blank');
            const resumeContent = document.querySelector('.resume-container').innerHTML;
            
            printWindow.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Ogunjimi Samuel Seye - Resume</title>
                    <style>
                        body { 
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                            margin: 0; 
                            padding: 20px; 
                            background: white;
                        }
                        .resume-container {
                            max-width: 1200px;
                            margin: 0 auto;
                            background: #ffffff;
                            border-radius: 15px;
                            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                            overflow: hidden;
                        }
                        .resume-header {
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            padding: 40px;
                            text-align: center;
                        }
                        .name {
                            font-size: 3rem;
                            font-weight: 700;
                            margin-bottom: 20px;
                            letter-spacing: 1px;
                        }
                        .contact-info {
                            display: flex;
                            justify-content: center;
                            flex-wrap: wrap;
                            gap: 30px;
                            margin-top: 20px;
                        }
                        .contact-item {
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            gap: 5px;
                        }
                        .contact-label {
                            font-size: 0.9rem;
                            opacity: 0.9;
                            font-weight: 500;
                        }
                        .contact-link {
                            color: white;
                            text-decoration: none;
                            font-weight: 600;
                        }
                        .resume-content {
                            display: grid;
                            grid-template-columns: 1fr 1fr;
                            gap: 0;
                            min-height: 800px;
                        }
                        .left-column, .right-column {
                            padding: 40px;
                        }
                        .left-column {
                            background: #f8f9fa;
                            border-right: 1px solid #e9ecef;
                        }
                        .section-title {
                            font-size: 1.4rem;
                            font-weight: 700;
                            color: #2c3e50;
                            margin-bottom: 15px;
                            padding-bottom: 8px;
                            border-bottom: 3px solid #3498db;
                        }
                        .summary-text {
                            line-height: 1.6;
                            color: #000000;
                            font-size: 1rem;
                            text-align: justify;
                        }
                        .competencies-list, .job-responsibilities, .certifications-list {
                            list-style: none;
                            padding: 0;
                        }
                        .competencies-list li, .job-responsibilities li, .certifications-list li {
                            padding: 8px 0;
                            border-bottom: 1px solid #ecf0f1;
                            position: relative;
                            padding-left: 20px;
                            color: #030303;
                            line-height: 1.5;
                        }
                        .competencies-list li::before, .job-responsibilities li::before, .certifications-list li::before {
                            content: '▶';
                            position: absolute;
                            left: 0;
                            color: #3498db;
                            font-size: 0.8rem;
                        }
                        .experience-item {
                            margin-bottom: 25px;
                            padding: 20px;
                            background: white;
                            border-radius: 8px;
                            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                            border-left: 4px solid #3498db;
                        }
                        .job-title {
                            font-size: 1.2rem;
                            font-weight: 700;
                            color: #2c3e50;
                            margin-bottom: 5px;
                        }
                        .company-name {
                            font-size: 1rem;
                            color: #000000;
                            font-weight: 600;
                            margin-bottom: 5px;
                        }
                        .job-duration {
                            font-size: 0.9rem;
                            color: #e74c3c;
                            font-weight: 600;
                            margin-bottom: 15px;
                        }
                        .education-item {
                            margin-bottom: 20px;
                            padding: 15px;
                            background: #f8f9fa;
                            border-radius: 8px;
                            border-left: 4px solid #27ae60;
                        }
                        .degree {
                            font-size: 1.1rem;
                            font-weight: 700;
                            color: #2c3e50;
                            margin-bottom: 5px;
                        }
                        .institution {
                            font-size: 0.95rem;
                            color: #000000;
                            margin-bottom: 5px;
                        }
                        .status, .year {
                            font-size: 0.9rem;
                            color: #e74c3c;
                            font-weight: 600;
                        }
                        .skills-grid {
                            display: grid;
                            grid-template-columns: 1fr 1fr;
                            gap: 15px;
                        }
                        .skill-category {
                            padding: 15px;
                            background: #f8f9fa;
                            border-radius: 8px;
                            border-left: 4px solid #9b59b6;
                        }
                        .skill-category h4 {
                            font-size: 1rem;
                            font-weight: 700;
                            color: #2c3e50;
                            margin-bottom: 8px;
                        }
                        .skill-category p {
                            font-size: 0.9rem;
                            color: #030303;
                            line-height: 1.4;
                        }
                        .references-text {
                            font-style: italic;
                            color: #7f8c8d;
                            text-align: center;
                            padding: 20px;
                            background: #f8f9fa;
                            border-radius: 8px;
                        }
                        @media print {
                            body { margin: 0; padding: 0; }
                            .resume-container { box-shadow: none; border-radius: 0; }
                        }
                    </style>
                </head>
                <body>
                    ${resumeContent}
                </body>
                </html>
            `);
            
            printWindow.document.close();
            
            // Wait for content to load, then trigger print dialog
            setTimeout(() => {
                printWindow.print();
            }, 500);
        });
    }
});
