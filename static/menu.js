// Инициализация меню
function initializeMenus() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const userMenuButton = document.querySelector('.user-menu-button');
    const userDropdown = document.querySelector('.user-dropdown');
    const body = document.body;

    // Функция закрытия всех меню
    function closeAllMenus() {
        if (navLinks) {
            navLinks.classList.remove('active');
        }
        if (userDropdown) {
            userDropdown.classList.remove('active');
        }
        body.style.overflow = '';
    }

    // Обработка клика вне меню
    document.addEventListener('click', function(e) {
        if ((!hamburger || !hamburger.contains(e.target)) && 
            (!navLinks || !navLinks.contains(e.target)) &&
            (!userMenuButton || !userMenuButton.contains(e.target)) &&
            (!userDropdown || !userDropdown.contains(e.target))) {
            closeAllMenus();
        }
    });

    // Инициализация пользовательского меню
    if (userMenuButton && userDropdown) {
        userMenuButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Закрываем навигационное меню если оно открыто
            if (navLinks) {
                navLinks.classList.remove('active');
            }
            
            // Переключаем пользовательское меню
            userDropdown.classList.toggle('active');
            
            // Управляем прокруткой на мобильных
            if (window.innerWidth <= 768) {
                body.style.overflow = userDropdown.classList.contains('active') ? 'hidden' : '';
            }
        });

        // Закрываем меню при клике на ссылки внутри
        userDropdown.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                closeAllMenus();
            });
        });
    }

    // Инициализация мобильного меню
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Закрываем пользовательское меню если оно открыто
            if (userDropdown) {
                userDropdown.classList.remove('active');
            }
            
            // Переключаем навигационное меню
            navLinks.classList.toggle('active');
            body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
        });

        // Закрываем меню при клике на ссылки
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                closeAllMenus();
            });
        });
    }

    // Обработка изменения размера окна
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeAllMenus();
        }
    });
}

// Гарантируем, что меню будет инициализировано после загрузки DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeMenus);
} else {
    initializeMenus();
}

// Повторная инициализация при динамической загрузке контента
document.addEventListener('turbolinks:load', initializeMenus);
window.addEventListener('load', initializeMenus); 