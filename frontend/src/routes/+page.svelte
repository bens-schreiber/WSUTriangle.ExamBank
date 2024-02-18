<script>
	let searchBarEngaged = false;
	const deltaT = new URL('/src/lib/assets/Delta_T.png', import.meta.url).href;
</script>

<div class="mt-10 flex flex-col items-stretch">
	{#if !searchBarEngaged}
		<img class="h-52 w-52 self-center" src={deltaT} alt="Delta T" />
	{/if}

	<!-- Search Bar-->
	<div class={`mx-4 search-bar ${searchBarEngaged ? 'mt-0' : 'mt-10'}`}>
		<form class="max-w-md mx-auto">
			<label
				for="default-search"
				class="mb-2 text-sm font-medium text-gray-900 sr-only">Search</label
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
                    placeholder="Search Mockups, Logos..."
                    required
                    on:focus={() => searchBarEngaged = true}
                    on:blur={() => searchBarEngaged = false}
                />
				<button
					type="submit"
					class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600"
					>Search</button
				>
			</div>
		</form>
	</div>
</div>
