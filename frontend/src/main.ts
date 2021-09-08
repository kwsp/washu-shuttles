import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		apiUrl: 'API_URL'
	}
});

export default app;
