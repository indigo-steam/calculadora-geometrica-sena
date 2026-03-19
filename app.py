import math
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Ellipse

st.set_page_config(page_title="Calculadora geométrica", layout="centered")

st.title("Calculadora de perímetros, áreas y volúmenes")
st.write("Aplicación para calcular figuras planas y sólidos regulares.")


def bloquear_edicion_selectbox():
    components.html(
        """
        <script>
        const bloquearInputsSelect = () => {
            try {
                const doc = window.parent.document;
                const inputs = doc.querySelectorAll('div[data-baseweb="select"] input');
                inputs.forEach((input) => {
                    input.setAttribute('readonly', 'readonly');
                    input.style.caretColor = 'transparent';
                });
            } catch (error) {
            }
        };

        bloquearInputsSelect();
        setTimeout(bloquearInputsSelect, 200);
        setTimeout(bloquearInputsSelect, 800);
        </script>
        """,
        height=0,
        width=0,
    )


bloquear_edicion_selectbox()

# Selection is required to maintain algorithm integrity and avoid invalid states
def selectbox_obligatorio(label, opciones, key):
    valor_actual = st.session_state.get(key)
    if valor_actual not in opciones:
        st.session_state[key] = opciones[0]

    seleccion = st.selectbox(
        label,
        opciones,
        index=opciones.index(st.session_state[key]),
        key=key,
        accept_new_options=False,
    )

    if seleccion not in opciones:
        st.session_state[key] = opciones[0]
        return opciones[0]

    return seleccion


tipos_calculo = ["Perímetro", "Área", "Volumen", "Sólido irregular"]
tipo = selectbox_obligatorio(
    "Seleccione el tipo de cálculo",
    tipos_calculo,
    key="tipo_calculo_select",
)

def mostrar_resultado(formula, reemplazo, resultado):
    st.subheader("Desarrollo del algoritmo")
    st.write(f"**Fórmula:** {formula}")
    st.write(f"**Sustitución:** {reemplazo}")
    st.success(f"**Resultado:** {resultado}")

def dibujar_rectangulo(base, altura):
    fig, ax = plt.subplots()
    rect = Rectangle((1, 1), base, altura, fill=False)
    ax.add_patch(rect)
    ax.text(1 + base / 2, 0.7, f"b = {base}", ha="center")
    ax.text(0.5, 1 + altura / 2, f"h = {altura}", va="center", rotation=90)
    ax.set_xlim(0, base + 2)
    ax.set_ylim(0, altura + 2)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)

def dibujar_cuadrado(lado):
    fig, ax = plt.subplots()
    cuad = Rectangle((1, 1), lado, lado, fill=False)
    ax.add_patch(cuad)
    ax.text(1 + lado / 2, 0.7, f"lado = {lado}", ha="center")
    ax.text(0.5, 1 + lado / 2, f"lado = {lado}", va="center", rotation=90)
    ax.set_xlim(0, lado + 2)
    ax.set_ylim(0, lado + 2)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)

def dibujar_circulo(radio):
    fig, ax = plt.subplots()
    circ = Circle((radio + 1, radio + 1), radio, fill=False)
    ax.add_patch(circ)
    ax.plot([radio + 1, radio * 2 + 1], [radio + 1, radio + 1])
    ax.text(radio + 1.2, radio + 1.2, f"r = {radio}")
    ax.set_xlim(0, radio * 2 + 2)
    ax.set_ylim(0, radio * 2 + 2)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)

def dibujar_triangulo(base, altura):
    fig, ax = plt.subplots()
    puntos = [(1, 1), (1 + base, 1), (1 + base / 2, 1 + altura)]
    tri = Polygon(puntos, fill=False)
    ax.add_patch(tri)
    ax.text(1 + base / 2, 0.7, f"b = {base}", ha="center")
    ax.text(1 + base / 2 + 0.2, 1 + altura / 2, f"h = {altura}")
    ax.set_xlim(0, base + 2)
    ax.set_ylim(0, altura + 2)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)


def draw_cube(lado):
    fig, ax = plt.subplots()
    origen_x, origen_y = 1, 1
    desfase_x = lado * 0.45
    desfase_y = lado * 0.35

    cara_frontal = Rectangle((origen_x, origen_y), lado, lado, fill=False)
    cara_trasera = Rectangle((origen_x + desfase_x, origen_y + desfase_y), lado, lado, fill=False)
    ax.add_patch(cara_trasera)
    ax.add_patch(cara_frontal)

    ax.plot([origen_x, origen_x + desfase_x], [origen_y, origen_y + desfase_y], color="black")
    ax.plot([origen_x + lado, origen_x + lado + desfase_x], [origen_y, origen_y + desfase_y], color="black")
    ax.plot([origen_x, origen_x + desfase_x], [origen_y + lado, origen_y + lado + desfase_y], color="black")
    ax.plot(
        [origen_x + lado, origen_x + lado + desfase_x],
        [origen_y + lado, origen_y + lado + desfase_y],
        color="black",
    )

    ax.text(origen_x + lado / 2, origen_y - 0.35, f"lado = {lado}", ha="center")
    ax.set_xlim(0, origen_x + lado + desfase_x + 1)
    ax.set_ylim(0, origen_y + lado + desfase_y + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)


def draw_prism(largo, ancho, altura):
    fig, ax = plt.subplots()
    origen_x, origen_y = 1, 1
    desfase_x = ancho * 0.6
    desfase_y = ancho * 0.35

    cara_frontal = Rectangle((origen_x, origen_y), largo, altura, fill=False)
    cara_trasera = Rectangle((origen_x + desfase_x, origen_y + desfase_y), largo, altura, fill=False)
    ax.add_patch(cara_trasera)
    ax.add_patch(cara_frontal)

    ax.plot([origen_x, origen_x + desfase_x], [origen_y, origen_y + desfase_y], color="black")
    ax.plot([origen_x + largo, origen_x + largo + desfase_x], [origen_y, origen_y + desfase_y], color="black")
    ax.plot([origen_x, origen_x + desfase_x], [origen_y + altura, origen_y + altura + desfase_y], color="black")
    ax.plot(
        [origen_x + largo, origen_x + largo + desfase_x],
        [origen_y + altura, origen_y + altura + desfase_y],
        color="black",
    )

    ax.text(origen_x + largo / 2, origen_y - 0.35, f"largo = {largo}", ha="center")
    ax.text(origen_x - 0.35, origen_y + altura / 2, f"altura = {altura}", va="center", rotation=90)
    ax.text(
        origen_x + largo + desfase_x / 2,
        origen_y + desfase_y / 2 + 0.1,
        f"ancho = {ancho}",
        rotation=32,
    )

    ax.set_xlim(0, origen_x + largo + desfase_x + 1.2)
    ax.set_ylim(0, origen_y + altura + desfase_y + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)


def draw_cylinder(radio, altura):
    fig, ax = plt.subplots()
    centro_x = radio + 1.2
    base_y = 1
    tapa_y = base_y + altura
    alto_elipse = radio * 0.55

    elipse_superior = Ellipse((centro_x, tapa_y), width=2 * radio, height=alto_elipse, fill=False)
    elipse_inferior = Ellipse(
        (centro_x, base_y),
        width=2 * radio,
        height=alto_elipse,
        fill=False,
        linestyle="--",
    )
    ax.add_patch(elipse_superior)
    ax.add_patch(elipse_inferior)

    ax.plot([centro_x - radio, centro_x - radio], [base_y, tapa_y], color="black")
    ax.plot([centro_x + radio, centro_x + radio], [base_y, tapa_y], color="black")

    ax.plot([centro_x, centro_x + radio], [tapa_y, tapa_y], color="tab:blue")
    ax.text(centro_x + radio / 2, tapa_y + 0.25, f"r = {radio}", ha="center", color="tab:blue")

    linea_altura_x = centro_x + radio + 0.5
    ax.plot([linea_altura_x, linea_altura_x], [base_y, tapa_y], color="tab:green")
    ax.text(
        linea_altura_x + 0.2,
        base_y + altura / 2,
        f"h = {altura}",
        va="center",
        rotation=90,
        color="tab:green",
    )

    ax.set_xlim(0, centro_x + radio + 1.3)
    ax.set_ylim(0, tapa_y + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)


def draw_sphere(radio):
    fig, ax = plt.subplots()
    centro_x, centro_y = radio + 1.2, radio + 1.2

    contorno = Circle((centro_x, centro_y), radio, fill=False)
    ecuador = Ellipse((centro_x, centro_y), width=2 * radio, height=radio * 0.65, fill=False, linestyle="--")
    ax.add_patch(contorno)
    ax.add_patch(ecuador)

    ax.plot([centro_x, centro_x + radio], [centro_y, centro_y], color="tab:blue")
    ax.text(centro_x + radio / 2, centro_y + 0.2, f"r = {radio}", ha="center", color="tab:blue")

    ax.set_xlim(0, centro_x + radio + 1)
    ax.set_ylim(0, centro_y + radio + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    st.pyplot(fig)

if tipo == "Perímetro":
    figuras_perimetro = ["Rectángulo", "Cuadrado", "Círculo"]
    figura = selectbox_obligatorio(
        "Seleccione la figura",
        figuras_perimetro,
        key="figura_perimetro_select",
    )

    if figura == "Rectángulo":
        base = st.number_input("Base", min_value=0.1, value=5.0)
        altura = st.number_input("Altura", min_value=0.1, value=3.0)
        perimetro = 2 * (base + altura)
        dibujar_rectangulo(base, altura)
        mostrar_resultado(
            "P = 2 × (base + altura)",
            f"P = 2 × ({base} + {altura})",
            f"{perimetro}"
        )

    elif figura == "Cuadrado":
        lado = st.number_input("Lado", min_value=0.1, value=4.0)
        perimetro = 4 * lado
        dibujar_cuadrado(lado)
        mostrar_resultado(
            "P = 4 × lado",
            f"P = 4 × {lado}",
            f"{perimetro}"
        )

    elif figura == "Círculo":
        radio = st.number_input("Radio", min_value=0.1, value=3.0)
        perimetro = 2 * math.pi * radio
        dibujar_circulo(radio)
        mostrar_resultado(
            "P = 2 × π × r",
            f"P = 2 × π × {radio}",
            f"{perimetro:.2f}"
        )

elif tipo == "Área":
    figuras_area = ["Rectángulo", "Cuadrado", "Círculo", "Triángulo"]
    figura = selectbox_obligatorio(
        "Seleccione la figura",
        figuras_area,
        key="figura_area_select",
    )

    if figura == "Rectángulo":
        base = st.number_input("Base", min_value=0.1, value=5.0)
        altura = st.number_input("Altura", min_value=0.1, value=3.0)
        area = base * altura
        dibujar_rectangulo(base, altura)
        mostrar_resultado(
            "A = base × altura",
            f"A = {base} × {altura}",
            f"{area}"
        )

    elif figura == "Cuadrado":
        lado = st.number_input("Lado", min_value=0.1, value=4.0)
        area = lado ** 2
        dibujar_cuadrado(lado)
        mostrar_resultado(
            "A = lado²",
            f"A = {lado}²",
            f"{area}"
        )

    elif figura == "Círculo":
        radio = st.number_input("Radio", min_value=0.1, value=3.0)
        area = math.pi * radio ** 2
        dibujar_circulo(radio)
        mostrar_resultado(
            "A = π × r²",
            f"A = π × {radio}²",
            f"{area:.2f}"
        )

    elif figura == "Triángulo":
        base = st.number_input("Base", min_value=0.1, value=6.0)
        altura = st.number_input("Altura", min_value=0.1, value=4.0)
        area = (base * altura) / 2
        dibujar_triangulo(base, altura)
        mostrar_resultado(
            "A = (base × altura) / 2",
            f"A = ({base} × {altura}) / 2",
            f"{area}"
        )

elif tipo == "Volumen":
    solidos = ["Cubo", "Prisma rectangular", "Cilindro", "Esfera"]
    solido = selectbox_obligatorio(
        "Seleccione el sólido",
        solidos,
        key="solido_volumen_select",
    )

    if solido == "Cubo":
        lado = st.number_input("Lado", min_value=0.1, value=3.0)
        volumen = lado ** 3
        draw_cube(lado)
        mostrar_resultado(
            "V = lado³",
            f"V = {lado}³",
            f"{volumen}"
        )

    elif solido == "Prisma rectangular":
        largo = st.number_input("Largo", min_value=0.1, value=5.0)
        ancho = st.number_input("Ancho", min_value=0.1, value=3.0)
        altura = st.number_input("Altura", min_value=0.1, value=2.0)
        volumen = largo * ancho * altura
        draw_prism(largo, ancho, altura)
        mostrar_resultado(
            "V = largo × ancho × altura",
            f"V = {largo} × {ancho} × {altura}",
            f"{volumen}"
        )

    elif solido == "Cilindro":
        radio = st.number_input("Radio", min_value=0.1, value=2.0)
        altura = st.number_input("Altura", min_value=0.1, value=5.0)
        volumen = math.pi * radio ** 2 * altura
        draw_cylinder(radio, altura)
        mostrar_resultado(
            "V = π × r² × h",
            f"V = π × {radio}² × {altura}",
            f"{volumen:.2f}"
        )

    elif solido == "Esfera":
        radio = st.number_input("Radio", min_value=0.1, value=3.0)
        volumen = (4 / 3) * math.pi * radio ** 3
        draw_sphere(radio)
        mostrar_resultado(
            "V = (4/3) × π × r³",
            f"V = (4/3) × π × {radio}³",
            f"{volumen:.2f}"
        )

elif tipo == "Sólido irregular":
    st.subheader("Método propuesto")
    st.write(
        "Para un sólido irregular se puede usar el método de desplazamiento de agua. "
        "Se mide el volumen inicial del agua en un recipiente, luego se introduce el sólido "
        "y se mide el nuevo volumen. La diferencia corresponde al volumen del sólido."
    )
