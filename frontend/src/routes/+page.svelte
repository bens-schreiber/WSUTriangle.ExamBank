<script>
  // @ts-nocheck
  import { onMount } from 'svelte';
  const delta_t = new URL('/src/lib/assets/Delta_T.png', import.meta.url).href;
  const search_input_text = 'Search for an exam or homework...';

  let showModal = false;
  let results = [];
  let query = '';
  let searchTimeout;

  onMount(() => {
    search(query);
  });

  $: if (query) {
    search(query);
  }

  async function search(query) {
    if (searchTimeout) clearTimeout(searchTimeout);

    searchTimeout = setTimeout(async () => {
      const response = await fetch(`http://127.0.0.1:5000/exams/search?query=${query}`);

      if (response.ok) {
        const data = await response.json();
        results = data;
      } else {
        results = [];
      }
    }, 300); // delay in milliseconds
  }

	let name = '';
	let tags = '';
	let image;

	async function submitForm() {
		const formData = new FormData();
		formData.append('name', name);
		formData.append('tags', tags.split(',').map((tag) => tag.trim()).join(' '));
		formData.append('file', image[0]);

		const response = await fetch('http://127.0.0.1:5000/exam', {
			method: 'POST',
			body: formData
		});

		if (response.ok) {
			showModal = false;
			name = '';
			tags = '';
			image = null;
		}
	}
</script>

<div class="mt-10 flex flex-col items-stretch">
	{#if showModal}
		<div class="fixed z-10 inset-0 flex items-center justify-center">
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<div class="fixed inset-0 bg-black opacity-50" on:click={() => (showModal = false)}></div>
			<div class="bg-bg-primary rounded-lg w-64 h-64 shadow-xl relative z-20 p-4">
				<form on:submit|preventDefault={submitForm} class="space-y-4">
					<label class="block">
						<input
							type="text"
							bind:value={name}
							required
							placeholder="Name"
							class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500"
						/>
					</label>
					<label class="block">
						<input
							type="text"
							bind:value={tags}
							required
							placeholder="CSV Tags"
							class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500"
						/>
					</label>
					<label class="block overflow-hidden overflow-ellipsis whitespace-nowrap">
						<input type="file" bind:files={image} required />
					</label>
					<button
						type="submit"
						class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-500 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
						>Submit</button
					>
				</form>
			</div>
		</div>
	{/if}

	<img class="h-52 w-52 self-center" src={delta_t} alt="Delta T" />

	<div class="mx-4 search-bar mt-10">
		<div class="flex justify-between max-w-md mx-auto">
			<form class="flex-grow">
				<label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only"
					>Search</label
				>
				<div class="relative">
					<div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
						<svg
							class="w-4 h-4 text-gray-500 dark:text-gray-400"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 20 20"
						>
							<path
								stroke="currentColor"
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
							/>
						</svg>
					</div>
					<input
						type="search"
						id="default-search"
						class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500"
						placeholder={search_input_text}
						required
						on:input={(event) => search(event.target.value)}
					/>
					<button
						type="submit"
						class="text-white absolute end-1.5 bottom-2.5 bg-blue-700 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600"
						>Search</button
					>
				</div>
			</form>
			<button
				class="text-white bg-blue-700 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 ml-4"
				on:click={() => (showModal = true)}
			>
				Upload
			</button>
		</div>
	</div>
</div>

<div class="grid place-items-center gap-10 mt-10 mb-40">
    {#each [...results].reverse() as item (item.name + item.url + item.tags)}
        <div class="text-center">
			<a href={item.url} class="text-2xl text-white">{item.name}</a>
            <!-- svelte-ignore a11y-missing-attribute -->
            <embed src={item.url + '?t=' + Date.now()} width="300" height="300" class="mt-3"/>

			<!-- split by tags-->
			{#each item.tags.split(' ') as tag}
				<span class="text-xs text-white bg-blue-500 rounded-full px-2 py-1 m-1">{tag}</span>
			{/each}

        </div>
    {/each}
</div>