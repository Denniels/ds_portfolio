"""
Estilos y componentes visuales para la página de productos
"""

def get_product_card_styles():
    """Retorna los estilos CSS para las tarjetas de productos"""
    return """
    <style>
    /* Reset y variables globales */
    .products-container * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    /* Contenedor principal */
    .products-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        width: 100%;
    }
    
    /* Estilos base para las tarjetas */
    .product-card {
        background: linear-gradient(145deg, 
            rgba(255, 255, 255, 0.08),
            rgba(255, 255, 255, 0.03)
        );
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 1.5rem;
        padding: 2.5rem;
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        overflow: hidden;
        position: relative;
        color: rgb(240, 240, 240);
    }
    
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, 
            var(--primary-color),
            var(--secondary-color)
        );
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .product-card:hover::before {
        opacity: 1;
    }
    
    /* Título del producto */
    .product-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        color: var(--text-color);
        display: flex;
        align-items: center;
        gap: 1rem;
        letter-spacing: -0.02em;
    }
    
    .product-title .icon {
        font-size: 2.5rem;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.5rem;
        border-radius: 1rem;
        backdrop-filter: blur(5px);
    }
    
    /* Descripción del producto */
    .product-description {
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
        color: rgb(240, 240, 240) !important;
        margin: 1.5rem 0 !important;
        padding: 1.8rem !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 1rem !important;
        border-left: 4px solid var(--primary-color, rgb(70, 120, 255)) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        white-space: pre-wrap !important;
    }
    
    .product-description p {
        margin: 0;
        text-align: left;
        max-width: 65ch;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    .product-description::before {
        content: '💡';
        position: absolute;
        top: 1.2rem;
        left: 1.2rem;
        font-size: 1.5rem;
        opacity: 0.5;
    }
    
    .product-description[data-content="product-desc"] {
        padding-left: 3.5rem;
    }
    
    .product-description:hover {
        background: rgba(var(--primary-color-rgb), 0.05);
        transform: translateX(5px);
    }
    
    /* Badges de estado */
    .status-badge {
        display: inline-flex !important;
        align-items: center !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 2rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        margin: 1rem 0 !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .status-badge::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg,
            rgba(255, 255, 255, 0),
            rgba(255, 255, 255, 0.1),
            rgba(255, 255, 255, 0)
        );
        transform: translateX(-100%);
        animation: shimmer 2s infinite;
    }
    
    .status-badge.demo {
        color: #2ed573 !important;
        border-color: rgba(46, 213, 115, 0.3) !important;
        background: rgba(46, 213, 115, 0.1) !important;
    }
    
    .status-badge.dev {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.15), rgba(255, 165, 0, 0.05));
        color: #ffa502;
        border: 1px solid rgba(255, 165, 0, 0.3);
    }
    
    .status-badge.concept {
        background: linear-gradient(135deg, rgba(128, 128, 128, 0.15), rgba(128, 128, 128, 0.05));
        color: #808080;
        border: 1px solid rgba(128, 128, 128, 0.3);
    }
    
    /* Secciones de características y tecnologías */
    .features-section, .tech-section {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 1rem !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
    }
    
    .features-section:hover, .tech-section:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-2px);
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1.8rem;
        color: var(--text-color);
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(var(--primary-color-rgb), 0.2);
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 50px;
        height: 2px;
        background: var(--primary-color);
    }
    
    /* Items de características y tecnologías */
    .features-grid, .tech-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)) !important;
        gap: 1rem !important;
    }
    
    .feature-item, .tech-item {
        color: rgb(240, 240, 240) !important;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 0.8rem !important;
        padding: 1rem 1.2rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    
    .feature-item::before {
        content: "✓";
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        background: rgba(var(--primary-color-rgb), 0.1);
        color: var(--primary-color);
        border-radius: 50%;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .tech-item::before {
        content: "⚙️";
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        font-size: 1.2rem;
    }
    
    .feature-item:hover, .tech-item:hover {
        background: rgba(var(--primary-color-rgb), 0.08);
        transform: translateX(5px);
        border-color: rgba(var(--primary-color-rgb), 0.2);
    }
    
    /* Botón de demo */
    .st-emotion-cache-19rxjzo {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(var(--primary-color-rgb), 0.2) !important;
    }
    
    .st-emotion-cache-19rxjzo:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(var(--primary-color-rgb), 0.3) !important;
    }
    </style>
    """

def get_status_badge(status):
    """Retorna el HTML para el badge de estado del producto"""
    icons = {
        "demo": "🚀",
        "dev": "🔨",
        "concept": "💭"
    }
    
    labels = {
        "demo": "Demo Disponible",
        "dev": "En Desarrollo",
        "concept": "Concepto"
    }
    
    return f"""
    <div class="status-badge {status}">
        {icons[status]} {labels[status]}
    </div>
    """

def product_card_template(title, description, icon, status, features, tech_stack):
    """Genera el HTML para una tarjeta de producto"""
    # Limpiar y formatear la descripción
    description = description.strip()
    
    # Generar HTML para características
    features_html = '<div class="features-grid">'
    for i, feature in enumerate(features or []):
        features_html += f"""
            <div class="feature-item" style="--item-index: {i}">
                {feature}
            </div>"""
    features_html += '</div>'

    # Generar HTML para stack tecnológico
    tech_html = '<div class="tech-grid">'
    for i, tech in enumerate(tech_stack or []):
        tech_html += f"""
            <div class="tech-item" style="--item-index: {i}">
                {tech}
            </div>"""
    tech_html += '</div>'

    return f"""
    <div class="product-card">
        <div class="product-title">
            <span class="icon">{icon}</span>
            <span>{title}</span>
        </div>
        {get_status_badge(status)}

        <div class="product-description">
            {description}
        </div>

        <div class="features-section">
            <div class="section-title">✨ Características</div>
            {features_html}
        </div>

        <div class="tech-section">
            <div class="section-title">🛠️ Stack Tecnológico</div>
            {tech_html}
        </div>
    </div>
    """
