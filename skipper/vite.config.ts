import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import pkg from './package.json' with { type: 'json' };

export default defineConfig({
	plugins: [
		sveltekit({
			adapter: adapter({ fallback: '404.html' }),
			// Per GitHub Pages: BASE_PATH=/nome-repo
			paths: { base: (process.env.BASE_PATH ?? '') as '' | `/${string}` }
		})
	],
	define: {
		__APP_VERSION__: JSON.stringify(pkg.version),
		// DEMO=1 npm run build: versione dimostrativa pubblica, con le parti bloccate
		__DEMO__: JSON.stringify(process.env.DEMO === '1')
	},
	test: { include: ['src/**/*.test.ts'] }
});
