# Oviora Frontend Design System

This document outlines the design philosophy, UI architecture, and component breakdown for the Oviora Next.js frontend.

---

## 1. Design Philosophy

Oviora embraces a **Neo-brutalist** aesthetic combined with modern, rich web design principles. The goal is to create a premium, dynamic, and engaging user experience that stands out from standard medical applications.

**Key Aesthetic Pillars:**
- **Vibrant & High-Contrast:** Avoiding generic colors in favor of curated, harmonious palettes (e.g., bold accent colors on sleek dark modes).
- **Glassmorphism & Depth:** Using blurred backgrounds and layered UI elements to create a sense of depth.
- **Dynamic Interactions:** Implementing micro-animations, hover effects, and smooth transitions so the application feels responsive and alive.
- **Typography:** Utilizing modern, highly readable sans-serif Google Fonts.

---

## 2. Page Hierarchy

The application is structured around a public landing page and a protected authenticated dashboard.

### 2.1 Public Pages
- **`/` (Landing Page):** The entry point. Features a high-impact hero section, value propositions, and calls to action. Utilizes shared components like the Header and Footer.
- **`/developer`:** Information regarding the platform's API and architecture.

### 2.2 Authenticated Dashboard `/(dashboard)`
These routes are wrapped in a shared Layout that persists the sidebar and top navigation.

- **`/dashboard` (Main Overview):** The central hub. Displays the user's current cycle phase, daily tasks, hormone estimations, and recent symptom logs.
- **`/ocr` (Lab Analyzer):** A dedicated page for users to drag-and-drop PDF/Image lab reports. Displays a loading state during PaddleOCR processing and presents extracted biomarkers in a data table.
- **`/meetings` (Clinician Summary):** An interface for generating and reviewing PDF summaries intended for OBGYN visits.

---

## 3. Shared Component Architecture

To maintain consistency and reduce code duplication, recurring UI elements are extracted into reusable components located in `frontend/src/components/`.

### 3.1 Global Components
- **`Header.tsx`:** The global top navigation bar for public pages. Contains the logo and authentication links.
- **`Footer.tsx`:** The global footer containing links, copyright, and social icons.
- **`UnderConstructionModal.tsx`:** A reusable modal used to gracefully handle clicks on features that are currently in the "Planned" phase of the roadmap.

### 3.2 Dashboard Components
- **`Sidebar.tsx`:** The persistent left-hand navigation menu for authenticated users. Contains links to Dashboard, OCR, Meetings, and Settings.
- **`TopNav.tsx`:** A contextual top bar within the dashboard for user profile access and notifications.
- **`CycleWidget.tsx`:** A visual representation of the user's current menstrual cycle phase (e.g., a circular progress indicator).
- **`TaskCard.tsx`:** A standardized card component for displaying daily actionable recommendations.

---

## 4. State Management & Data Fetching

- **Local State:** React `useState` and `useEffect` are used for component-level UI state (e.g., modal visibility, mobile menu toggles).
- **Data Fetching:** The `src/services/api.ts` file acts as the single source of truth for external data fetching. React components call these async functions and store the resulting data in local state for rendering.
