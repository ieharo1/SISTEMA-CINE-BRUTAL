# 🎬 Sistema de Cine Brutal

<p align="center">
  <img src="https://img.icons8.com/color/200/000000/cinema-.png" alt="Cinema System Logo" width="200"/>
</p>

---

## 📱 Descripción

Sistema de Cine Brutal es una plataforma **full stack** desarrollada con **Django + PostgreSQL + Docker** y un frontend totalmente en **Bootstrap 5** (sin CSS personalizado), para gestionar:

- Cartelera y funciones.
- Selección visual de butacas disponibles/ocupadas.
- Venta de entradas.
- Venta de palomitas/snacks.
- Panel administrativo para operación completa.

> Diseñado para funcionar de forma responsive y lista para producción con despliegue en contenedores.

---

## ✨ Características

### Funcionalidades Implementadas ✅

- ✅ **Cartelera Dinámica** - Funciones ordenadas por fecha
- ✅ **Mapa de Butacas Visual** - Asientos libres/ocupados en tiempo real
- ✅ **Bloqueo de Concurrencia** - Evita doble venta de butacas
- ✅ **Generación de Tickets** - Registro de compra por cliente
- ✅ **Módulo de Snacks** - Palomitas, combos, bebidas y control de stock
- ✅ **Backoffice Django Admin** - Gestión de películas, salas, funciones e inventario
- ✅ **Seed de Demo** - Datos de ejemplo automáticos
- ✅ **Docker + Docker Compose** - Levantamiento completo de app y base de datos
- ✅ **Bootstrap 5 Only** - UI moderna sin CSS extra
- ✅ **Responsive 100%** - Adaptado para móvil, tablet y desktop

### Próximamente 🔄

- 🎟️ Pasarela de pagos
- 📧 Envío de ticket por correo
- 📊 Dashboard de ventas por día/función
- 📱 QR para validación en acceso

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Backend | Django | 5.1.7 |
| Lenguaje | Python | 3.12 (contenedor) |
| Base de datos | PostgreSQL | 16-alpine |
| Servidor WSGI | Gunicorn | 23.0.0 |
| Frontend | Bootstrap | 5.3.3 CDN |
| Contenedores | Docker / Compose | latest |

---

## 📁 Estructura del Proyecto

```
automation-toolkit-devops/
├── cinema_system/
│   ├── cinema/
│   │   ├── management/commands/seed_demo.py
│   │   ├── migrations/0001_initial.py
│   │   ├── templates/cinema/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── showtime_detail.html
│   │   │   └── snacks.html
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── db_wait.py
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
├── docker-compose.yml
└── README.md
```

---


## 📦 Generar ZIP para descarga

Como este repositorio no admite binarios versionados, genera el ZIP localmente con:

```bash
zip -r cine-brutal-sistema.zip cinema_system docker-compose.yml README.md
```

## 🚀 Cómo Ejecutar el Proyecto

### 1. Clonar repositorio
```bash
git clone <tu-repo>
cd automation-toolkit-devops
```

### 2. Levantar con Docker
```bash
docker compose up --build
```

### 3. Abrir aplicación
- App: http://localhost:8000/
- Admin: http://localhost:8000/admin/

### 4. Credenciales admin (crear si deseas)
```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Detener
```bash
docker compose down
```

---

## 🎟️ Flujo de Venta de Entradas

1. Cliente entra a cartelera.
2. Elige función.
3. Selecciona butacas disponibles (verdes).
4. Envía nombre y correo.
5. Sistema valida concurrencia y bloquea butacas.
6. Genera ticket con total por número de asientos.

---

## 🍿 Flujo de Venta de Snacks

1. Cliente entra al módulo de snacks.
2. Selecciona cantidades por producto.
3. Sistema valida stock.
4. Crea orden y descuenta inventario.

---

## 🔐 Concurrencia de Butacas

Se usa transacción atómica con `select_for_update()` + restricción única por función/asiento para impedir sobreventa.

---

## 👨‍💻 Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack Developer · Automatización · Data**

### 📞 Contacto

- 📧 **Email:** zackharo1@gmail.com
- 📱 **WhatsApp:** [+593 988055517](https://wa.me/593988055517)
- 💻 **GitHub:** [ieharo1](https://github.com/ieharo1)
- 🌐 **Portafolio:** [ieharo1.github.io](https://ieharo1.github.io/portafolio-isaac.haro/)

---

## 📄 Licencia

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados.

---

⭐ Si te gustó el proyecto, ¡dame una estrella en GitHub!
