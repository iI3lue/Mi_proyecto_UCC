// ============================================
// SISTEMA DE TEMA CLARO/OSCURO
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Cargar tema guardado
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // Toggle de tema
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Animación del toggle
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = 'rotate(0deg)';
            }, 300);
        });
    }
    
    // Menú hamburguesa móvil
    const hamburger = document.getElementById('hamburger');
    const navbarMenu = document.getElementById('navbar-menu');
    
    if (hamburger && navbarMenu) {
        hamburger.addEventListener('click', function() {
            navbarMenu.classList.toggle('active');
            
            // Animación del hamburger
            const spans = this.querySelectorAll('span');
            if (navbarMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translateY(8px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
                // Prevenir scroll del body cuando el menú está abierto
                document.body.style.overflow = 'hidden';
            } else {
                spans[0].style.transform = 'rotate(0) translateY(0)';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'rotate(0) translateY(0)';
                // Restaurar scroll del body
                document.body.style.overflow = '';
            }
        });
        
        // Cerrar menú al hacer clic en un enlace
        const navLinks = navbarMenu.querySelectorAll('.navbar-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navbarMenu.classList.remove('active');
                const spans = hamburger.querySelectorAll('span');
                spans[0].style.transform = 'rotate(0) translateY(0)';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'rotate(0) translateY(0)';
                document.body.style.overflow = '';
            });
        });
        
        // Cerrar menú al hacer clic fuera de él
        document.addEventListener('click', function(event) {
            if (navbarMenu.classList.contains('active') && 
                !navbarMenu.contains(event.target) && 
                !hamburger.contains(event.target)) {
                navbarMenu.classList.remove('active');
                const spans = hamburger.querySelectorAll('span');
                spans[0].style.transform = 'rotate(0) translateY(0)';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'rotate(0) translateY(0)';
                document.body.style.overflow = '';
            }
        });
        
        // Cerrar menú al cambiar tamaño de pantalla (responsive)
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                if (window.innerWidth > 768 && navbarMenu.classList.contains('active')) {
                    navbarMenu.classList.remove('active');
                    const spans = hamburger.querySelectorAll('span');
                    spans[0].style.transform = 'rotate(0) translateY(0)';
                    spans[1].style.opacity = '1';
                    spans[2].style.transform = 'rotate(0) translateY(0)';
                    document.body.style.overflow = '';
                }
            }, 100);
        });
    }
});

// ============================================
// CARRITO - FUNCIONES AJAX
// ============================================

// Obtener cookie CSRF de Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Actualizar contador del carrito
function updateCartCount() {
    fetch('/api/cart/count/')
        .then(response => response.json())
        .then(data => {
            const cartBadge = document.querySelector('.cart-badge');
            if (cartBadge) {
                cartBadge.textContent = data.count;
                if (data.count > 0) {
                    cartBadge.style.display = 'inline-block';
                } else {
                    cartBadge.style.display = 'none';
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

// Agregar al carrito
function addToCart(productId, button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading"></span> Agregando...';
    button.disabled = true;
    
    fetch(`/carrito/agregar/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mostrar mensaje de éxito
            showNotification('¡Producto agregado al carrito!', 'success');
            
            // Actualizar contador
            updateCartCount();
            
            // Animación de éxito en el botón
            button.innerHTML = '✓ Agregado';
            button.classList.add('btn-success');
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.disabled = false;
            }, 2000);
        } else {
            throw new Error(data.message || 'Error al agregar al carrito');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification(error.message || 'Error al agregar al carrito', 'error');
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

// Actualizar cantidad en el carrito
function updateCartQuantity(productId, change) {
    const quantityElement = document.querySelector(`#quantity-${productId}`);
    const currentQuantity = parseInt(quantityElement.textContent);
    const newQuantity = currentQuantity + change;
    
    if (newQuantity < 1) {
        if (confirm('¿Desea eliminar este producto del carrito?')) {
            removeFromCart(productId);
        }
        return;
    }
    
    fetch('/api/cart/update/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: newQuantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar cantidad
            quantityElement.textContent = newQuantity;
            
            // Actualizar subtotal
            const subtotalElement = document.querySelector(`#subtotal-${productId}`);
            if (subtotalElement) {
                subtotalElement.textContent = `$${data.subtotal.toFixed(2)}`;
            }
            
            // Actualizar total
            const totalElement = document.querySelector('#cart-total');
            if (totalElement) {
                totalElement.textContent = `$${data.total.toFixed(2)}`;
            }
            
            // Actualizar contador
            updateCartCount();
            
            // Animación de actualización
            quantityElement.style.transform = 'scale(1.2)';
            setTimeout(() => {
                quantityElement.style.transform = 'scale(1)';
            }, 200);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al actualizar cantidad', 'error');
    });
}

// Eliminar del carrito
function removeFromCart(productId) {
    const cartItem = document.querySelector(`#cart-item-${productId}`);
    
    fetch('/api/cart/remove/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Animación de eliminación
            cartItem.style.transform = 'translateX(100%)';
            cartItem.style.opacity = '0';
            
            setTimeout(() => {
                cartItem.remove();
                
                // Actualizar total
                const totalElement = document.querySelector('#cart-total');
                if (totalElement) {
                    totalElement.textContent = `$${data.total.toFixed(2)}`;
                }
                
                // Actualizar contador
                updateCartCount();
                
                // Si el carrito está vacío, mostrar mensaje
                const cartContainer = document.querySelector('.cart-container');
                if (cartContainer && cartContainer.querySelectorAll('.cart-item').length === 0) {
                    cartContainer.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">🛒</div>
                            <div class="empty-state-text">Tu carrito está vacío</div>
                            <a href="/productos" class="btn btn-primary">Ver productos</a>
                        </div>
                    `;
                }
                
                showNotification('Producto eliminado del carrito', 'success');
            }, 300);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al eliminar producto', 'error');
    });
}

// ============================================
// BÚSQUEDA EN TIEMPO REAL
// ============================================
let searchTimeout;

function setupSearch() {
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const priceFilter = document.getElementById('price-filter');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch();
            }, 500); // Esperar 500ms después de que el usuario deje de escribir
        });
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', performSearch);
    }
    
    if (priceFilter) {
        priceFilter.addEventListener('change', performSearch);
    }
}

function performSearch() {
    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const priceFilter = document.getElementById('price-filter');
    
    const query = searchInput ? searchInput.value : '';
    const category = categoryFilter ? categoryFilter.value : '';
    const priceOrder = priceFilter ? priceFilter.value : '';
    
    // Construir URL con parámetros
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (category) params.append('category', category);
    if (priceOrder) params.append('price', priceOrder);
    
    // Redirigir a la página de búsqueda
    window.location.href = `/productos?${params.toString()}`;
}

// ============================================
// SISTEMA DE NOTIFICACIONES
// ============================================
function showNotification(message, type = 'info') {
    // Crear contenedor de mensajes si no existe
    let messagesContainer = document.querySelector('.messages');
    if (!messagesContainer) {
        messagesContainer = document.createElement('div');
        messagesContainer.className = 'messages';
        document.body.appendChild(messagesContainer);
    }
    
    // Crear alerta
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <span>${getAlertIcon(type)}</span>
        <span>${message}</span>
    `;
    
    messagesContainer.appendChild(alert);
    
    // Auto-eliminar después de 5 segundos
    setTimeout(() => {
        alert.style.transform = 'translateX(100%)';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

function getAlertIcon(type) {
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    return icons[type] || icons.info;
}

// ============================================
// ANIMACIONES DE SCROLL
// ============================================
function setupScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Observar tarjetas de producto
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.5s ease ${index * 0.1}s`;
        observer.observe(card);
    });
}

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Actualizar contador del carrito al cargar la página
    updateCartCount();
    
    // Configurar búsqueda
    setupSearch();
    
    // Configurar animaciones de scroll
    setupScrollAnimations();
    
    // Auto-cerrar alertas de Django messages
    setTimeout(() => {
        const djangoMessages = document.querySelectorAll('.alert');
        djangoMessages.forEach(alert => {
            alert.style.transform = 'translateX(100%)';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});

// ============================================
// PREVENIR MÚLTIPLES ENVÍOS DE FORMULARIOS
// ============================================
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn && !submitBtn.disabled) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Procesando...';
        
        // Re-habilitar después de 3 segundos por seguridad
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = submitBtn.dataset.originalText || 'Enviar';
        }, 3000);
    }
});
