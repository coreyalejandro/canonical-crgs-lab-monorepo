# UICare

UICare is a collection of React components designed to make web applications more accessible, intuitive, and supportive of users' mental well-being. It focuses on creating interfaces that are comfortable for neurodivergent users while enhancing the experience for everyone.

## Installation

```bash
# Using npm
npm install uicare

# Using yarn
yarn add uicare

# Using pnpm
pnpm add uicare
```

## Quick Start

1. Add the required CSS to your project:

```css
/* In your globals.css or equivalent */
:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

.reality-layer {
  min-height: 100vh;
  transition: all 0.5s ease-in-out;
}

.reality-layer.ninja {
  filter: contrast(1.3) brightness(0.7) saturate(1.4);
  background: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1));
}

.reality-layer.red {
  filter: sepia(1) hue-rotate(320deg) saturate(2.5);
  background: linear-gradient(rgba(255, 0, 0, 0.05), rgba(255, 0, 0, 0.05));
}
```

2. Wrap your application with the providers:

```jsx
import { SettingsProvider, RealityProvider } from 'uicare';

function App() {
  return (
    <SettingsProvider>
      <RealityProvider>
        {/* Your application components */}
      </RealityProvider>
    </SettingsProvider>
  );
}
```

3. Add the components where needed:

```jsx
import { RealityFilter, NinjaPresence, SettingsPanel } from 'uicare';

function Layout() {
  return (
    <>
      <RealityFilter />
      <NinjaPresence />
      <SettingsPanel />
    </>
  );
}
```

## Features

- **Reality Filters**: Allow users to switch between different visual modes to suit their preferences.
- **Ninja Presence**: A subtle, animated indicator that provides gentle visual feedback without causing distractions.
- **Trauma-Informed Interactions**: Components designed with sensitivity to potential triggers, ensuring a safe user experience.

## Components

### RealityProvider
The main provider that enables reality filters in your application.

### RealityFilter
A component that allows users to switch between different visual modes.

### NinjaPresence
A subtle indicator that provides gentle visual feedback.

### SettingsPanel
A panel that allows users to customize various aspects of UICare.

## Customization

UICare is designed to be highly customizable. You can modify the appearance and behavior of components by:

1. Adjusting CSS variables in your styles
2. Using the SettingsPanel for user-level customization
3. Extending components for advanced customization

For detailed customization instructions, see the [Documentation](https://github.com/coreyalejandro/uicare-components/documentation).

## Documentation

For comprehensive documentation, including detailed explanations, usage examples, and customization guides, visit the [Documentation](https://github.com/coreyalejandro/uicare-components/documentation) page.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for more accessible and user-friendly web interfaces
- Special thanks to the neurodivergent community for their insights and feedback

## Development Environment Setup

### Prerequisites

- Node.js 18.0.0 or higher
- Yarn 1.22.0 or higher
- Git

### Getting Started

1. Clone the repository:
```bash
git clone https://github.com/coreyalejandro/uicare-components.git
cd uicare-components
```

2. Install dependencies:
```bash
yarn install
```

3. Start the development server:
```bash
yarn dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

### Available Scripts

- `yarn dev`: Start the development server
- `yarn build`: Build the production application
- `yarn start`: Start the production server
- `yarn lint`: Run ESLint
- `yarn test`: Run tests
