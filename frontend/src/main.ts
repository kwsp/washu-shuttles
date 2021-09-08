import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		apiUrl: 'http://192.168.0.146:9999/api'
	}
});

export default app;