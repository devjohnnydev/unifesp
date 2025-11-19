# TeleAcolhe - Design Guidelines

## Design Approach
**System**: Material Design principles with healthcare-focused adaptations, drawing inspiration from accessible health platforms like Ada Health and government digital health services. The design prioritizes trust, clarity, and accessibility for users in vulnerable situations.

## Core Design Principles
- **Trust First**: Clean, professional aesthetic that conveys medical credibility while remaining warm and approachable
- **Radical Accessibility**: Every interaction must work for users with varying abilities and device limitations
- **Information Clarity**: Medical information presented with clear visual hierarchy and plain language

## Typography
- **Primary Font**: Roboto (400, 500, 700) via Google Fonts - excellent legibility for medical content
- **Headings**: 2xl-4xl font sizes, font-semibold to font-bold, leading-tight
- **Body Text**: Base to lg sizes, font-normal, leading-relaxed for comfortable reading of medical information
- **Form Labels**: Text-sm to text-base, font-medium, high contrast for clarity
- **Minimum body text**: 16px (text-base) for accessibility

## Layout System
**Spacing Units**: Consistent use of Tailwind units 4, 6, 8, 12, 16 for predictable rhythm
- Component padding: p-4 to p-8
- Section spacing: py-12 (mobile) to py-20 (desktop)
- Form field gaps: gap-6
- Container max-widths: max-w-4xl for forms, max-w-6xl for content sections

## Component Library

### Navigation
- Sticky header with clear logo, minimal navigation (Início, Como Funciona, Sobre, Ajuda)
- Mobile: Hamburger menu with large touch targets (min-height: 48px)
- Emergency disclaimer banner at top (subtle, non-alarming)

### Hero Section
- Single column, centered content with reassuring headline
- Subheading explaining mission and reach
- Primary CTA button (large, high contrast): "Descrever Sintomas"
- Use calming medical imagery: diverse patients receiving care, community health workers, or abstract healing/wellness visuals (soft, warm tones)

### Symptom Form (Primary Feature)
- Multi-step form with clear progress indicator
- Large, touch-friendly input fields (min-height: 48px)
- Step 1: Basic info (idade, sexo)
- Step 2: Symptom description (textarea with character count)
- Step 3: Duration and intensity (radio buttons with large targets)
- Step 4: Additional factors (checkboxes for existing conditions)
- Inline validation with clear error states
- "Voltar" and "Próximo" buttons always visible

### Results Display
- Card-based layout for differential diagnoses
- Each diagnosis card includes: name, probability indicator, brief description
- Color-coded severity (using accessible color combinations)
- Expandable sections for detailed information
- Clear disclaimer: "Isto não substitui consulta médica"
- CTA: "Procurar Unidade de Saúde Mais Próxima"

### Educational Content Section
- Grid layout: 2 columns (tablet+), 1 column (mobile)
- Icon + title + brief description pattern for health topics
- Links to detailed articles with government/WHO sources

### Trust & Safety Elements
- Data privacy notice (small, always visible)
- Medical disclaimer in every results page
- Contact information for emergency services
- Partner logos (SUS, health organizations) in footer

### Footer
- Multi-column (desktop): About, Resources, Legal, Contact
- Single column (mobile) with accordion sections
- Emergency hotline numbers prominent
- Social proof: "X consultas realizadas"

## Accessibility Implementation
- WCAG 2.1 AA compliance minimum
- Contrast ratios: 7:1 for text, 4.5:1 for interactive elements
- Focus indicators: 3px solid outline on all interactive elements
- Screen reader labels on all form inputs
- Keyboard navigation for entire flow
- Touch targets minimum 48x48px
- Form field labels always visible (no placeholder-only)

## Visual Hierarchy
- Primary actions: Large buttons with solid backgrounds
- Secondary actions: Outlined buttons or text links
- Danger/Warning: Reserved for medical disclaimers and emergency prompts
- Success: Used sparingly for form completion confirmations

## Images
- **Hero Image**: Warm, inclusive photo showing diverse patients in caring medical environment or community health worker assisting patient (avoid clinical/sterile hospital imagery)
- **How It Works Section**: Simple iconography or illustrations showing 3-step process
- **Educational Cards**: Icon-based (medical icons from Material Icons)
- **About Section**: Photo of team or community health impact (builds trust)

## Responsive Behavior
- Mobile-first progression: Stack everything vertically on mobile
- Tablet (md:): Two-column grids for content cards
- Desktop (lg:): Maximum 3-column grids, generous whitespace
- Form remains single column on all breakpoints for focus

## Performance Considerations
- Minimal animations (only for form transitions and loading states)
- Lazy load educational content
- Optimize for 3G connections (target users may have limited bandwidth)
- Progressive enhancement approach

This design balances medical professionalism with warmth and accessibility, creating a trustworthy platform that serves vulnerable communities with dignity and clarity.