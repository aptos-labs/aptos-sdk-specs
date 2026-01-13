// Bun natively supports TypeScript, no ts-node needed
// Using ESM imports for Cucumber v12+
export default {
  import: ['steps/**/*.ts', 'support/**/*.ts'],
  paths: ['../../features/**/*.feature'],
  format: ['progress-bar', 'html:reports/cucumber-report.html'],
  formatOptions: {
    snippetInterface: 'async-await'
  }
};

