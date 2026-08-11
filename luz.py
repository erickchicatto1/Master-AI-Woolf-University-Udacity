"""
Fórmulas de Física de la Luz
=============================
Incluye: ondas electromagnéticas, óptica geométrica, efecto fotoeléctrico,
interferencia y difracción.
"""

# Constantes físicas
c = 3e8          # velocidad de la luz en el vacío (m/s)
h = 6.626e-34    # constante de Planck (J·s)
eV = 1.602e-19   # 1 electronvoltio en Joules


# ---------- 1. Relación velocidad, frecuencia y longitud de onda ----------
def velocidad_onda(frecuencia, longitud_onda):
    """c = f * λ"""
    return frecuencia * longitud_onda


def frecuencia_onda(velocidad, longitud_onda):
    """f = c / λ"""
    return velocidad / longitud_onda


def longitud_onda(velocidad, frecuencia):
    """λ = c / f"""
    return velocidad / frecuencia


# ---------- 2. Energía del fotón (Ecuación de Planck) ----------
def energia_foton(frecuencia):
    """E = h * f"""
    return h * frecuencia


def energia_foton_por_longitud(longitud_onda):
    """E = h * c / λ"""
    return h * c / longitud_onda


# ---------- 3. Efecto fotoeléctrico ----------
def energia_cinetica_fotoelectron(frecuencia, funcion_trabajo):
    """Ec = h*f - W  (Einstein)"""
    return h * frecuencia - funcion_trabajo


# ---------- 4. Índice de refracción y Ley de Snell ----------
def indice_refraccion(c_vacio, v_medio):
    """n = c / v"""
    return c_vacio / v_medio


def ley_snell(n1, angulo1_grados, n2):
    """n1 * sin(θ1) = n2 * sin(θ2) -> devuelve θ2 en grados"""
    import math
    angulo1_rad = math.radians(angulo1_grados)
    sin_theta2 = (n1 * math.sin(angulo1_rad)) / n2
    if abs(sin_theta2) > 1:
        return None  # reflexión interna total, no hay refracción
    return math.degrees(math.asin(sin_theta2))


# ---------- 5. Óptica geométrica: espejos y lentes ----------
def ecuacion_lente(f, do=None, di=None):
    """1/f = 1/do + 1/di  -> despeja la variable faltante"""
    if do is None:
        return 1 / ((1/f) - (1/di))
    if di is None:
        return 1 / ((1/f) - (1/do))
    raise ValueError("Debes dejar 'do' o 'di' como None para calcularla")


def aumento_lateral(di, do):
    """m = -di / do"""
    return -di / do


# ---------- 6. Interferencia (experimento de Young) ----------
def franjas_young(m, longitud_onda, distancia_pantalla, separacion_rendijas):
    """y_m = m * λ * L / d  (posición de la franja de orden m)"""
    return m * longitud_onda * distancia_pantalla / separacion_rendijas


# ---------- 7. Difracción (red de difracción) ----------
def red_difraccion(m, longitud_onda, d):
    """d * sin(θ) = m * λ  -> devuelve θ en grados"""
    import math
    sin_theta = m * longitud_onda / d
    if abs(sin_theta) > 1:
        return None
    return math.degrees(math.asin(sin_theta))


# ---------------- EJEMPLOS DE USO ----------------
if __name__ == "__main__":
    print("== Ejemplos ==")

    # Frecuencia de luz visible (λ = 500 nm)
    lam = 500e-9
    f = frecuencia_onda(c, lam)
    print(f"Frecuencia para λ=500nm: {f:.3e} Hz")

    # Energía del fotón
    E = energia_foton_por_longitud(lam)
    print(f"Energía del fotón: {E:.3e} J  ({E/eV:.2f} eV)")

    # Ley de Snell: luz de aire (n=1) a vidrio (n=1.5), ángulo incidencia 30°
    theta2 = ley_snell(1.0, 30, 1.5)
    print(f"Ángulo refractado en vidrio: {theta2:.2f}°")

    # Lente convergente: f=10cm, do=30cm -> hallar di
    di = ecuacion_lente(f=10, do=30)
    print(f"Distancia imagen (di): {di:.2f} cm")

    # Interferencia de Young: m=1, λ=600nm, L=2m, d=0.5mm
    y1 = franjas_young(1, 600e-9, 2, 0.5e-3)
    print(f"Posición 1ra franja brillante: {y1*1000:.2f} mm")
