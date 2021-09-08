<script lang="ts">
  import Table from "./Table.svelte";

  export let apiUrl: string;

  let schedules: Object = {};
  let weekdayP = true;

  $: suffix = weekdayP ? "_weekday" : "_weekend";
  $: removeSuffix = (s: string) => {
    return s.slice(0, s.lastIndexOf("_"));
  };

  $: scheduleNames = Object.keys(schedules).filter((name) =>
    name.endsWith(suffix)
  );
  let selectName;

  fetch(apiUrl)
    .then((resp) => resp.json())
    .then((res) => {
      schedules = res;
    })
    .catch((err) => console.log(err));
</script>

<main>
  <h2>WashU Shuttles</h2>
  <a href={apiUrl}>API: {apiUrl}</a>

  <section>
    {#if !schedules}
      <p>Waiting for data to load...</p>
    {:else}
      {#each scheduleNames as name}
        <p>{removeSuffix(name)}</p>
        <Table data={schedules[name]} />
      {/each}
    {/if}
  </section>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    /* max-width: 240px; */
    margin: 0 auto;
  }

  h2 {
    color: #ff3e00;
    text-transform: uppercase;
    font-weight: 300;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
