<script>
	import '../app.css';
	import { onMount } from 'svelte';
	onMount(() => {
		const viewport = document.createElement('meta');
		viewport.name = 'viewport';
		viewport.content = 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0';
		document.head.appendChild(viewport);
	});
</script>

<slot />

<style global lang="postcss">
	:global(body) {
		background-color: theme('colors.bg-primary');
	}
</style>
